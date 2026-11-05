---
name: improve-codebase-architecture
description: Review architectural friction in a named module or changing area, compare caller-first interface designs, and recommend a scoped improvement. Review and design requests remain read-only.
disable-model-invocation: true
---

# Improve codebase architecture

Find a concrete maintenance or correctness problem and design the smallest
change that improves it. A design conversation does not authorize implementation,
CONTEXT.md edits, ADR creation, or external actions.

## Ground the review

Read project instructions, current changes, relevant domain documentation and
ADRs. If the user names a target, stay there. Otherwise use recent changes and
reported friction to choose a bounded area. Trace real callers, ownership,
lifetimes, invariants, and available verification before suggesting abstractions.

Use the installed `codebase-design` skill when its deep-module vocabulary helps;
read its SKILL.md through the host's file tools. There is no required generic
Skill API and no dependency on grilling or domain-modeling skills. Existing
project terminology takes precedence over a preferred architecture vocabulary.

Separate observed friction from anticipated benefit. A wrapper or small module
is not a defect just because it is thin. State what becomes easier or safer for
a caller or maintainer, and what the change costs.

## Compare designs

Write a representative caller usage example first. Derive the necessary types,
operations, error behavior, configuration, and ownership from that example.
For a material design choice, compare structurally distinct alternatives,
including keeping the current design when reasonable. Small, clear changes
need one grounded proposal, not a mandatory design tournament.

Evaluate the alternatives against the actual constraint: behavior, caller
complexity, locality, runtime cost, migration effort, and verification. Identify
which invariants existing tests protect and how they remain covered. A new
integration test does not automatically replace focused unit tests.

Give a recommendation with a concise rationale and unresolved product decisions.
Use an inline diagram or table if useful; a separate HTML report is optional,
not a required detour. If requested, `HTML-REPORT.md` offers presentation examples;
use the host's artifact tools and keep third-party resources out of private reports.

## Implementation boundary

For review/design-only work, stop with the recommendation and verification plan.
Ask only about a material choice that evidence cannot settle. Do not turn every
minor interface decision into a question or update domain docs during discussion.

When implementation is authorized, make the scoped change using the chosen sketch,
preserve unrelated edits, and run relevant checks. Revisit the design if callers
repeatedly need workarounds; do not redesign for every incidental detail.
Record documentation changes only when they are part of the authorized work.

For explicitly requested parallel design exploration, use
`codebase-design/DESIGN-IT-TWICE.md` from the installed skill directory. Otherwise
compare alternatives locally. Never describe a local reconsideration as an
independent review.

## Handoff

Explain the friction, traced evidence, proposed caller experience, alternatives,
migration/verification plan, and any decision needed. If implemented, report the
actual diff and checks rather than presenting the design sketch as proof.
