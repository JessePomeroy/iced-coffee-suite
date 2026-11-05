# Interaction record

Record the feature, environment, preconditions, action/target, expected result,
observed result, and proof location for each meaningful check. A concise table
or structured log is enough; use the project's evidence format when it has one.
Record only actions actually performed. Timestamp events when the tool provides
it; do not invent timing or infer authenticity from a minimum event gap.

Plan coverage by applicable behavior, not a quota of six actions per route.
For each planned check record:
- Exercised: observed result and evidence, whether passing or failing.
- Not applicable: the feature/state does not exist or is outside the declared scope.
- Not assessed: missing capability/access/time or another blocker, plus remaining work.

Screenshots establish visible state; DOM assertions, request outcomes, files,
and reload checks may establish other effects. Capture the action and outcome
when needed to connect cause and effect. Keep selectors fresh after navigation.
A route without a form or modal is not missing interaction evidence merely
because those checks do not apply. Report coverage over the declared applicable
checks and disclose sampling; never label a sample an exhaustive audit.
