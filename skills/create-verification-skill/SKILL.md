---
name: create-verification-skill
description: Create or improve a project-local skill that launches, drives, and verifies a real app or service, with a maintained map of observable features. Use when asked to build reusable project verification.
---

# Create project verification

Build a repeatable way for future agents to exercise the project's real behavior.
This request authorizes verification instructions and necessary scoped helpers,
not product fixes, deployments, recurring tasks, new production dependencies, or
production data changes. Reuse an existing verification skill when it fits.

## Discover the actual project

Read instructions, Git state, runtime versions, package scripts, existing tests,
fixtures, and tool capabilities. Identify the user-facing surface: browser,
desktop, CLI/TUI, API, or library. Trace how to launch it, obtain safe test state,
check readiness, drive it, observe effects, and clean up. Detect whether instances
can be isolated by ports, profiles, data directories, or test databases.

Prefer existing Playwright/Cypress tests, API clients, CLI commands, and browser
tools over a new control layer. Build a small helper only when a repeated operation
needs deterministic execution. Do not wrap an existing command merely to add a
CLI. Use stable controls/roles, meaningful failure messages, and machine-readable
results when useful. Inspect any helper before executing it.

## Write a project-local skill

Use `.agents/skills/verify-<app>/` at the appropriate project scope, respecting
existing repository conventions. Preserve unrelated content if it already exists.
Give SKILL.md a valid name and a description identifying its app and trigger.
Keep the instructions grounded in observed commands and selectors:

- **Launch:** exact supported command, environment prerequisites, readiness signal,
  isolated instance identity, and teardown. Never print secret values.
- **Health:** a read-only check that this is the intended ready instance/account.
- **Drive:** how to perform actual user operations through the supported surface.
- **Prove:** expected outcomes and relevant side effects, with evidence paths.
- **Cleanup:** stop only task-owned instances, remove disposable state, retain proof.
- **Limits:** unavailable surfaces, accounts, permissions, or measurement tools.

Don't call internal setters and claim a user flow passed. Don't treat HTTP success
as UI correctness or screenshots as persistence proof. Mocks belong at deliberate
external boundaries; disclose what they cannot prove. Check dry-run semantics
before relying on the name. Do not create brittle launch scripts for an environment
that cannot currently run; document the exact blocker and label the output draft.

## Seed a feature map

Create `references/features/README.md` plus small feature files. Start with the
primary flows actually inspected, not an invented exhaustive inventory. The index
names feature, entry points, and scope; link to each detailed file. Use
`references/feature-template.md` in this creator as the suggested shape.

Each feature explains prerequisites, how users reach it, driver operations,
observable success/error/cancel/persistence expectations, and known limits.
Mark source-only knowledge separately from behavior exercised live. Never call
an unvisited feature verified. Shared workflows should read the relevant feature
file rather than reconstructing the whole app on every task.

## Prove and hand over

Run the generated instructions through launch, health, one representative feature,
proof capture, and cleanup. On a failed attempt, clean up its task-owned residue
before retrying. Confirm proof survives teardown. Use the actual installed tool
surface; do not assume a Cursor Task API, Pi wrapper, or browser `page` object.

Report the skill path, covered feature(s), actual proof, and unverified areas.
A skill that cannot be executed remains a draft, with the missing prerequisite.
For later upkeep, use `maintain-verification-skill` if available or follow the same
source-to-runtime check locally. Scheduling that upkeep is a separate request.

Inspired by [Lauren Tan's Pstack verification creator](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md); adapted to local authority and available tools.
