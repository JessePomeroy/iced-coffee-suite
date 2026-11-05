# Adapt to the available browser

Use the host's browser documentation and supported tools. Do not assume Chrome
MCP, Playwright MCP, Pi wrappers, or a `page` object is available. Discover the
actual tool surface first. For a project harness, prefer its documented commands.

Navigate to the intended instance, health-check it, inspect current controls,
perform the real interaction, and observe the outcome. Refresh references after
DOM/navigation changes. Source evaluation may inspect state but must not replace
a user action with an internal setter and claim equivalence.

Report unavailable console/network/trace/touch capabilities rather than inventing
calls. Screenshots do not prove touch input. Preserve session ownership and use
isolated test instances for parallel driving. Stop only processes started here.
