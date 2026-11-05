---
name: reflect
description: Review a completed task or explicitly selected history for recurring workflow failures and propose evidence-backed skill or tooling improvements. Use for retrospectives and requests to learn from a session; proposals are read-only by default.
---

# Reflect on completed work

Find a small number of durable improvements, not another list of universal rules.
Use the active conversation or user-selected tasks/history. Do not search unrelated
private transcripts or infer that old instructions authorize current changes.

## Establish evidence

Identify the intended outcome, observed actions, user corrections, failures,
recovery, and final verification. Cite actual messages, tool results, or source.
Separate repeated preferences from one-off constraints and duplicates/forked
prompts from independent evidence. A single serious demonstrated failure can
justify a proposal, but label its evidence honestly.

For selected Pi history, `analyze-pi-sessions` can provide scoped read-only retrieval.
For Codex tasks, use available task-reading tools. Neither is a required dependency:
if history access is unavailable, use a user-provided excerpt or report the limit.
Do not invent a transcript path or read broad archives merely to find a lesson.

## Choose the smallest durable correction

For each supported issue, decide whether it belongs in:
- a script, schema, lint, or runtime check that can enforce an invariant;
- a narrowly triggered existing skill or reference;
- a project-local instruction or feature map;
- a one-off task decision that should not become persistent policy.

First check whether the current instructions already cover it. A failure to follow
a good rule does not necessarily call for more rules. Retire conflicting/stale
wording instead of piling on exceptions. Consider false positives, lost flexibility,
additional tool calls, and maintenance costs. Do not infer effectiveness from prose
quality alone.

## Propose, then apply only with authority

Return the evidence, likely cause, exact target, proposed behavioral change, tradeoff,
and a realistic verification case. Separate recommendations, rejected ideas, and
uncertainties. Do not file tickets, message anyone, schedule work, or edit skills
merely because reflection found an improvement.

If the user already authorized named skill changes in this session, apply within
that scope using skill-creator guidance when available, validate affected resources,
and report actual checks. Otherwise stop at reviewable proposals. Independent
review is optional and requires delegation authority; local reflection is useful
without a mandatory panel.

Inspired by [Pstack's reflect workflow](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md), with local permission boundaries.
