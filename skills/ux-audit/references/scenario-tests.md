# Optional scenario catalog

Select applicable scenarios from the brief and feature map; do not run all of
these for every page. Name omitted in-scope scenarios as unassessed.

1. First visit: discover the intended action with the expected account state.
2. Empty state: useful explanation and next action.
3. Normal completion: input, action, feedback, persisted result.
4. Validation/recovery: invalid input, understandable error, correction.
5. Loading/slow response: progress, repeated action, cancellation when supported.
6. Failure: safe test failure, retained work, retry without duplicate effects.
7. Navigation round trip: return to the right entity and expected state.
8. Account/permission boundary: allowed and denied actions for authorized test roles.
9. Keyboard/focus: reach, operate, dismiss, and restore focus.
10. Responsive/content stress: relevant narrow layout and realistic data extremes.
11. Re-entry: reload/session interruption where persistence is part of the contract.

Destructive confidence checks, failure injection, account changes, and data seeding
require explicit scope. Report unavailable prerequisites instead of forcing a run.
