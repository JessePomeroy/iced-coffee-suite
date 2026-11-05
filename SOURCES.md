# Sources and distribution notes

This checkout was assembled on 2026-11-05 from the author's maintained shared
suite and separately installed packages. It is a portable snapshot. Editing it
does not update the author's separate live `agent-config` folder automatically.
No credentials, sessions, plugin caches, dependency installations, or absolute
discovery symlinks are part of the distribution.

The root license covers the original installer, repository tooling, documentation,
tests, and instruction template. It does not assert a blanket license for every
skill. Keep the terms, attribution, and provenance files carried by each package.

## Recorded upstream projects

| Package | Recorded source | Carried terms and local edition |
| --- | --- | --- |
| Bug Hunter | [codexstar69/bug-hunter](https://github.com/codexstar69/bug-hunter) | Package MIT license. This is the locally adapted Svelte-first edition, not an unmodified upstream install. |
| Punchlist | [xenstalker02/punchlist](https://github.com/xenstalker02/punchlist) | Package MIT license and complete supporting taxonomy/report resources. |
| Find Skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Upstream MIT license; retrieval details in `licenses.json`. |
| Impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Upstream Apache-2.0 license; the installed edition includes local modifications. |
| 21st UI Build | [21st-dev/skill](https://github.com/21st-dev/skill) | Upstream Apache-2.0 license; the installed edition includes local modifications. |
| UX Audit | [jezweb/claude-skills](https://github.com/jezweb/claude-skills) | Upstream MIT license; locally maintained entrypoint and references. |
| Unclaimed | [iannuttall/unclaimed](https://github.com/iannuttall/unclaimed) | Upstream MIT license and original agent metadata. |
| TypeSafe | [typesafe-ai/skills](https://github.com/typesafe-ai/skills) | Package MIT license. |
| Testprune | [NeuraCerebra-AI/testprune](https://github.com/NeuraCerebra-AI/testprune) | Package license; locally maintained snapshot based on checkout `4f692700603018ea7f1ddd16d2001977b92852c5`. |
| Anti-slop rule sources | [dmmulroy/anti-slop](https://github.com/dmmulroy/anti-slop) | The bundled assets retain their MIT license and existing `PROVENANCE.json`; the installer wrapper is locally maintained. |
| Codebase Design, Improve Codebase Architecture, Diagnosing Bugs | [mattpocock/skills](https://github.com/mattpocock/skills) | Upstream entrypoints and MIT license verified; these are locally adapted editions. |
| Redesign Existing Projects | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Upstream MIT license. This preserves the older redesign workflow; newer upstream releases have retired/reorganized it. |
| Pstack influences | [cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack) | MIT license retained with the four locally rewritten workflows that record this influence. |

`licenses.json` records the upstream license URLs and blob SHAs retrieved for
packages whose installed directories lacked a license file. It does not identify
the upstream revision of every locally modified skill file.

## Personal workflows and recorded influences

`babysit`, `blast-radius`, `codebase-design`, `create-verification-skill`,
`diagnosing-bugs`, `docx-tracked-changes`, `improve-codebase-architecture`,
`install-anti-slop`, `maintain-verification-skill`, `pdf-reader`, `project-audit`,
`redesign-existing-projects`, `reflect`, `svelte-best-practices`, `web-debug`, and
`youtube-transcript` were copied from the maintained personal suite.

The PDF, YouTube, browser, and Svelte workflows also have published snapshots in
[Rhubarb](https://github.com/JessePomeroy/rhubarb). Their current portable editions
may differ from those snapshots. DOCX's [implementation provenance](skills/docx-tracked-changes/PROVENANCE.md)
distinguishes its original helper from the managed Documents plugin.

Blast-radius, verification creation/maintenance, and reflection record inspiration
from [Pstack](https://github.com/cursor/plugins/tree/main/pstack). PDF, YouTube, and
browser workflows record inspiration from
[Amos Blomqvist's Pi configuration](https://github.com/amosblomqvist/pi-config).
Those links describe recorded influences and the carried licenses identify the
corresponding upstream terms. The original installation did not record exact
upstream revisions for every locally modified file. New research established the
Matt Pocock and Leonxlnx sources above; do not replace the maintained editions with
their current upstream versions merely to make versions match. For the personal
entries `babysit` and `project-audit`, the publication review found no recorded
earlier upstream source. That history remains unverified: this catalog does not
assign them an inferred third-party license or claim the entire suite is uniformly
MIT. The root license retains the limited scope stated above.

## Changes made for portability

- PDF and YouTube helper examples resolve paths from the installed skill directory
  instead of a Pi discovery path, with zsh-compatible examples.
- DOCX uses an existing Python environment with `lxml`; it no longer assumes an
  author's cached Codex artifact interpreter. Document rendering remains a separate
  verification requirement using the available document workflow.
- Web Debug discovers the active harness's actual browser tools rather than
  requiring Pi's browser wrappers or local service manager.
- The old `redesign-skill` directory is named `redesign-existing-projects` to match
  its existing frontmatter name. Its workflow content is preserved.
- Apache-licensed entrypoints carry a notice that they are modified local editions.
  Impeccable's `extract.md`, `harden.md`, and `optimize.md` references also carry
  notices for trailing-whitespace normalization during publication checks.
- Bug Hunter is exported using its package runtime allowlist, plus package metadata
  and its lockfile. Generated validators/prompts are preserved, not hand-edited.
  Upstream release tests, evaluation state, large promotional images, local run
  artifacts, and dependency trees are not part of this runtime distribution.
- Punchlist also retains the governance files used by its package validator.
- Other packages retain their runtime scripts, tests, references, assets, and
  metadata. Nested Git metadata, caches, and installed dependencies are excluded.

## Deliberately excluded

Angels Rest/HubSpoke integration packages contain project-specific knowledge.
Pi history/orchestration, Herdr control, and the MUNBYN queue-specific label workflow
depend on an individual environment. Keep them in their appropriate installations.
Managed OpenAI/plugin skills are not redistributed from a local cache.

For updates, compare whole packages and preserve local edits and licenses.
Replacing a personal edition with an upstream installation can remove its local
behavior. Review the diff instead of updating by name alone.
