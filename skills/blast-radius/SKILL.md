---
name: blast-radius
description: Trace what a proposed or existing change could break beyond its diff, including callers, data formats, configuration, and lifecycle behavior. Use for impact analysis or asking what else a change affects; read-only by default.
---

# Blast-radius review

Identify concrete downstream consequences and the assumptions on which a change's
safety depends. This is an impact review, not authority to fix, commit, or ship.
Use existing safe checks; a review request does not permit product edits or new
persistent tests. Temporary offline probes are appropriate only within the host's
read-only/verification rules, with no external or production mutation.

## Trace the change

Resolve the exact diff/base/head or proposed behavior and relevant instructions.
Read changed code with callers and safeguards. Trace what symbol search misses:
serialized fields, stored rows, migrations, environment defaults, feature flags,
other languages/services, asynchronous ordering, teardown, and reused UI state.
Inspect pinned library behavior when a conclusion depends on it. Don't invent
consumers, treat all configuration as supported, or equate grep coverage with
execution coverage. Name unavailable cross-repository context.

State the few assumptions that materially determine safety. For each, distinguish:
source evidence, a traced reachable/unreachable path, an executed check, and a
live user-flow observation. Choose the cheapest meaningful available proof; mark
unproven assumptions rather than forcing a script that tests a proxy.

Use a project verification skill/feature map to select affected journeys when
available. Otherwise use existing project tests or documented operations.
Dynamic proof is especially useful for timing, persistence, library semantics,
and rendered behavior. If unavailable, report the source-supported conclusion
and the exact verification gap instead of declaring safe.

## Report

Explain the behavioral change, safety assumptions and evidence, confirmed risks,
checked-and-cleared concerns, and remaining uncertainty. Each risk needs a reachable
trigger and consequence. Distinguish potential risk from an established defect;
avoid invented probability percentages. Recommend the smallest useful regression
check without adding it unless test changes are authorized.

Keep the review bounded by the requested change and necessary dependencies.
For a large review, use independent agents only when authorized, with clear read
scopes. Agreement between agents is not a substitute for tracing the boundary.

Inspired by [Pstack's blast-radius review](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md).
