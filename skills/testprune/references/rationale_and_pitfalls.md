# Preservation rules

Tests certify supported contracts. Trace runtime entrypoints, callers, data
compatibility, docs and history; current behavior may itself be defective.
Retired producers can leave supported readers and migrations that need tests.
A stale filename, old fixture vocabulary, or persistent failure is not proof
that coverage is obsolete. Preserve the invariant before removing its test.

Git tracking and runner collection answer different questions. Ignored files
may run; tracked files may be excluded. File inventory is a candidate list, not
proof of collection, and collection itself can run imports/hooks with side effects.

Fast and broad checks can serve different purposes. Compare equivalent work when
claiming speed improvements, and preserve release validation if introducing a
focused gate. New tests must be discoverable by the intended runner/CI path.

A purported offline test must fence every reachable external boundary, including
indirect fixture and import paths. Missing credentials alone do not establish
isolation. Use existing project environments and safe test doubles at real seams.

Keep unrelated files and policy intact. Permission to clean tests is not permission
to change production contracts, synchronize unrelated instruction files, stage
changes, or publish anything.
