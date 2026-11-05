---
name: testprune
description: Audit or improve a slow, noisy, redundant, or unsafe test suite while preserving supported behavior and offline verification. Use for test-suite cleanup, stale tests, paid-service leakage, or scoped follow-up work.
argument-hint: [audit|direct|prompt-first|followups]
disable-model-invocation: true
metadata:
  version: "1.3.0"
---

# Testprune

Make verification trustworthy and useful at the project's real boundaries.
A request to audit/review is read-only. `direct` applies scoped cleanup when
requested; `prompt-first` drafts a repo-specific plan and stops; `followups`
addresses only named, authorized deferred items. With no clear edit request,
use audit mode. Mode labels do not expand mutation or external authority.

## Inspect before running

Read applicable repository/nested instructions, runner configuration, package
scripts, lockfiles, and current Git state using actual tool calls. Record the
current revision and unrelated dirty/untracked files. Preserve them; do not
stage anything unless committing/staging is requested. Use the repository's
supported toolchain, environment, and package manager, not a global interpreter
merely because it appears first on PATH.

Trace supported production entrypoints and relevant feature flags. A project can
have multiple supported paths. Tests of historical data, migrations, refusal,
and public compatibility remain meaningful even when old producers are retired.
Neither a red test nor current implementation alone establishes intended behavior.
Resolve stale assertions against documented contracts, callers, and history.

Inspect test-side external boundaries before execution or collection: imports,
configuration loading, fixtures, email, databases, paid providers, and deploy
helpers. Never print credential values. A collect-only command can execute imports.
Run only checks known to be offline and isolated; otherwise state the limitation.

## Inventory and classify

Resolve `scripts/test_inventory.py` relative to this skill and invoke it with
`--root <repository>` using an available Python interpreter. It compares candidate
files on disk with Git tracking/ignore state. It is a heuristic, not the runner's
collection result; inspect custom naming, generated tests, inline tests, configured
roots, and exclusions. Pass `--dir` or repeated `--pattern` when appropriate.

Use the runner's supported collection/timing commands when safe. For pytest,
`--durations` is available; do not pass pytest flags to Vitest, Jest, Go, or Cargo.
Record commands, environment, observed counts, time, and failure categories.

Classify by the behavior each test proves: supported coverage, duplicate invariant,
obsolete expectation, retired implementation, environment dependency, or unsafe
external call. For every removal candidate, identify its invariant and demonstrate
that it is obsolete or retained elsewhere. Failing, old, or slow is not sufficient
reason to delete a test.

## Scoped cleanup when authorized

- Retarget meaningful invariants before removing their former tests. Do not alter
  product behavior just to satisfy a stale expectation.
- Investigate actual waits and fixture costs. Replace test-side waits only while
  preserving retry, cancellation, ordering, and fallback assertions.
- Prove offline boundaries reject external calls; a test name or missing key is
  not a safety guarantee. Do not add live calls to verify the fence.
- Preserve unrelated modifications. Delete a tracked test only within authorized
  removal scope, retaining its base revision and rationale. Preserve untracked
  user work unless specifically authorized; do not silently archive it.
- Follow existing runner selectors/markers for focused checks. Add a new gate
  only if it solves a demonstrated need. Prefer existing scripts over a parallel
  runner, and retain the meaning of the default test command.
- A request to change the default gate must include review of CI/release callers
  and their assertions so full validation is not silently weakened.
- Keep configuration, documentation, and test references synchronized with scoped
  changes. Do not create CLAUDE.md or duplicate AGENTS.md content by default.

Run changed tests, relevant neighboring coverage, and broader checks justified by
shared fixture/config changes. Re-run after substantive changes or failures, not
by ritual. Do not skip required checks because a fixed run-count was exhausted.
Report pre-existing failures separately from regressions and unresolved intent.

## Boundaries and handoff

Keep code-model, production, dependency, and security changes outside test cleanup
unless explicitly included. Stop at the agreed scope/budget and identify remaining
work; do not run to an arbitrary two-hour limit. Delegate only when authorized,
with disjoint edit ownership and independent useful work.

Report what changed, preserved invariants, measured before/after on comparable
checks, remaining failures, and unavailable verification. A narrower fast check
is not a speedup of the full suite. Commit/push/PR actions remain separate.

Read these only for their relevant mode:
- `references/prompt_creator.md`: requested plan/prompt handoff.
- `references/followups_execution.md`: conflicting intent or deferred items.
- `references/techniques.md`: inventory, timing, offline fences, and gate changes.
- `references/gate_script_template.sh`: optional pytest gate example to adapt.
- `references/agent_instruction_block.md`: requested testing documentation.
- `references/final_report.md`: concise result format.
- `references/rationale_and_pitfalls.md`: preservation and classification rationale.
