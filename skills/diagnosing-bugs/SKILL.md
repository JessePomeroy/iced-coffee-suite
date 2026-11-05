---
name: diagnosing-bugs
description: Diagnose a reported defect or performance regression using a concrete symptom, discriminating evidence, and the smallest useful reproduction. Fix only when requested.
---

# Diagnose a bug

Establish what fails, why, and what evidence supports the conclusion. A diagnosis
request permits investigation, not product edits. An authorized fix includes
relevant verification; commit, deployment, and production instrumentation need
their own authority.

## Establish the symptom

Read project instructions, relevant context/ADRs, versions, and current changes.
Record expected behavior, actual behavior, environment, input/account state,
and the triggering sequence. Preserve the original evidence before changing
caches, login state, flags, or timing. Redact secrets from captures and output;
use test data and environment references instead of printing credentials.

Prefer an existing project verification skill or test harness. For browser
behavior, use available browser tools and the actual user interaction. For
services or CLIs, use the real request/command boundary. Do not call an internal
setter and claim to have verified a user flow.

## Build evidence and a feedback loop together

Read source, traces, logs, and callers to form a working explanation and choose
the next probe. Investigation may be necessary to construct a reproduction;
absence of an executable repro is not a reason to stop reading evidence.

Use the narrowest check that can distinguish the reported failure from correct
behavior: an existing test, request, command, browser sequence, or captured
trace replay. Improve its speed and determinism when that helps, but a slow
integration check is valid when the boundary requires it. Minimize only enough
to isolate the cause without losing the real caller pattern.

For intermittent failures, record attempts, failures, timing, seed, and relevant
environment. Compare before and after under equivalent conditions. A few green
runs do not prove a rare race is gone. For performance, collect a baseline and
repeat measurements with the same method; distinguish noise from a measured win.

State the leading hypothesis and its predicted observation. Keep alternatives
when evidence is ambiguous; do not invent a fixed number of explanations for an
obvious failure. Choose probes that distinguish alternatives, change one relevant
variable at a time, and revisit the premise after repeated contradictory results.

Use a debugger, targeted traces, or uniquely tagged temporary logs. Avoid broad
payload dumps. Run production probes only within explicit authority; missing
access calls for a specific evidence request, not a bypass.

## Correct and verify when authorized

Trace the symptom to its owner and fix the smallest complete cause. A practical
regression test should fail for the reported reason before the fix and pass after.
Do not create brittle mocks or restructure the application solely to produce a
unit test; a repeatable integration or browser check may be the appropriate proof.
Run the original scenario after the correction and relevant nearby checks.

Separate an observed fix from a proposed correction that cannot be exercised.
Remove temporary instrumentation, retain sanitized proof, and stop only processes
started for this task using recorded identities. Never weaken assertions or hide
errors to make the result green. Record the causal explanation in the handoff;
include it in a commit/PR only when that action is authorized.

## Report one of these outcomes

- **Reproduced:** name the failing scenario and evidence. If repaired, also name
  the passing check and its scope; reproduction alone does not mean fixed.
- **Evidence-supported diagnosis:** explain the source/trace chain, remaining
  uncertainty, proposed correction, and the check needed to verify it.
- **Unresolved:** show the competing explanations, attempted probes, and smallest
  missing evidence or access needed to distinguish them.

Stop expanding when the scoped diagnosis or verified fix is complete. When the
next useful probe needs unavailable access or exceeds scope, report that limit.
For a human-operated reproduction, the optional `scripts/hitl-loop.template.sh`
can organize observations; inspect and adapt it before use.
