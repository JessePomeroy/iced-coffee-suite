# Skill catalog

Generated from `catalog.json` by `python3 scripts/build_catalog.py`. Do not edit directly.

Choose skills that match your work. Installing a skill does not install its tools,
authenticate an account, authorize paid calls, or grant permission to change external systems.

| Skill | When to use it | Why | Requirements |
| --- | --- | --- | --- |
| [21st-ui-build](../skills/21st-ui-build/SKILL.md) | Build substantial UI using project context and grounded 21st inspiration. | Reuse existing design primitives and preserve the product identity. | 21st CLI or equivalent MCP tools; relevant access; explicit authority for paid generation or dependency changes. |
| [babysit](../skills/babysit/SKILL.md) | Carry approved changes through PR checks, independent review, and merge. | Keep delivery engaged until the requested result is verified. | Git; GitHub CLI or equivalent; review-agent capability when requested. |
| [blast-radius](../skills/blast-radius/SKILL.md) | Trace downstream effects of a proposed change or diff. | Find affected callers, formats, configuration, and lifecycle assumptions. | Repository access; existing checks where available. |
| [bug-hunter](../skills/bug-hunter/SKILL.md) | Run evidence-backed code and security reviews, with a Svelte-first lens. | Separate reachable defects from speculation and refactoring preferences. | Node.js 22+ for structured runtime; Git; optional current documentation/advisory access. |
| [codebase-design](../skills/codebase-design/SKILL.md) | Design small interfaces that hide useful complexity. | Keep behavior and maintenance knowledge local to a clear boundary. | Project source and caller context. |
| [create-verification-skill](../skills/create-verification-skill/SKILL.md) | Build project-local launch, drive, and proof instructions. | Give future agents a repeatable way to exercise real behavior. | The project runtime and its actual browser, CLI, API, or library driver. |
| [diagnosing-bugs](../skills/diagnosing-bugs/SKILL.md) | Diagnose a reported failure or performance regression. | Find discriminating evidence before changing code. | A concrete symptom and access to the relevant implementation or runtime. |
| [docx-tracked-changes](../skills/docx-tracked-changes/SKILL.md) | Report, accept, or reject supported inline Word revisions. | Preserve restored text and original files while resolving revisions. | Python 3; lxml; python-docx for regression tests; a document renderer for layout verification. |
| [find-skills](../skills/find-skills/SKILL.md) | Find and assess existing reusable skills. | Reuse an appropriate maintained workflow instead of reinventing it. | Web/source access; Node.js and the Skills CLI only for CLI-based discovery or installation. |
| [impeccable](../skills/impeccable/SKILL.md) | Improve frontend hierarchy, typography, accessibility, and interaction. | Make design decisions deliberate and grounded in the project. | Frontend source; browser access for live verification; optional tools described by the skill. |
| [improve-codebase-architecture](../skills/improve-codebase-architecture/SKILL.md) | Compare caller-first designs for a concrete architectural problem. | Recommend an improvement grounded in actual callers and constraints. | Project source; codebase-design is a useful companion. |
| [install-anti-slop](../skills/install-anti-slop/SKILL.md) | Install bundled anti-slop Oxlint rules into an authorized project. | Enforce selected recurring code-quality rules mechanically. | A compatible JavaScript/TypeScript project and its package manager; see the bundled version requirements. |
| [maintain-verification-skill](../skills/maintain-verification-skill/SKILL.md) | Check and update a project verification skill and feature map. | Keep verification instructions aligned with source and live behavior. | An existing project verification skill and the relevant runtime/driver. |
| [pdf-reader](../skills/pdf-reader/SKILL.md) | Read, search, and selectively render local PDF pages. | Combine page-numbered text with visual evidence when layout matters. | Python 3; Poppler: pdfinfo, pdftotext, and pdftoppm. |
| [project-audit](../skills/project-audit/SKILL.md) | Coordinate a scoped audit across code, tests, security, UX, and architecture. | Produce one evidence-backed report with honest coverage and limits. | Applicable bundled skills; project-specific checks; live drivers for runtime claims. |
| [punchlist](../skills/punchlist/SKILL.md) | Audit UI against named defects with locations and evidence. | Turn design criticism into concrete, assessable findings. | Suitable rendered/screenshot input; independent critics when required by its protocol; Python helpers; optional report tooling. |
| [redesign-existing-projects](../skills/redesign-existing-projects/SKILL.md) | Improve an existing frontend while preserving its functionality. | Replace generic or weak visual patterns using the existing stack. | Project frontend and a rendered browser for meaningful visual verification. |
| [reflect](../skills/reflect/SKILL.md) | Review selected completed work and recurring corrections. | Propose small durable improvements rather than accumulating generic rules. | Selected conversation/task evidence; history tools are optional. |
| [svelte-best-practices](../skills/svelte-best-practices/SKILL.md) | Apply modern Svelte 5 and SvelteKit patterns. | Respect reactivity, ownership, SSR, accessibility, and server boundaries. | A Svelte/SvelteKit project; current official docs for version-sensitive decisions. |
| [testprune](../skills/testprune/SKILL.md) | Audit or improve a noisy, slow, redundant, or unsafe test suite. | Preserve meaningful invariants and trustworthy offline verification. | Python 3 for inventory; the project test runner; explicit invocation where the host honors that policy. |
| [typesafe-ai](../skills/typesafe-ai/SKILL.md) | Compose typed AI judgments and probabilities with application code. | Keep workflow logic in code while using AI for semantic decisions. | Current TypeSafe documentation; credentials and service access for explicitly authorized API work. |
| [unclaimed](../skills/unclaimed/SKILL.md) | Find and refresh single-word domain availability and pricing. | Use the supporting CLI rather than guessing availability. | Unclaimed CLI; network access; optional registrar configuration. |
| [ux-audit](../skills/ux-audit/SKILL.md) | Exercise real user journeys in a live application. | Find task-level confusion, blockers, and recovery problems. | A real app instance; a supported browser driver; authorized test state. |
| [web-debug](../skills/web-debug/SKILL.md) | Reproduce frontend failures and verify fixes in a real browser. | Connect actual interactions, console/network evidence, and observable outcomes. | A browser automation tool supplied by the active agent; relevant local/staging access. |
| [youtube-transcript](../skills/youtube-transcript/SKILL.md) | Retrieve YouTube captions with timestamps and source links. | Summarize or search spoken content without a paid transcription service. | Python 3; yt-dlp; network access; existing video captions. |

## Bug Hunter's nested skills

These travel with the parent package; the installer does not create duplicate top-level links.

- [commit-security-scan](../skills/bug-hunter/skills/commit-security-scan/SKILL.md): Review the security effects of a particular commit, branch, or PR diff.
- [doc-lookup](../skills/bug-hunter/skills/doc-lookup/SKILL.md): Verify framework and library behavior with current documentation.
- [fixer](../skills/bug-hunter/skills/fixer/SKILL.md): Apply explicitly authorized fixes for verified defects.
- [hunter](../skills/bug-hunter/skills/hunter/SKILL.md): Find reachable defects with concrete triggers, consequences, and evidence.
- [recon](../skills/bug-hunter/skills/recon/SKILL.md): Map entrypoints, ownership, architecture, and trust boundaries.
- [referee](../skills/bug-hunter/skills/referee/SKILL.md): Resolve findings and objections against current evidence.
- [security-review](../skills/bug-hunter/skills/security-review/SKILL.md): Assess security with threat-model and relevant dependency context.
- [skeptic](../skills/bug-hunter/skills/skeptic/SKILL.md): Challenge findings and investigate plausible counterevidence.
- [threat-model-generation](../skills/bug-hunter/skills/threat-model-generation/SKILL.md): Map assets, boundaries, and threats using STRIDE.
- [vulnerability-validation](../skills/bug-hunter/skills/vulnerability-validation/SKILL.md): Establish reachability, exploitability, and practical impact.

## Deliberately separate

Company integration (`client-site-integration`, `hubspoke-sync`), Pi history and
orchestration, Herdr control, and the author's printer-specific label workflow
remain outside this portable distribution. Official system skills and managed
plugins should be installed through their providers. See [sources](../SOURCES.md).
