# Resolve deferred test questions

Read the named items, current revision, and approved mutation scope. A prior report
is evidence, not permission. For each item, identify the conflicting claimants:
code, test, comment, docs, configuration, and supported caller behavior.

Inspect history and reachable paths. Do not use a universal authority ranking:
a document may be stale, a test may encode a bug, and a newer comment may be wrong.
If evidence establishes the supported contract, correct only the authorized test,
document, fixture, or implementation. If intent remains ambiguous, describe the
choice and leave conflicting assertions visible rather than codifying a guess.

Preserve historical-row/read compatibility tests. A configured backend that cannot
complete a supported workflow may still need refusal/adapter coverage. Record
retention prerequisites before proposing removal of dormant production modules.

Review CI/release callers when a requested change alters their test command.
Run focused affected tests and the broader gate warranted by shared changes.
Follow repository documentation requirements; do not invent new ledgers or fixed
agent/time budgets. Report resolved, unresolved, and out-of-scope items distinctly.
