# Feature map shape

Use one compact file per coherent user-facing feature. Suggested fields:

- Purpose and supported user/task.
- Entry points, including distinct routes or callers when their behavior differs.
- Prerequisites: safe account role, data state, environment, feature flag.
- Driver steps: actual commands or controls from this project.
- Expectations: observable success, error, empty, cancellation, and persistence
  behavior applicable to this feature.
- Proof: assertion, screenshot, response, file, or reload evidence that settles
  the expectation; distinguish source-inspected from live-exercised facts.
- Limits/gotchas: required entitlement, unsupported environment, isolation needs.

The index links feature files and names the inventory's scope. Include a last
verified revision/environment when useful; age alone is not proof of drift.
Do not fill unknown selectors or commands with plausible guesses. The generated
project map should contain concrete instructions and explicit gaps, not this
abstract template.
