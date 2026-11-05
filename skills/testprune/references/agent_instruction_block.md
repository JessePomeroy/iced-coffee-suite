# Document test commands where the project already does

Update the existing testing guide or relevant instruction section only when the
cleanup changes its documented behavior. Preserve unrelated text and distinct
host-specific instructions. Do not create or synchronize CLAUDE.md and AGENTS.md
as a default action. Read-only audits only propose documentation edits.

Include actual supported commands, environment prerequisites, what each check
covers, measured runtimes when useful, and explicit isolation/live-test boundaries.
Retain the default command's meaning unless changing it was requested. Explain
known failures without labeling them passes. Avoid a blanket prohibition on broad
tests or an arbitrary seconds-per-test requirement.
