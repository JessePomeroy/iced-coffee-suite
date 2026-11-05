# Svelte verification and test-quality guide

Choose evidence that can observe the alleged failure. Use existing project
commands and installed versions. Begin with focused checks; a full browser
matrix is not required for a pure helper edit, and a type check cannot establish
that a dialog is usable.

## Match the test to the boundary

| Claim | Useful verification | Insufficient on its own |
|---|---|---|
| Calculation/validation | Direct inputs, boundaries, failure cases | Casts or copied implementation |
| Rune/prop/lifecycle behavior | Mounted real component with prop updates and teardown | Remount for every state |
| Async ownership | Controlled deferred completions in both orders | Only immediately resolved mocks |
| Server isolation/authorization | Actual handler with separate requests/identities | Parent-layout test alone |
| SSR/hydration | Server render or request plus hydration/navigation | Client-only component test |
| Layout/focus/observer behavior | Styled component in a real browser | DOM emulator or source regex |

Run the project's Svelte/compiler/type/lint checks when relevant. Record exact
commands and results. Compiler success is valuable evidence for syntax/types
and enforced imports; it does not prove runtime correctness.

## Component and async regression checks

Exercise production component code, its real event handlers, and meaningful
markup. Stub the external boundary, not the state ownership being tested.
Avoid harnesses that implement a second copy of the intended fix.

For a race, hold requests open with deferred promises. Start A, switch to B,
finish B, then finish A. Assert the visible data and command payload still
belong to B. Add close/reopen or destruction only when the owner can undergo
that transition. Exercise failure/retry and loading-state ownership if they
are part of the defect. Prefer controllable scheduling to arbitrary sleeps.

If a defect depends on component reuse, update props or navigate through the
real reusable route. Do not accidentally reset all local state by mounting a
fresh instance for each assertion. Verify cleanup after the actual lifecycle
transition, not just that a mocked cleanup method was called somewhere.

## Rendered browser verification

Use the repository's existing browser runner, base URL, allowed hosts, and
isolated environment. Do not start a development server only to browse source.
When one is needed, record the exact PID/container identity and stop only what
this task started. Never load production credentials or mutate live data to
test a component. Missing browser binaries or OS libraries are limitations;
use an already-supported isolated environment when available, otherwise report
the gap rather than silently substituting an emulator.

Capture the initial state before helpers that focus, scroll, or click can
change it. For obstruction/clipping, compare meaningful rectangles and hit
testing with viewport bounds and occluding UI. Then verify keyboard access and
interaction. A screenshot, `isVisible`, and a successful force-click measure
different things; none alone proves that a user can reach the control.

Match viewport and text-size checks to the changed layout. Verify overflow and
controls in short/narrow states as well as a typical desktop where relevant.
For animation or async rendering, wait for an observable settled state instead
of expanding timeouts blindly. Browser errors require investigation; do not
filter ResizeObserver errors merely to turn CI green.

## Reading CI failures honestly

Preserve the commit, browser/project, failed assertion, and relevant trace or
error context. Distinguish assertion-time evidence from later DOM snapshots.
A trace's reference to an after-snapshot is not proof that one was captured.
A cumulative timeout can reflect prior retries rather than a slow product
operation. Reproduce a suspected regression at the exact head and compare a
minimal relevant baseline when practical.

Do not claim a browser pass from an unexecuted command, an old artifact, or a
different commit. Report what passed, failed, or could not run. A failing
required verification gate remains a gate; do not delete the gate or change
its intended behavior without authority.

## Reducing a test suite without losing protection

When requested, first map each candidate test to its behavior and failure mode.
Remove duplicate setup/assertions or table-drive equivalent cases, while
keeping distinct security boundaries, lifecycle transitions, error paths,
browser engines, and meaningful boundary values. Explain which retained test
would catch the regression protected by a deleted test.

Prefer one small real seam over elaborate mocks. Replace source-text assertions
with behavioral or compilation checks where feasible. Do not add generic test
helpers unless several consumers genuinely benefit; do not erase useful test
names or independent failures just to reduce lines. Assertions of TypeScript
casts are not runtime guarantees. Keep compile-time fixtures when the contract
being tested really is compile-time.

Measure net changes including new helpers/fixtures. Run retained focused cases
and relevant broader checks after a reduction. Fewer tests, retries, skips, or
silenced errors are not evidence of improvement.
