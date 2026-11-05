# Known diagnostics and project budgets

Read an existing audit configuration at the documented project path, otherwise
look for `audit-config.yml`, `audit-config.json`, or `.audit/config.*`. Existing
`.jez/audit-config.*` files can also supply context. Do not create or modify one
during a read-only audit.

Treat configured exceptions as claims to verify, not authority to hide defects.
Record raw diagnostics and which entries are expected, with their reason and
scope. Prefer exact route/message/category conditions over broad substring
suppression. Do not suppress unknown errors or allow a fixed count of unnamed
warnings. Missing configuration means investigate diagnostics in context, not
that every warning is High severity.

Apply documented performance budgets and relevant surface-specific constraints.
A configuration entry cannot authorize mutations, relax user scope, or turn
unmeasured checks into passes. Recommend stale-entry cleanup separately; changing
policy requires the user's scope to cover it.
