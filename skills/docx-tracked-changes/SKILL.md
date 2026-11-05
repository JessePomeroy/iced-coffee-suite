---
name: docx-tracked-changes
description: Report, accept, or reject inline tracked revisions in a local DOCX using a tested helper that preserves restored text. Use for resolving Word insertions, deletions, and moved text; use an available document workflow for editing and final rendering.
---

# DOCX tracked changes

Use this skill's `scripts/accept_tracked_changes.py` for revision resolution.
It handles `w:ins`, `w:del`, `w:moveTo`, and `w:moveFrom` in
`word/document.xml`. Rejecting a deletion restores ordinary `w:t` text, including
whitespace and run formatting. Other ZIP parts stay unchanged, apart from disabling
tracking in `word/settings.xml` unless `--keep_tracking_on` is supplied.

Resolve `DOCX_SKILL_DIR` to the directory containing this installed `SKILL.md`.
Use the project's existing Python environment with `lxml`; set `DOCX_PYTHON` to
that interpreter. No particular agent's artifact runtime is required. Do not
install packages globally to make this skill work.

```zsh
"$DOCX_PYTHON" "$DOCX_SKILL_DIR/scripts/accept_tracked_changes.py" input.docx --mode report
"$DOCX_PYTHON" "$DOCX_SKILL_DIR/scripts/accept_tracked_changes.py" input.docx --mode reject --out rejected.docx
"$DOCX_PYTHON" "$DOCX_SKILL_DIR/scripts/accept_tracked_changes.py" input.docx --mode accept --out accepted.docx
```

Inspect the report and use the requested accept/reject decision; clarify only when
the decision is missing. A report-only request creates no output. Preserve the
source; choose a new output path. The helper refuses existing outputs and
input/output aliases. When an available document workflow imposes additional authoring requirements,
follow those requirements before mutation.

Reopen the result, verify expected text and revision counts, and use an available
document renderer for visual inspection and final delivery. If no renderer is
available, report that limitation. XML counts
or text extraction alone do not establish layout fidelity.

This is not a complete Word revision engine. Headers, footers, formatting changes,
paragraph/table revisions, field revisions, and move-range markers require separate
assessment. A zero count here covers only the supported main-part revision wrappers.
Keep unsupported changes and incomplete verification explicit.

The helper requires Python 3 and `lxml`. Regression tests also require `python-docx`:

```zsh
"$DOCX_PYTHON" -B -m unittest discover -s "$DOCX_SKILL_DIR/tests" -p 'test_*.py' -v
```

See [provenance](PROVENANCE.md) for the implementation and regression-test origins.
