# Verification

From the repository root:

```zsh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
```

The validator checks catalog coverage, required frontmatter, complete nested skill
entrypoints, carried licenses, generated catalog freshness, and the absence of
distribution symlinks and private/cache directories.

Installer tests use temporary homes and custom discovery directories. They cover
preview behavior, multiple agents, duplicate shared destinations, conflicts,
existing instructions, broken and changed links, rollback after a creation failure,
path containment, installation checks, and removal without source deletion.

## Package helper checks

The package scripts retain their own focused tests. Run a relevant suite after
changing helper behavior, using the appropriate installed environment:

```zsh
python3 -B -m unittest discover -s skills/pdf-reader/scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s skills/youtube-transcript/scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s skills/docx-tracked-changes/tests -p 'test_*.py' -v
```

The PDF suite needs Poppler and the DOCX suite needs `lxml` and `python-docx`.
Do not install those globally to force a pass. Missing prerequisites are reported
as unavailable verification. Transcript tests are offline; a real video request
would be a separate network check and would depend on caption availability.

For Bug Hunter's packaged runtime, Node.js 22+ supports:

```zsh
node skills/bug-hunter/scripts/run-bug-hunter.cjs preflight --skill-dir skills/bug-hunter
```

This distribution includes its runtime package, not the complete upstream release
development checkout. Its upstream `npm test`/release scripts can reference omitted
development resources; use the upstream project for release development.

## Actual agent discovery

`install.py --check` proves the selected link targets only. A fresh agent session,
its discovery UI, and an exercised skill are separate verification. Do not claim
all agents or optional paid services work from an installer unit-test pass.
