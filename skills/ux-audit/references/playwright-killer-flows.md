# Durable browser regression checks

When test changes are requested, choose the real user flows that protect the
changed behavior. Use the repository's installed harness, selectors, fixtures,
and test environment. Assert observable completion and relevant persistence,
recovery, or cancellation. Avoid arbitrary test-count targets and screenshot-only
proof for behavior.

Observe the failing case before repair when feasible, then repeat after repair.
Use deterministic request ordering for races and safe fixtures for external
boundaries. Do not add CI jobs, dependencies, or production mutations as an
implicit consequence of an audit.
