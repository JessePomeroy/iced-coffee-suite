# Verification

From the repository root:

```zsh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
```

The validator checks catalog coverage, required frontmatter, complete nested skill
entrypoints, carried licenses, generated catalog freshness, and the absence of
distribution symlinks and private/cache directories.

Installer tests use temporary homes and custom discovery directories. They cover
preview behavior, multiple agents, duplicate shared destinations, conflicts,
existing instructions, broken and changed links, rollback after a creation failure,
path containment, installation checks, and removal without source deletion.
Compatibility-link tests cover both Codex roots, shared-root deduplication,
conflict preservation, preview, check, and removal. Discovery tests use a fake
stdio server and fixtures, including timeouts, cleanup, disabled/missing skills,
same-named packages from other sources, and discovery errors. They make no paid calls.

## Package helper checks

The package scripts retain their own focused tests. Run a relevant suite after
changing helper behavior, using the appropriate installed environment:

```zsh
python3 -B -m unittest discover -s skills/pdf-reader/scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s skills/youtube-transcript/scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s skills/docx-tracked-changes/tests -p 'test_*.py' -v
```

The PDF suite needs Poppler and the DOCX suite needs `lxml` and `python-docx`.
Do not install those globally to force a pass. Missing prerequisites are reported
as unavailable verification. Transcript tests are offline; a real video request
would be a separate network check and would depend on caption availability.

For Bug Hunter's packaged runtime, Node.js 22+ supports:

```zsh
node skills/bug-hunter/scripts/run-bug-hunter.cjs preflight --skill-dir skills/bug-hunter
```

This distribution includes its runtime package, not the complete upstream release
development checkout. Its upstream `npm test`/release scripts can reference omitted
development resources; use the upstream project for release development.

## Actual agent discovery

`install.py --check` proves the selected link targets only. A fresh agent session,
its discovery UI, and an exercised skill are separate verification. Do not claim
all agents or optional paid services work from an installer unit-test pass.

After installing selected skills, run the optional local Codex diagnostic from
this checkout with the same selection:

```zsh
python3 scripts/check_codex_discovery.py --skill slice-loop-workflow --cwd /path/to/project
```

Use `--all` only when every bundled top-level skill was installed. `--codex` accepts
an executable name or path, and `--timeout` sets a positive response deadline
(30 seconds by default). The diagnostic starts its own local app-server, performs
`initialize` and `skills/list` with `forceReload`, and closes that process. It
does not start a model turn, alter discovery links, or change account settings.
The CLI can still read its normal configuration and contact configured services
during startup; this is not an offline or sandboxed Codex invocation.

Results distinguish `FOUND`, `DISABLED`, `MISSING`, and `OTHER_SOURCE`. Only an
enabled manifest resolving to this checkout's expected `SKILL.md` passes. Other
same-named sources are disclosed even when the selected manifest is present.
Any reported discovery errors make the check incomplete. Exit status is `0` for
a complete selected listing, `1` for incomplete discovery, and `2` when the CLI,
protocol, arguments, or timeout prevent verification.

This checks the experimental local app-server interface (exercised with Codex CLI
0.165.0). If a host or version does not support it, report the unavailable check
and use that host's discovery UI. Do not infer success from link existence or a
same-named package elsewhere. Refresh the actual running agent separately and
exercise the skill's behavior with its required tools before claiming an end-to-end pass.

On 2026-11-06, an actual Codex CLI 0.165.0 scan found all 26 bundled top-level
manifests through links in a temporary Git project's `.agents/skills` directory.
After those links were removed, the diagnostic correctly rejected the same-named
global Slice Loop package as `OTHER_SOURCE`. The temporary project was removed
and the maintainer's global discovery links were verified unchanged. This was a
discovery smoke check; it did not execute the skills' workflows.
