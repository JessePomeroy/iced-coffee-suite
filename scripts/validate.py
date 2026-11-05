#!/usr/bin/env python3
"""Check the portable distribution without installing skills or contacting services."""

import importlib.util
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from install import load_catalog


def main() -> int:
    errors = []
    catalog = load_catalog(ROOT)
    expected = {item["name"] for item in catalog}
    actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if expected != actual:
        errors.append(f"Catalog/package mismatch: {sorted(expected ^ actual)}")
    required = {"name", "path", "category", "use", "why", "requirements", "source", "license"}
    for item in catalog:
        if not required <= item.keys() or any(not isinstance(item[key], str) or not item[key].strip() for key in required):
            errors.append(f"Incomplete catalog metadata: {item['name']}")
        for name in item.get("subskills", []):
            if not (ROOT / item["path"] / "skills" / name / "SKILL.md").is_file():
                errors.append(f"Missing nested skill: {name}")
    skills = list((ROOT / "skills").rglob("SKILL.md"))
    names = set()
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"Missing frontmatter: {skill.relative_to(ROOT)}")
            continue
        match = re.search(r"^name:\s*['\"]?([a-z0-9]+(?:-[a-z0-9]+)*)['\"]?\s*$", parts[1], re.MULTILINE)
        if not match or not re.search(r"^description:\s*\S", parts[1], re.MULTILINE):
            errors.append(f"Invalid name/description: {skill.relative_to(ROOT)}")
            continue
        name = match.group(1)
        if name in names or name != skill.parent.name:
            errors.append(f"Duplicate or mismatched skill name: {skill.relative_to(ROOT)}")
        names.add(name)
        if not parts[2].strip():
            errors.append(f"Empty skill: {name}")
        if re.search(r"(?:/(?:home|Users)/[^/\s]+/|\.cache/codex-runtimes)", text):
            errors.append(f"Author-specific runtime path: {name}")
    licenses = ["bug-hunter/LICENSE", "punchlist/LICENSE", "find-skills/LICENSE",
                "impeccable/LICENSE", "21st-ui-build/LICENSE", "ux-audit/LICENSE",
                "unclaimed/LICENSE", "typesafe-ai/LICENSE", "testprune/LICENSE",
                "install-anti-slop/assets/anti-slop/LICENSE"]
    for filename in licenses:
        if not (ROOT / "skills" / filename).is_file():
            errors.append(f"Missing carried license: {filename}")
    forbidden = {"node_modules", "__pycache__", ".loop", ".loop-history", "sessions", "auth.json", "models-store.json", ".env"}
    for path in (ROOT / "skills").rglob("*"):
        if path.is_symlink():
            errors.append(f"Distribution symlink: {path.relative_to(ROOT)}")
        if path.name in forbidden or path.name == ".git":
            errors.append(f"Private/cache path: {path.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location("build_catalog", ROOT / "scripts/build_catalog.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = ROOT / "docs/CATALOG.md"
    if not output.is_file() or output.read_text(encoding="utf-8") != module.render():
        errors.append("Generated catalog is stale; run python3 scripts/build_catalog.py")
    for filename in ["README.md", "INSTALL.md", "SOURCES.md", "docs/SETUP.md", "docs/VERIFY.md", "docs/CATALOG.md"]:
        path = ROOT / filename
        for target in re.findall(r"\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            if ":" in target or target.startswith("#"):
                continue
            linked = path.parent / target.split("#", 1)[0]
            if not linked.exists():
                errors.append(f"Broken documentation link in {filename}: {target}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(catalog)} packages and {len(skills)} skill entrypoints; catalog and distribution checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
