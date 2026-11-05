---
name: svelte-best-practices
description: Apply modern Svelte 5 and SvelteKit conventions when creating, reviewing, or editing .svelte files and SvelteKit routes, load functions, form actions, hooks, or server modules.
---

# Svelte best practices

## Establish project context first

1. Inspect `package.json`, Svelte/SvelteKit versions, configuration, and nearby components.
2. Follow the project's established runes or legacy style. Do not migrate unrelated legacy components merely because Svelte 5 is installed.
3. Use generated route types from `./$types` and preserve the project's formatter, linter, test, and package manager choices.

## Svelte 5 components

For new Svelte 5 components, prefer runes mode:

- Use `$state` only for values whose changes must update a template, `$derived`, or `$effect`. DOM references, animation handles, and disposers can stay ordinary local variables when they have no reactive consumers.
- Use `$state.raw` for large objects or arrays that are replaced rather than deeply mutated.
- Compute values with `$derived` or `$derived.by`; do not synchronize derived state through `$effect`.
- Treat `$effect` as an escape hatch for external side effects. Avoid updating state from effects and always clean up subscriptions, observers, and timers.
- Declare typed props with `$props`; use `$bindable` only when two-way binding is intentional.
- Prefer callback props over `createEventDispatcher` and snippets over legacy slots in runes-mode components.
- Keep component state local unless it genuinely needs to be shared. Use context or `.svelte.ts` state modules deliberately.

## DOM behavior and elegance

- Identify what CSS and the browser already handle before adding imperative code. Preserve native layout and reflow; isolate the unsupported behavior. Prefer one capability-checked implementation over browser-name branches when its behavior is verified across the relevant engines.
- For new element-owned behavior in Svelte 5.29+, consider `{@attach ...}` with setup and a returned cleanup function in one place. Keep working actions unless migration has a concrete benefit. Reactive reads during attachment setup can cause reruns; choose those dependencies deliberately.
- Use declarative event attributes for ordinary markup. For imperative listeners that interact with Svelte handlers, use `on` from `svelte/events` to preserve event ordering. It returns a disposer; collect those disposers in the owning attachment's cleanup without adding a second listener-cleanup mechanism.
- Separate interaction changes from teardown. Cancel owned resources on cleanup, and honor live reduced-motion preferences for animation. A finite animation may finish during a fade when immediate cancellation would cause a visible jump; verify interruption and re-entry rather than cancelling on every visibility change.
- Batch geometry reads before DOM or style writes. Prefer event-driven updates or browser-managed animation when they express the behavior; justify a continuous measurement loop with a requirement that actually needs it. A browser-managed animation of layout properties still has rendering cost.
- Reduce state, synchronization, and competing code paths before compressing syntax. Use names that expose intent, guard clauses that clarify the main path, and small helpers for non-obvious calculations or behavior. Preserve short usage-contract comments. Nested closures and CSS conditions are valid tools; flatten them when it improves readability or follows an explicit project preference, not solely to minimize line count.

## SvelteKit boundaries

- Keep secrets, privileged credentials, and database access in server-only modules (`+page.server`, `+layout.server`, `+server`, or `$lib/server`).
- Use server `load` functions for private data and universal `load` functions only when browser execution is safe and useful.
- Avoid unnecessary `await parent()` calls because they create loading waterfalls.
- Prefer form actions for ordinary data mutations and progressive enhancement. Use remote functions only when the installed SvelteKit version and project configuration intentionally adopt them.
- Use `error` and `redirect` according to SvelteKit control flow; do not accidentally catch redirects.
- Validate all untrusted form, URL, cookie, and endpoint input at the server boundary.
- Preserve SSR safety: guard browser-only APIs and do not introduce hydration-dependent behavior without need.

## Markup and accessibility

- Prefer semantic HTML before ARIA.
- Keep labels, keyboard behavior, focus handling, and error messaging accessible.
- Use keyed each blocks only when identity matters.
- Avoid unnecessary wrapper elements and component abstractions.

## Validation

Run the repository's relevant formatting, `svelte-check`, type-check, lint, unit, and browser tests after changes.

## Official references

- https://svelte.dev/docs/svelte/best-practices
- https://svelte.dev/docs/svelte/v5-migration-guide
- https://svelte.dev/docs/svelte/@attach
- https://svelte.dev/docs/svelte/svelte-events
- https://svelte.dev/docs/kit/load
- https://svelte.dev/docs/kit/form-actions
- https://svelte.dev/docs/kit/remote-functions
