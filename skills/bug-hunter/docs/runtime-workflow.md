# Advanced runtime workflow

Load this for structured pipelines: canonical JSON or machine-consumed output,
resumable/runtime orchestration, security modes, complete-coverage loops, or the
Fixer pipeline. Lightweight peer reviews use the
[review-format guidance](../SKILL.md#choose-the-review-format); native-agent
delegation or a saved prose report alone does not require this runtime.
The [Svelte-first entrypoint](../SKILL.md)
remains the review lens; these contracts govern orchestration and authority.
Canonical role files live under `skills/`; `prompts/` are generated copies.
Paths below are relative to the skill root unless they name run artifacts.

## Flags and authority

Initialize all modes false, including `LOOP_MODE=false`, `FIX_MODE=false`,
`APPROVE_MODE=false`, `AUTONOMOUS_MODE=false`, and `AUTO_COMMIT=false`.

- `--loop` sets `LOOP_MODE=true`; `--no-loop` retains single-pass behavior.
- `--scan-only` / `--review` mean report-only.
- `--plan-only` / `--plan` produce strategy/plan, not edits.
- `--fix` / `--approve` / `--safe` enable reviewed fixing in the host's approval
  mode. They do not override repository scope or host permission controls.
- `--autonomous` explicitly allows eligible unattended fixes, not arbitrary
  refactors or production actions.
- `--dry-run` / `--preview` produce planned output without edits, locks, or commits.
- `--auto-commit` is separate and valid only with fixing enabled. Never stage
  outside validated scope or use `git add -A`.
- Contradictory read-only and mutation intent must not increase authority;
  reject it or retain the safer interpretation and explain.

PR selectors are `current`, `recent`, or a number; bare `--pr` and `--review-pr`
mean current, and `--last-pr` means recent. Use `scripts/pr-scope.cjs`; fail if
the base cannot be trusted. Branch `-b <branch> --base <base>` reviews
`<base>...<branch>`; this public branch form's default base remains `main`.
Staged review uses `git diff --cached` and the staged blobs. Empty scope is an
empty review, not a repository-wide fallback. Use the manifest triage interface
in the entrypoint; preserve its supported-source/context exclusions in reports.

## Preflight, modes, and delegation

Require Node 22+ and the needed role/runtime files. Choose an isolated output
directory according to the host/repository rules; do not overwrite another run
or commit `.bug-hunter` artifacts inadvertently. Before initializing runtime
state, run:

```bash
node "$SKILL_DIR/scripts/run-bug-hunter.cjs" preflight --skill-dir "$SKILL_DIR"
```

Use a supported runtime backend. `local-sequential` is valid; native host agent
tools can also be available independently of this CLI's process-backend probe.
Never invent unavailable tools, model tiers, or independent reviewers. For
structured pipeline delegation read `modes/dispatch.md` and
`templates/subagent-wrapper.md`; validate
payloads with `scripts/payload-guard.cjs`, then validate returned artifacts.

Preserve `triage.scanOrder`, `riskMap`, `domains`, `fileBudget`, and `needsLoop`.
Choose the corresponding `modes/single-file.md`, `modes/small.md`,
`modes/parallel.md`, `modes/extended.md`, `modes/scaled.md`, or
`modes/large-codebase.md`. Local execution uses `modes/local-sequential.md`.
Read a selected mode fully before using it, not every mode in advance.

Source chunks use combined estimated tokens of assigned files, default 48,000
unless explicitly overridden. Isolate an oversized file; don't hide it in a
mixed chunk. Large scope does not enable looping automatically. Report partial
coverage when one pass cannot cover the queue. Explicit looping requires
`modes/loop.md` or `modes/fix-loop.md` and its active driver. Continue until all
queued files reach terminal outcomes or a visible hard blocker/user stop; a
terminal failed file is not a successful review.

## Evidence and artifact integrity

Read `docs/precision-protocol.md` for fail-closed runtime details. In every structured mode:

- A worker may report findings only for its exact assigned source files.
  Context can explain a finding; it cannot silently enlarge writable scope.
- Canonicalize through real paths and enforce repository containment. Capture
  exact source hashes before dispatch and recheck before accepting findings,
  fact cards, or completion. Changed/deleted/unreadable source fails closed.
- Resume keeps its original source baseline; changed content is not silently
  adopted. A parent chunk marked done cannot manufacture file completion.
- Missing/invalid artifacts and failed role phases remain failed or unreviewed.
  Do not fill them with invented clean JSON. Keep bounded retries and fresh
  attempt outputs; runners need a real artifact-producing worker command.
- Findings lacking completed adjudication stay unreviewed/manual-review and
  cannot authorize remediation. Deduplication preserves the strongest evidence
  and useful cross-references, not inflated finding counts.

Canonical outputs under the run's `.bug-hunter/` include `triage.json`,
`recon.json`, `hunter-findings.json`, `skeptic.json`, `referee.json`,
`coverage.json`, and joined `scan-report.json`; render `report.md` as its human
view. Validate each schema-backed artifact using `scripts/schema-validate.cjs`.
The final report distinguishes confirmed, dismissed, manualReview, unreviewed,
failed/pending coverage, and required-verification failure.

## Optional evidence policies and verification

Read `docs/world-class-protocol.md` only for measurable/adaptive workflows.
`adaptive-plan.json`, `retrieval-plan.json`, content-addressed evidence-cache
facts, `benchmark-report.json`, and `verification-report.json` are bounded
evidence policies, never permission grants. Explicit caller settings take
precedence. Load direct evidence first and optional retrieval only within
budgets. Re-check exact current source before trusting cached facts.

When a verification plan is supplied/required, use the bounded hybrid verifier:
inert argv arrays, `shell:false`, repository containment, secret redaction, and
time/output limits. A required failure, timeout, or unavailable check fails
closed. Required verification failure prevents Fixer authorization. Follow
`docs/svelte-verification.md` when selecting meaningful Svelte checks.

## Security workflows

Read the selected bundled skill, not every security workflow:

- `--pr-security`: `skills/commit-security-scan/SKILL.md`; defaults current PR,
  dependency/STRIDE context, and report-only.
- `--security-review`: `skills/security-review/SKILL.md`; repository security
  context and report-only.
- `--threat-model`: `skills/threat-model-generation/SKILL.md`; generate/reuse
  native `threat-model.md` and related configuration within authorized scope.
- `--validate-security`: `skills/vulnerability-validation/SKILL.md`.
- `--deps`: `scripts/dep-scan.cjs --target <path> --output <run-path>`; current
  supported dependency parsing/reachability is JS/TS npm, pnpm, Yarn, and Bun
  lockfiles. Unsupported scanners are unresolved, not clean.

Security intent alone does not permit fixing, active attacks, or production
access. Threat-model assumptions must be checked against the SvelteKit request
and server-only boundaries actually used by the application.

## Fixing and development gates

With explicit authority, read `modes/fix-pipeline.md` and
`skills/fixer/SKILL.md`. Produce `fix-strategy.json`, `fix-plan.json`, immutable
`fixer-scope.json`, and `fix-report.json`. Only Referee-confirmed,
confidence-eligible `safe-autofix` entries in a validated rollout plan enter
automatic Fixer scope. Manual-review, larger-refactor,
architectural-remediation, conflicting, and report-only entries stay non-writable.
Escalate deliberate larger redesigns separately instead of relabeling them safe.

Preserve worktree, locks, canary, circuit-breaker, and rollback safeguards.
Requested isolation may not silently fall back to direct edits. Add regression
tests only within authorized paths. Dry runs stop before mutation; commits need
separate authority. A required gate, unsafe Git state, invalid payload, failed
review, or scope violation cannot be waived by a generated report.

For skill-source development, regenerate compatibility prompts with
`scripts/generate-compat-prompts.cjs` and run `pnpm quality:world-class`.
The bundled benchmark tests the protocol; it is not independent evidence of
Svelte detection accuracy or universal superiority. Evaluate new guidance with
blind, fresh-agent Svelte cases and report their actual limitations.
