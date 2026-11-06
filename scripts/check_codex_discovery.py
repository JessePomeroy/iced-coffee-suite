#!/usr/bin/env python3
"""Check that a fresh local Codex app-server lists selected manifests from this checkout."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from install import load_catalog


def list_skills(executable: str, cwd: Path, timeout: float) -> dict:
    # This is a separate, short-lived server. No thread/turn or inference request is sent.
    process = subprocess.Popen(
        [executable, "app-server", "--stdio", "-c", "analytics.enabled=false"],
        cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, encoding="utf-8",
    )
    messages = queue.Queue()

    def read_stdout():
        try:
            for line in process.stdout:
                messages.put(line)
        finally:
            messages.put(None)

    reader = threading.Thread(target=read_stdout, daemon=True)
    reader.start()
    deadline = time.monotonic() + timeout

    def send(message):
        process.stdin.write(json.dumps(message) + "\n")
        process.stdin.flush()

    def response(identifier):
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Codex discovery timed out")
            try:
                line = messages.get(timeout=remaining)
            except queue.Empty:
                raise TimeoutError("Codex discovery timed out") from None
            if line is None:
                raise RuntimeError("Codex exited before returning its skill listing")
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("Unexpected Codex app-server response")
            if message.get("id") != identifier:
                continue
            if "error" in message:
                raise RuntimeError("Codex rejected a discovery request; check app-server compatibility")
            result = message.get("result")
            if not isinstance(result, dict):
                raise ValueError("Unexpected Codex app-server result")
            return result

    try:
        send({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "iced-coffee-discovery", "version": "1.0"},
            "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True},
        }})
        response(1)
        send({"method": "initialized", "params": {}})
        send({"id": 2, "method": "skills/list", "params": {
            "cwds": [str(cwd)], "forceReload": True,
        }})
        return response(2)
    finally:
        try:
            process.stdin.close()
        except OSError:
            pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
        reader.join(timeout=1)
        process.stdout.close()


def assess(result: dict, cwd: Path, expected: dict[str, Path]) -> tuple[list[dict], int]:
    entries = result.get("data")
    if not isinstance(entries, list):
        raise ValueError("Unexpected skills/list schema: missing data array")
    entry = next((item for item in entries if isinstance(item, dict)
                  and isinstance(item.get("cwd"), str) and Path(item["cwd"]).resolve() == cwd), None)
    if entry is None or not isinstance(entry.get("skills"), list) or not isinstance(entry.get("errors"), list):
        raise ValueError("Codex returned no valid listing for the requested working directory")
    skills = entry["skills"]
    for skill in skills:
        if (not isinstance(skill, dict) or not isinstance(skill.get("name"), str)
                or not isinstance(skill.get("path"), str) or not Path(skill["path"]).is_absolute()
                or not isinstance(skill.get("enabled"), bool)):
            raise ValueError("Unexpected skill metadata in skills/list")
    rows = []
    for name, path in expected.items():
        named = [skill for skill in skills if skill["name"] == name]
        matching = [skill for skill in named if Path(skill["path"]).resolve() == path.resolve()]
        status = ("FOUND" if any(skill["enabled"] for skill in matching) else "DISABLED" if matching
                  else "OTHER_SOURCE" if named else "MISSING")
        other_sources = {str(Path(skill["path"]).resolve()) for skill in named
                         if Path(skill["path"]).resolve() != path.resolve()}
        rows.append({"name": name, "path": str(path), "status": status, "other_sources": len(other_sources)})
    return rows, len(entry["errors"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", action="append", default=[], help="catalog name; repeat as needed")
    selection.add_argument("--all", action="store_true", help="check every bundled top-level skill")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="project directory Codex should scan")
    parser.add_argument("--codex", default="codex", help="Codex CLI executable name or path")
    parser.add_argument("--timeout", type=float, default=30, help="total response timeout in seconds")
    args = parser.parse_args(argv)
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError("--timeout must be a positive finite number")
        cwd = args.cwd.expanduser().resolve()
        if not cwd.is_dir():
            raise ValueError("--cwd must be an existing directory")
        catalog = {item["name"]: item for item in load_catalog(ROOT)}
        names = list(catalog) if args.all else list(dict.fromkeys(args.skill))
        unknown = set(names) - catalog.keys()
        if unknown:
            raise ValueError("Unknown skill(s): " + ", ".join(sorted(unknown)))
        expected = {name: (ROOT / catalog[name]["path"] / "SKILL.md").resolve() for name in names}
        if any(not path.is_file() for path in expected.values()):
            raise ValueError("A selected skill package is missing from this checkout")
        executable = shutil.which(args.codex)
        if executable is None:
            raise ValueError("Codex CLI not found; use --codex /path/to/codex or check discovery in your host")
        rows, errors = assess(list_skills(executable, cwd, args.timeout), cwd, expected)
        print(f"Fresh Codex skills/list for {cwd}")
        for row in rows:
            print(f"{row['status']:12} {row['name']}: {row['path']}")
            if row["other_sources"]:
                print(f"             Also listed from {row['other_sources']} other source(s); inspect duplicate names in your host.")
        if errors:
            print(f"Codex reported {errors} discovery error(s); inspect its discovery UI for details.", file=sys.stderr)
        if errors or any(row["status"] != "FOUND" for row in rows):
            print("Discovery incomplete. Check selected links, disabled skills, and source paths; then refresh your agent.")
            return 1
        print("Selected manifests are enabled and listed from this checkout. No model task was run.")
        print("Refresh an existing agent session separately; listing does not prove workflow behavior or tool access.")
        return 0
    except (OSError, RuntimeError, ValueError, TimeoutError) as error:
        print(f"Discovery unavailable: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
