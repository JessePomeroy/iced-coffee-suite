# Draft a test-cleanup handoff

Inspect within the requested read scope and return a concrete prompt/plan. Include
repository/revision, permitted files, preserved user changes, supported production
contracts, actual runner/environment, safe baseline evidence, candidate changes,
replacement invariants, and verification commands. Mark unknown facts explicitly.

Separate proposed test/config changes from decisions affecting product behavior,
dependencies, CI gate semantics, or external systems. A plan authorizes none of
these. Save a file only when requested or appropriate to the requested deliverable;
do not edit instruction files while drafting a prompt.

Avoid fixed durations, agent counts, test quotas, new runner layers, or a mandatory
pair of visualizations. Use a table when it clarifies measured comparisons.
