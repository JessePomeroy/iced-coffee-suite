---
name: project-audit
description: Coordinate an evidence-backed audit of an existing project across code behavior, tests, security, user journeys, and architecture, using applicable installed skills and one consolidated report. Use for a full project audit or a scoped multi-discipline review; no repairs or delivery by default.
---

# Project audit

Audit an existing project through complementary skills, not a stack of duplicate
reports. Resolve the repository/path from the request or current project. Ask for
the target only when it cannot be determined unambiguously; never infer a project
from this skill's own location. Do not start auditing an unrelated checkout.

The default is report-only. No source/config/skill edits, test deletion, dependency
installation, automatic fixes, commits, PRs, deployment, publishing, or messages.
User-approved local verification may create task-owned scratch/results, but must
preserve existing tracked and untracked work and shared state. Production mutations,
active attacks, paid calls, and sending data to external services need appropriate
explicit authority. A complete audit is not a production certification.

## 1. Scope and inventory

Read project and nested instructions, Git state/revision, package/toolchain config,
supported entrypoints, application surfaces, data stores, integrations, CI/release
configuration, and existing tests/verification skills. Inspect secrets handling
without reading or printing secret values. Identify safe test data and whether
local runtime work can be isolated. Start no server just to inspect source.

Use `recon` for a bounded ownership/entrypoint map when available. Its Svelte lens
applies to Svelte; do not manufacture rune concerns for other stacks. Map omitted
packages and external dependencies as limits, not implicitly audited code.

Choose full or focused scope from the user request:
- **Full:** all applicable disciplines below across a declared domain/feature
  inventory, with risk-based deep checks and explicit sampling limits.
- **Focused:** the named subsystem, task, or diff plus necessary caller context.

Write a compact coverage plan: domain/feature, intended check, owner skill,
expected evidence, and known prerequisites. Full does not mean every possible
state or every line is proved correct. Do not silently reduce a full request to
one homepage or a file inventory. Process planned domains in bounded passes;
stop at blockers, explicit budget, cancellation, or scope completion, and show
unfinished coverage. Do not repeat hunts until no new findings appear.

## 2. Safe baseline

Inspect runner scripts, imports, fixtures, network access, and environment loading
before executing checks. Collection can have side effects. Run the relevant safe
existing type/lint/build/test checks, recording exact commands and revision.
Use the project's environment and package manager. Do not install dependencies,
run migrations, seed shared databases, or switch environments to force a baseline.
Record existing failures, missing dependencies, and unavailable checks separately.

Locate the project `verify-*` skill and feature map. Reuse its health/isolation
recipes. If none exists, use the supported harness that is already available.
Recommend `create-verification-skill` as a separate setup task; do not create or
repair a project harness during a report-only audit. A missing harness need not
block source review, but limits runtime claims.

## 3. Code, tests, and security

Load each selected skill's instructions when its phase starts. Reuse context and
evidence without claiming a second independent review for the same agent.

- **Code behavior — `bug-hunter`:** review each assigned domain and necessary
  callers for reachable failures. Use its Hunter/Skeptic/Referee reasoning and
  distinguish local passes from independent reviewers. Map full component behavior
  for Svelte; use general runtime/request-boundary analysis for other stacks.
  A triage/index entry is not a reviewed file. Do not enable fix or commit modes.
- **Tests — `testprune` in audit mode:** assess invariants, misleading tests,
  unsafe external calls, collection gaps, fixture costs, and test command/CI
  meaning. No removal, gate rewrite, or new test infrastructure in this phase.
- **Security — `security-review`:** inspect trust boundaries, authorization,
  sensitive data, and relevant dependency reachability. Reuse a verified threat
  model or build the required context within the audit's authorized output scope.
  Apply `vulnerability-validation` to serious candidates; benign local proof is
  preferred, and unavailable exploitability evidence remains unresolved.

Security workflow artifact paths refer to the run's isolated `.bug-hunter/`, not
permission to write into the source repository. Follow Bug Hunter's runtime
workflow for structured outputs and canonical filenames/schemas. Use an explicit
source target and isolated output root. If a helper cannot separate these or
requires unapproved access, report the capability gap rather than bypassing it.
Resolve helper paths against the installed skill bundle, not the project cwd.

Check available dependency scanner support for the actual lockfile/language.
An unsupported scanner or unavailable/current advisory lookup is not a clean
result. Do not upload source, lockfiles, or dependency inventories to a service
without appropriate authority. Public documentation/advisory research must follow
the host's allowed retrieval tools and privacy rules.

## 4. User-facing and runtime verification

For an app with a UI, use `ux-audit` with the matching declared scope and its
project feature map. Use `web-debug` to investigate specific failing interactions,
not to duplicate the entire walkthrough. Cover relevant keyboard/focus, responsive
layout, errors/recovery, and persistence with actual interaction evidence.
Measure performance only through supported tooling; unmeasured is not zero.

For APIs, CLIs, libraries, or workers, exercise supported request/command/consumer
boundaries with existing safe fixtures. UI-only checks are not applicable, not a
reason to force a browser or mark the entire project failed. Deployment smoke
checks must target an authorized environment and remain within its permissions.

Maintain one driver per shared instance and clean up only task-owned resources.
If auth, browser capability, or safe fixtures are missing, retain completed source
findings and mark the affected runtime coverage incomplete.

## 5. Architecture and optional design review

Use `codebase-design` and `improve-codebase-architecture` in review/design-only
mode to assess observed ownership, coupling, caller complexity, and testability
friction. Prioritize actual hotspots and evidence from earlier phases; do not
produce speculative redesigns for every module. Keep improvement proposals
separate from verified defects.

Use `blast-radius` when there is an actual proposed change, pending diff, or named
migration whose downstream effects need review. Do not invent a diff to make it
fit an audit of the current system.

Visual hierarchy, usability, and accessibility observations belong in the live
UX phase. A separate Impeccable critique is optional when design judgment is part
of the request; follow its actual read-only/permission protocol and disclose any
unavailable required detector or independent assessment. Do not silently run its
setup/repair operations or force its full critique for every technical audit.

**Punchlist is opt-in only:** invoke it when the user specifically requests its
named-defect inspection. Preserve its current critic, coverage, privacy, and
verification protocol; this wrapper does not implement the proposed bounded mode.
If its required independence cannot run under the user's delegation permissions,
report that phase blocked or obtain the required choice. Never simulate its panel.

## 6. Reconcile once and report

Join phase outputs by root cause and affected behavior, preserving evidence and
all affected paths. Recheck apparent contradictions against current source. Use
`vulnerability-validation` for security reachability and `diagnosing-bugs` for a
specific unresolved failure when the needed probe remains in audit scope.
Do not reinterpret an uncertain claim as confirmed just because several tools
reported it. A source change mid-audit invalidates affected evidence; record the
revision mismatch and recheck that portion or report it incomplete.

Return one report:
- Target/revision, scope, applicable disciplines, and declared exclusions.
- Confirmed findings ordered by demonstrated impact, with trigger, expected and
  observed result, source/evidence, and a scoped correction direction.
- Architecture/design/test-maintenance recommendations, clearly separate.
- Unresolved hypotheses and the exact evidence needed to decide them.
- Coverage by domain and check: exercised, not applicable, or not assessed.
- Actual commands/interactions, baseline failures, and verification limits.
- Prioritized next actions and dependencies, without implementing them.

Report completion within the declared scope separately from issues found.
Incomplete coverage cannot become a clean bill of health. Do not issue a global
numerical quality grade or pad a fixed finding count. Use in-chat output by default;
save a report when requested and keep structured run artifacts in task-owned
scratch. Repository-owned report files need that write scope.

## Coordination and next steps

Multiple skills do not imply multiple agents. Run sequentially by default and
reuse the domain map. Delegate only when the user or applicable project authority
permits it, with disjoint scopes and explicit output ownership. Read each required
phase's skill; never claim it ran because its name appeared in the plan. If a skill
is absent, report the gap and use an honest equivalent review when possible,
without installing a plugin or pretending that skill's protocol completed.

Repairs, verification-harness creation, lint installation, and maintenance edits
are separate follow-ups. Use `fixer` for explicitly approved confirmed repairs,
`babysit` only for authorized delivery through merge, and `reflect` only when a
retrospective is requested. A project audit never auto-ships its findings.
