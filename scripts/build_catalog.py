#!/usr/bin/env python3
"""Generate the human catalog from catalog.json."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render() -> str:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    lines = [
        "# Skill catalog", "",
        "Generated from `catalog.json` by `python3 scripts/build_catalog.py`. Do not edit directly.", "",
        "Choose skills that match your work. Installing a skill does not install its tools,",
        "authenticate an account, authorize paid calls, or grant permission to change external systems.", "",
        "| Skill | When to use it | Why | Requirements |",
        "| --- | --- | --- | --- |",
    ]
    for item in catalog["skills"]:
        cells = [f"[{item['name']}](../{item['path']}/SKILL.md)", item["use"], item["why"], item["requirements"]]
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |")
    lines.extend(["", "## Bug Hunter's nested skills", "",
                  "These travel with the parent package; the installer does not create duplicate top-level links.", ""])
    summaries = {
        "commit-security-scan": "Review the security effects of a particular commit, branch, or PR diff.",
        "doc-lookup": "Verify framework and library behavior with current documentation.",
        "fixer": "Apply explicitly authorized fixes for verified defects.",
        "hunter": "Find reachable defects with concrete triggers, consequences, and evidence.",
        "recon": "Map entrypoints, ownership, architecture, and trust boundaries.",
        "referee": "Resolve findings and objections against current evidence.",
        "security-review": "Assess security with threat-model and relevant dependency context.",
        "skeptic": "Challenge findings and investigate plausible counterevidence.",
        "threat-model-generation": "Map assets, boundaries, and threats using STRIDE.",
        "vulnerability-validation": "Establish reachability, exploitability, and practical impact.",
    }
    parent = next(item for item in catalog["skills"] if item["name"] == "bug-hunter")
    for name in parent["subskills"]:
        lines.append(f"- [{name}](../skills/bug-hunter/skills/{name}/SKILL.md): {summaries[name]}")
    lines.extend(["", "## Deliberately separate", "",
                  "Company integration (`client-site-integration`, `hubspoke-sync`), Pi history and",
                  "orchestration, Herdr control, and the author's printer-specific label workflow",
                  "remain outside this portable distribution. Official system skills and managed",
                  "plugins should be installed through their providers. See [sources](../SOURCES.md).", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = ROOT / "docs/CATALOG.md"
    expected = render()
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != expected:
            print("Catalog is stale. Run python3 scripts/build_catalog.py")
            return 1
        print("Catalog is current.")
        return 0
    output.write_text(expected, encoding="utf-8")
    print("Generated docs/CATALOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
