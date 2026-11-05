---
name: web-debug
description: Reproduce frontend failures and verify fixes in a live browser using the active agent's available browser tools. Use for broken forms, session behavior, blank pages, failed requests, hydration issues, and browser verification of a frontend fix.
---

# Live browser debugging

Investigate a concrete reported problem through observable browser behavior.
An inspection or diagnosis request does not authorize source edits or production
mutations. Use `diagnosing-bugs` when its broader reproduction discipline helps.

This portable edition adapts the locally maintained workflow inspired by
[Amos Blomqvist's web-debug approach](https://github.com/amosblomqvist/pi-config/tree/main/skills/web-debug).
It does not require Pi, a particular browser bridge, or a paid scraping service.

## Resolve actual capabilities

Discover the active agent's browser tools and their schemas. Use its supported
navigation, accessibility/DOM inspection, interaction, screenshot, console, and
network capabilities. Tool names and arguments vary; do not invent another
harness's wrappers or assume a particular page object.

For static public content, use available search or fetch tools. For an app
interaction, use the browser. Report missing capabilities rather than treating
source inspection as a live reproduction. Do not attach a personal browser
profile or switch to a paid service without the appropriate authorization.

Prefer a suitable existing local or staging instance. If a server is required,
follow the project's launch instructions, isolate its port/state where supported,
record the exact task-owned PID, and stop only that process during cleanup.
Keep a browser session open through the reproduction; do not assume authentication
survives reconnects, another agent's session, or a tool reload.

## Reproduce and investigate

Establish the URL, expected behavior, relevant account/test state, and smallest
interaction that demonstrates the problem. Production actions must remain within
the user's explicit authority.

1. Navigate and inspect current controls. Prefer current accessibility/DOM
   references or stable role/label locators to coordinates. Refresh stale references
   after navigation or meaningful DOM changes.
2. Perform the actual user interaction. Direct state setters or API calls do not
   prove that clicking, typing, submission, or keyboard behavior works.
3. Collect the narrowly relevant console error, request outcome, DOM observation,
   and screenshot. Do not copy unrelated customer data, cookies, or credentials.
4. Form a discriminating hypothesis and inspect its source/request path. One HTTP
   status or screenshot is not enough to establish a root cause.
5. When a fix is authorized, make a scoped change and repeat the same interaction.
   Check visible feedback, focus, relevant network/console evidence, and persisted
   behavior where applicable.

Use separate evidence for distinct claims. HTTP success does not prove UI
correctness; a screenshot does not prove persistence; CSS syntax support does
not prove layout or animation behavior. For motion, check intermediate geometry
and interruption/re-entry as well as the final state, including reduced motion
and the relevant pointer/browser capabilities.

## Human handoffs and cleanup

For sign-in or consent, give the exact destination and expected environment/account,
a secure way to obtain any required credential, and the visible result that
completes the step. Never put credentials in chat. Distinguish the application's
identity from a separately connected service account. Withdraw obsolete handoff
instructions when the workflow changes.

Keep one driver per shared browser instance. Record what was exercised, observed,
and unavailable. Clean up only task-owned servers and disposable test state;
preserve authorized evidence without publishing it implicitly.
