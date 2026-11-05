# Audit handoff

Lead with whether the scoped user task worked and what prevents it from working.
Include:
- Scope: features, journey, environment/build, device states, and sampling.
- Outcome: pass within scope, issues found, or incomplete; coverage is separate.
- Findings: trigger, expected/observed behavior, user impact, severity, evidence,
  and a correction direction when supported. Source location may be unknown.
- Coverage: exercised checks, justified not-applicable checks, and not-assessed
  work with reasons. Unmeasured performance is not a pass.
- Verification: actual commands/interactions and proof locations.
- Next action: the smallest useful repair, investigation, or access decision.

No findings is a valid result. Do not pad a Top Five, attach arbitrary scores,
claim a global clean bill of health, or require a metaphorical closing paragraph.
A confirmed issue can coexist with incomplete coverage. State that plainly.
For authorized repairs, distinguish fixed-and-retested from proposed/unverified.
