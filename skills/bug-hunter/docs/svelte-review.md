# Svelte and SvelteKit review lens

Use the sections touched by the requested behavior. This is a hypothesis guide,
not a list of patterns to flag automatically. Confirm the installed framework
version and compiler configuration before applying version-sensitive guidance.

## Read the whole component and its owner

Inspect instance and module scripts, template branches/snippets, bindings,
actions/attachments, and relevant scoped styles. Follow direct callers and
rune modules. A script-only index cannot show which handler a template invokes,
whether a node still exists, or what a containing block does to its layout.

Separate component-local state, route data, shared client state, and server
request state. Name the owner of each asynchronous operation or external
resource. Read an external boundary's actual return/failure contract before
inventing a compatibility wrapper.

## State, props, and component reuse

- Trace a prop update through every consumer. A destructured plain value or a
  one-time state initializer may be an intentional snapshot; report it only
  when later updates must be observed. Distinguish reactive `$props` bindings
  from values copied out of a reactive object or passed by value to a helper.
- Prefer a proven live derivation over state duplicated in an effect, but do
  not report `$effect` itself as a defect. Determine whether a value is editable
  draft state, derived output, or a deliberate initial default.
- Follow navigation or selection A → B while the component stays mounted.
  Check captured IDs, selected variants, validation, pending work, and callbacks.
  Route components may be reused; a remount in a test can conceal stale state.
- Check mutation semantics for `$state.raw`, non-plain objects, collection
  wrappers, and exported rune modules only when the code relies on them.
  Types and casts do not prove runtime identity or reactivity.
- A keyed block/list changes DOM identity and can reset focus or local state.
  An unkeyed list is not automatically wrong. Show which state or DOM node is
  incorrectly associated with a different record before recommending a key.

## Effects, asynchronous work, and cleanup

An effect tracks reactive reads made synchronously during its execution,
including synchronous calls it makes. Reads only after `await` or in a later
callback do not become dependencies of that run. Dependencies reflect the
branches actually read on that execution. Validate against the project's
version of the [effect contract](https://svelte.dev/docs/svelte/$effect).

For each effect, subscription, action/attachment, or lifecycle hook:

1. Identify the state that starts/restarts it and the resource it owns.
2. Trace rerun, destruction, navigation, and failure. Check listeners, timers,
   animation frames, observers, subscriptions, and pending requests.
3. Test late completion after a newer request or a close/reopen. Cancellation
   alone is not always enough; an operation that cannot be cancelled still
   needs an ownership/staleness check where its result is applied.
4. Check teardown identity and ordering. Restore the prior global value rather
   than a guessed default; nested consumers may share body scroll, focus, or
   document listeners. An async callback does not return a synchronous cleanup
   function to an API that expects one.

Do not move every operation into an effect or require every effect to abort.
Prove a lifecycle mismatch. Third-party UI, canvas, and subscriptions are valid
effect uses. Check actual error handling; swallowing rejection is not cleanup.

## SSR, hydration, and SvelteKit request boundaries

- Separate module evaluation, server rendering, hydration, and client events.
  Browser globals accessed during SSR can fail even if later code is guarded.
  Effects do not run during SSR; they cannot supply required initial server
  output. A browser-only callback is not defective merely for using `window`.
- Look for user/tenant/request data in server module-level mutable state or
  stores. Demonstrate the cross-request path, not just the existence of a
  module singleton. Immutable config and safely scoped clients can be valid.
- Load results crossing to the browser are public to that caller. Check for
  secrets or excessive data even when their source file is server-only.
- Trace authorization at the actual endpoint/action/query. A layout check is
  not universal protection for independently callable handlers. Authentication
  proves identity; membership/ownership checks authorize the requested object.
- Confirm server-only imports and environment boundaries. Compiler protections
  are useful evidence, not a substitute for checking what a handler returns.
- For redirects, cache keys, invalidation, cookies, and form-action behavior,
  consult the installed adapter/framework contract. Do not infer safety from a
  route filename or blindly apply another framework's CSRF defaults.

Primary references: [state management](https://svelte.dev/docs/kit/state-management),
[server-only modules](https://svelte.dev/docs/kit/server-only-modules),
[authentication](https://svelte.dev/docs/kit/auth).

## Template and security semantics

Trace data into the actual sink: escaped interpolation differs from `{@html}`,
URL navigation, inline styles, and server-side fetch targets. Ordinary escaped
text does not prove a separate raw-HTML path safe. Establish attacker control,
reachable execution, and missing protection before calling it a vulnerability.

Review uploads, object ownership, redirects, webhooks, payment callbacks, and
tenant selection at their trust boundary. Existing schema validation is only
relevant if it runs on that path and constrains the field at issue. Keep
security probes local and inert; do not contact live customers/providers.

## Browser layout and accessibility

- Read containing blocks, overflow, sticky/fixed positioning, and responsive
  styles together with conditional rendering. CSS-hidden content is not
  necessarily unmounted; mounted does not mean visible or interactive.
- For observer-driven layout, trace measurement → write → layout → notification.
  A real feedback loop needs an ownership/scheduling fix, not an ignored browser
  error. Deferring work to a cancellable animation frame can be appropriate
  when demonstrated; it is not a universal wrapper for layout code.
- Test modal/menu focus entry, Tab and reverse Tab, Escape, opener restoration,
  nested owners, background inertness, and scroll locking where relevant.
  Native controls reduce custom behavior but do not validate their labels or
  disabled/loading states by themselves.
- Check short/narrow viewports, text enlargement, and reflow for sticky purchase
  controls or dialogs. Root-font enlargement and browser zoom are different
  checks. Capture geometry before focus/scroll helpers can move a clipped target
  into view. Confirm the control can be hit and reached, not merely that it is
  attached to the DOM.
- Use the actual browser for layout/observer/focus claims. Include WebKit or
  another engine when the risk is browser-dependent; disclose unavailable
  engines rather than treating one engine's pass as universal.

## Architecture and simplification, when requested

Prefer one owner for state, resource cleanup, or a security decision. Recommend
an extraction when it hides real complexity behind a useful interface, not to
move lines into another file. Pure calculations can be tested directly; a
network boundary still needs explicit failure, retry, and identity handling.

Map a proposed deletion to retained behavior and tests. Keep architecture
options separate from verified defects, and identify any public/API/data-model
change that requires a decision. Never use a line-count target to remove a
necessary guard, browser regression, or distinct negative-path test.
