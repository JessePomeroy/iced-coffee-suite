# Maintaining Iced Coffee Suite

This repository distributes portable skill packages and a symlink installer.
This file guides repository maintenance; `instructions/AGENTS.example.md` is the
template for users' global working agreements. Do not install this file globally.

- Preserve complete runtime packages, nested skills, source attribution, licenses,
  and existing invocation policies. Keep optional host metadata optional.
- Resolve helpers relative to the installed SKILL.md, never an author's home path.
- Keep reviews read-only and require explicit authority for fixes and external actions.
- Never install into the maintainer's real discovery paths during verification.
  Exercise apply/remove behavior in temporary directories.
- The installer uses the Python standard library. Do not add a dependency merely
  to read frontmatter, create links, or run tests.
- `catalog.json` owns catalog metadata. Generate `docs/CATALOG.md` using
  `python3 scripts/build_catalog.py`; do not edit generated catalog output.
- Keep `SOURCES.md` honest about local editions and incomplete upstream provenance.
  Do not blanket-relicense third-party packages.
- Verify scoped changes with `python3 scripts/validate.py` and
  `python3 -B -m unittest discover -s tests -v`. Run affected package checks when
  modifying its helper code. Do not run live paid-service calls as tests.
- Preserve unrelated changes. Commits, pushes, PRs, and publication need the user's
  explicit request; creating this local repository does not authorize publishing it.
