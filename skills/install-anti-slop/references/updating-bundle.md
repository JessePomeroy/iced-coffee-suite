# Reproduce a bundled update

Do not fetch or upgrade rules as an incidental installation step. Compare a
reviewed upstream revision with the current bundle, including its license,
relative imports, supported Oxlint API, and representative project diagnostics.
Preserve local rule customizations until their disposition is explicit.

After placing the reviewed upstream asset files in `assets/anti-slop/`, run from
the skill directory:

```sh
node scripts/record-provenance.mjs /path/to/upstream-checkout FULL_40_CHARACTER_REVISION
node --test scripts/install.test.mjs
node scripts/test-profiles.mjs /path/to/project-with-installed-oxlint
```

The recorder compares the complete bundled source file set and exact bytes with
Git blobs at that revision, then copies its root license and records deterministic
hashes. It does not silently replace source files. The smoke script reuses the
supplied project's `node_modules/.bin/oxlint` and plugin dependency; it installs
nothing and leaves that project's files unchanged. Review failures against the
chosen toolchain instead of updating dependencies automatically.

For each consumer, compare the existing vendor files before using `--force`.
The installer replaces only manifest-owned files and metadata; other destination
files remain. If upstream removed a formerly owned file, identify and remove that
exact obsolete file as a separately reviewed part of the update. Run the actual
consumer lint command and compare diagnostics. Record the revision, tool versions,
file hashes, profile, and exceptions. Keep rule upgrades separate from severity
changes so either can be reviewed and rolled back independently.
