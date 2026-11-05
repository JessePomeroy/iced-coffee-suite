# Authentication and authorization during a walkthrough

A 401 or 403 does not uniquely identify expiry. Check the operation, expected
role, environment, redirects, prior account state, and observable UI response.
A denied request may demonstrate correct access control. Record the exact step
without capturing tokens, cookies, or sensitive response bodies.

If the test session actually expires, preserve evidence and mark the affected
checks blocked. Re-authenticate only through the available authorized test-account
flow, then resume from known state. Otherwise request the specific missing access
and report incomplete coverage; do not discard unrelated completed evidence.
Do not acquire personal browser cookies, expose credentials, or label every
expiry a product bug. Report a defect when the app's handling violates its
expected behavior, such as losing submitted work without recovery.
