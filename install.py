#!/usr/bin/env python3
"""Preview or manage selected skill links without replacing existing files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
AGENTS = {
    "codex": (".agents/skills", ".codex/AGENTS.md"),
    "claude": (".claude/skills", ".claude/CLAUDE.md"),
    "gemini": (".agents/skills", ".gemini/GEMINI.md"),
    "pi": (".pi/agent/skills", ".pi/agent/AGENTS.md"),
}


@dataclass(frozen=True)
class Link:
    source: Path
    destination: Path


def absolute(path: Path) -> Path:
    # Resolving the destination itself would follow the link we must inspect.
    return Path(os.path.abspath(path.expanduser()))


def load_catalog(root: Path = ROOT) -> list[dict]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog.get("version") != 1 or not isinstance(catalog.get("skills"), list):
        raise ValueError("Unsupported catalog format")
    names = set()
    for item in catalog["skills"]:
        name = item.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("Invalid skill name in catalog")
        if name in names or item.get("path") != f"skills/{name}":
            raise ValueError(f"Invalid or duplicate catalog entry: {name}")
        names.add(name)
    return catalog["skills"]


def make_links(
    root: Path,
    home: Path,
    names: list[str],
    agents: list[str],
    skills_dirs: list[Path],
    instructions: Path | None = None,
    instructions_target: Path | None = None,
    remove: bool = False,
    codex_compat: bool = False,
) -> list[Link]:
    if codex_compat and ("codex" not in agents or not names):
        raise ValueError("--codex-compat requires --agent codex and selected skills")
    catalog = {item["name"]: item for item in load_catalog(root)}
    unknown = set(names) - catalog.keys()
    if unknown:
        raise ValueError("Unknown skill(s): " + ", ".join(sorted(unknown)))
    home = absolute(home)
    skill_roots = [home / AGENTS[agent][0] for agent in agents]
    if codex_compat:
        skill_roots.append(home / ".codex/skills")
    skill_roots.extend(absolute(path) for path in skills_dirs)
    links = []
    for name in dict.fromkeys(names):
        source = (root / catalog[name]["path"]).resolve()
        if not source.is_relative_to((root / "skills").resolve()):
            raise ValueError(f"Skill source escapes this repository: {name}")
        if not remove and not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing skill package: {name}")
        links.extend(Link(source, directory / name) for directory in skill_roots)
    if instructions is not None:
        source = absolute(instructions).resolve()
        if not remove and not source.is_file():
            raise ValueError(f"Instructions must be an existing personalized file: {source}")
        targets = [home / AGENTS[agent][1] for agent in agents]
        if instructions_target is not None:
            targets.append(absolute(instructions_target))
        links.extend(Link(source, target) for target in targets)
    destinations: dict[Path, Link] = {}
    for link in links:
        destination = absolute(link.destination)
        if destination == link.source or (not destination.is_symlink() and destination.resolve() == link.source):
            raise ValueError(f"Source and destination are the same location: {destination}")
        physical_destination = destination.parent.resolve() / destination.name
        if physical_destination in destinations and destinations[physical_destination].source != link.source:
            raise ValueError(f"Two sources would use the same destination: {destination}")
        if link.source.is_dir() and destination.parent.resolve().is_relative_to(link.source):
            raise ValueError(f"Destination would be inside its own skill package: {destination}")
        destinations[physical_destination] = Link(link.source, destination)
    ordered = list(destinations.values())
    for link in ordered:
        if any(other.destination in link.destination.parents for other in ordered):
            raise ValueError(f"Install destinations overlap: {link.destination}")
    return ordered


def points_to(link: Link) -> bool:
    if not link.destination.is_symlink():
        return False
    target = Path(os.readlink(link.destination))
    if not target.is_absolute():
        target = link.destination.parent / target
    try:
        return target.resolve() == link.source
    except (OSError, RuntimeError):
        return False


def state(link: Link, remove: bool = False) -> str:
    if points_to(link):
        return "remove" if remove else "present"
    if link.destination.is_symlink() or link.destination.exists():
        return "conflict"
    if remove:
        return "absent"
    for parent in link.destination.parents:
        if parent.exists() or parent.is_symlink():
            if not parent.is_dir():
                return "conflict"
            break
    return "create"


def apply_links(links: list[Link], remove: bool = False) -> None:
    if any(state(link, remove) == "conflict" for link in links):
        raise ValueError("Conflicts found; no links changed. Compare and merge existing configuration manually.")
    created: list[Link] = []
    try:
        for link in links:
            current = state(link, remove)
            if current == "conflict":
                raise ValueError(f"Destination changed during installation: {link.destination}")
            if current == "remove":
                # Check again immediately before unlinking; never follow or delete the target.
                if not points_to(link):
                    raise ValueError(f"Link target changed: {link.destination}")
                link.destination.unlink()
            elif current == "create":
                link.destination.parent.mkdir(parents=True, exist_ok=True)
                link.destination.symlink_to(link.source, target_is_directory=link.source.is_dir())
                created.append(link)
    except (OSError, ValueError):
        # Roll back only links created by this attempt. Empty parent directories may remain.
        for link in reversed(created):
            if points_to(link):
                link.destination.unlink()
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list bundled top-level skills")
    parser.add_argument("--agent", action="append", choices=AGENTS, default=[], help="repeat for multiple agents")
    parser.add_argument("--skills-dir", action="append", type=Path, default=[], help="custom discovery directory")
    parser.add_argument("--codex-compat", action="store_true",
                        help="also link selected Codex skills into ~/.codex/skills")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--skill", action="append", default=[], help="select a catalog name; repeat as needed")
    selection.add_argument("--all", action="store_true", help="explicitly select every top-level package")
    parser.add_argument("--instructions", type=Path, help="existing personalized global instructions to link")
    parser.add_argument("--instructions-target", type=Path, help="custom global instruction destination")
    parser.add_argument("--remove", action="store_true", help="remove only selected links with matching targets")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="apply the displayed plan; default is preview only")
    mode.add_argument("--check", action="store_true", help="check selected links without changing them")
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog()
        if args.list:
            if any((args.agent, args.skills_dir, args.skill, args.all, args.instructions,
                    args.instructions_target, args.apply, args.remove, args.check, args.codex_compat)):
                parser.error("--list must be used by itself")
            for item in catalog:
                print(f"{item['name']}: {item['use']}")
            return 0
        if args.remove and args.check:
            parser.error("--remove and --check cannot be combined")
        if args.instructions_target and not args.instructions:
            parser.error("--instructions-target requires --instructions")
        if not args.agent and not args.skills_dir and not args.instructions_target:
            parser.error("choose --agent, --skills-dir, or --instructions-target")
        names = [item["name"] for item in catalog] if args.all else args.skill
        if not names and not args.instructions:
            parser.error("select --skill, --all, or --instructions")
        if names and not args.agent and not args.skills_dir:
            parser.error("selected skills need --agent or --skills-dir")
        if args.instructions and not args.agent and not args.instructions_target:
            parser.error("instructions need --agent or --instructions-target")
        links = make_links(ROOT, Path.home(), names, args.agent, args.skills_dir,
                           args.instructions, args.instructions_target, args.remove, args.codex_compat)
        states = [state(link, args.remove) for link in links]
        for link, status in zip(links, states):
            print(f"{status.upper():8} {link.destination} -> {link.source}")
        if "conflict" in states:
            print("Conflicts found; no links changed. Existing files and other links are preserved.", file=sys.stderr)
            return 1
        if args.check:
            if all(status == "present" for status in states):
                print("Selected links match. Agent discovery is a separate check; see docs/VERIFY.md.")
                return 0
            print("Some selected links are missing.", file=sys.stderr)
            return 1
        if args.apply:
            apply_links(links, args.remove)
            print("Removal complete; source files were preserved." if args.remove else
                  "Installation complete. No dependencies or account settings were changed.")
        else:
            print("Preview only; no files changed. Add --apply to execute this plan.")
        return 0
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
