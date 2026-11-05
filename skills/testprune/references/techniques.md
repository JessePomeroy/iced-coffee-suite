# Runner-aware techniques

## Inventory

Use the bundled Python helper as a disk/Git candidate inventory, then compare
with safe runner collection. Custom roots, hidden directories, inline tests,
generated cases, and naming patterns need explicit attention. Do not equate
ignored with excluded. Inspect hooks/import effects before collect-only runs.

## Timing

Use the project's supported command and environment. For pytest, request durations;
for other runners, use their installed version's reporting/profiling capability.
Record elapsed time and environment, separating setup, waits, and actual execution.
A fake clock must preserve retry/cancellation semantics, not merely erase sleeps.

## Offline fences

Inspect configuration and fixture import paths. Stub or deny the actual I/O boundary
and assert no requests escape. Use disposable local state and scoped environment
variables. Do not read/print .env values or call a provider to prove the fence.

## Gate changes

Prefer the existing runner's selectors. Keep focused and broad purposes explicit.
When asked to change a default command, inspect every CI/release/operator caller
and update its expectation with the same change. Run the affected orchestration
checks. Do not silently weaken strict release profiles.

## Removal

Before deleting an authorized tracked test, inspect its invariant, references,
and replacement coverage; retain the recoverable base revision. Preserve dirty
and untracked user work. Review the final diff. Stage/commit only when requested,
using explicit paths/hunks and preserving unrelated staged content.
