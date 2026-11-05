---
name: maintain-verification-skill
description: Check and, when requested, repair a project's verification instructions, driver helpers, and feature map against source and live behavior. Use for verification drift or maintaining a verify-app skill.
---

# Maintain project verification

Keep a project verification skill trustworthy as the app changes. A review or
status request is read-only. A request to maintain/update authorizes scoped edits
to the verification skill and its owned helpers, not product changes, PR creation,
commits, deployment, or scheduling.

Locate the project skill with launch/drive/proof instructions and its feature map.
If several materially different targets match, resolve the requested app before
editing. If none exists, explain the gap and suggest creating one; do not silently
invent a new app harness during an audit.

## Select coverage

Read project instructions, current diff/revision, map index, and relevant recent
changes. A targeted request covers affected features and neighboring shared
behavior. An unqualified maintenance pass covers the map's current entries; name
that inventory and report gaps rather than claiming completion from a sample.
Do not expand to every theoretical feature or loop until no changes are found.

Inspect feature source and actual callers to identify likely drift, missing
prerequisites, broken links, or new surfaces relevant to the map. Source is a plan
for the live check, not proof of runtime behavior. Read the mapped driver recipe
and health-check the intended test instance before using it.

## Reconcile against live behavior

Exercise each in-scope reachable feature through its real entry points. Record
expected and observed outcomes, evidence, and not-assessed checks. Use one driver
for a shared UI instance; delegate only when authorized, with isolated instances
for parallel driving. A local pass is sufficient by default.

Separate these cases:
- Documentation drift: the implementation and intended contract changed; update
  the map within edit authority and verify the new recipe.
- Harness gap: supported behavior cannot be driven by the existing helper; make
  a scoped helper correction and exercise it before calling it repaired.
- Product defect: behavior violates the intended contract; report it without
  rewriting the expected result to bless the regression.
- Access/environment blocker: identify the missing prerequisite and preserve
  completed evidence. Unreachable is not verified-correct.

After unexpected behavior, recheck health and recover to known state. Clean up
failed-run residue and task-owned processes, retaining proof. No blanket retries,
process-name kills, personal cookie acquisition, or production resets.

## Finish

Return **current**, **updated**, or **incomplete**, with coverage and any confirmed
product defects reported separately. A source-only pass is incomplete for requested
live verification. Report edits, exercised recipes, proof paths, and unresolved
work. Do not open a PR or create an automation without that explicit request.

Inspired by [Pstack's maintenance skill](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md).
