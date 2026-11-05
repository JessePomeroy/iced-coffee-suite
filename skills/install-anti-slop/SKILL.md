---
name: install-anti-slop
description: Install or update the bundled Oxlint anti-slop rules, preview diagnostics, and select a project-appropriate rule profile. Use for requested anti-slop lint setup or migration.
---

# Install anti-slop

Integrate the bundled rules with the project's actual lint configuration. Installing
rules does not authorize unrelated code cleanup, production dependencies, or
rewriting an existing policy. Preserve existing rule choices unless changing them
is part of the request.

## Inspect

Read project instructions, Git state, package manager/lockfile, installed Oxlint
version, configuration, and any existing plugin copy. Inspect baseline lint
results and boundary parsing conventions. Do not overwrite a customized plugin
without comparing its source and diagnostics.

The bundle includes `LICENSE` and `PROVENANCE.json` with the reviewed upstream
revision and SHA-256 hashes. The installer verifies these before writing and after
copying. This detects accidental drift; it is not a signature or upstream trust
attestation. For an intentional rule update, follow `references/updating-bundle.md`.

## Select and preview a profile

Read `references/rule-profiles.md`. For a new setup, start with the small baseline
profile, not every bundled rule. The strict profile is an opt-in architectural
policy for named internal modules. Boundary validators may accept `unknown` and
use runtime narrowing; do not require a schema dependency or unsafe cast just
to satisfy a rule.

Preview selected rules at warning severity using a temporary configuration or a
reviewable local config change. Inspect representative diagnostics in boundary
parsers, domain code, tests, and framework adapters before final enforcement.
Warnings here are a migration preview, not a way to hide failed required checks.
Explain material policy tradeoffs and get a choice if selection would broaden
scope or conflict with established architecture.

## Install and configure

1. Resolve this skill's directory and use `scripts/install.mjs` from the target
   repository. It copies to `tools/oxlint/anti-slop/`, or a supplied project-relative
   directory, and refuses replacement by default. Use `--force` only after
   preserving and reviewing the exact existing files.
2. Reuse installed compatible `oxlint` and `@oxlint/plugins` versions when possible.
   Check current compatibility/release documentation before adding or upgrading.
   Use the repository package manager and lockfile; these are development
   dependencies for a local plugin. Do not upgrade both packages merely to match
   the latest registry version or assume their version numbers must be equal.
3. Merge the plugin into `jsPlugins` (or `lint.jsPlugins` in Vite+):

   ```ts
   { name: "anti-slop", specifier: "./tools/oxlint/anti-slop/index.ts" }
   ```

   Preserve existing ignores. Exclude the copied vendor plugin and installed
   agent assets when they are not owned application code; do not blanket-ignore
   dot-directories containing project source. For Vite+, align formatter ignores
   for those same vendored assets.
4. Apply the selected rules and justified file-scoped boundary exceptions. For a
   strict profile, show the target globs and excluded boundary paths explicitly.
   Do not silently relax existing enforced rules during an update.
5. If the project directly declares Effect or explicitly requests Effect policy,
   offer the bundled `anti-slop-effect` plugin from `effect/index.ts` and its
   `no-service-constructor-imports` rule. A transitive lockfile entry alone does
   not justify enabling it. Its relative-import coverage does not cover aliases.

## Verify and hand off

Run the repository lint/type checks and, for Vite+, its applicable combined check.
Fix source diagnostics only when migration/cleanup is authorized. Never launder
types, add unsafe casts, suppress required checks, or discard valid boundary
validation to make the new configuration green.

Report copied files, versions, chosen profile, exact exceptions, actual checks,
and remaining migration work. Keep a new preview unenforced when policy remains
unresolved; do not describe that as a clean enforced installation.

Record each retained diagnostic's location, rule, owner contract, and concrete
reason. Partial SDK test doubles and malformed-input fixtures may need assertions;
already typed mock calls and pure provider error classes usually do not. Retaining
a justified cast is not a decision to retain its test in a later suite cleanup.
Promote one reviewed rule at a time and prove a deliberate violation fails the
repository's normal lint command. Report Svelte script coverage separately from
template, CSS, type-checking, and rendered behavior.
