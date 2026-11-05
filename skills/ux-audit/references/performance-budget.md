# Performance evidence

Use the project's existing performance tests, trace tools, or supported
`web-vitals` collector. Do not implement INP as max(event.duration), CLS as the
sum of all shifts, or missing observations as zero. No inline approximation in
this skill is a substitute for the metric's implementation.

1. Define the route, user interaction, build, browser, viewport, account/data
   state, cache state, and any real CPU/network throttling.
2. Prefer a collector already installed in the project. If none exists, use
   available browser profiling to report directly observed timings and long
   tasks under their actual names. Report CWV metrics as unmeasured. Installing
   a measurement dependency or injecting a remote script needs appropriate
   authority; never fetch and execute CDN code merely to complete a checklist.
3. Start collection before the relevant navigation and interactions, using the
   collector's documented lifecycle. Capture its final measurement after the
   flow. Preserve its metric name, unit, measured interval, and attribution.
4. For an improvement claim, repeat baseline and candidate under equivalent
   conditions and report samples and variability. One unthrottled run is not a
   prediction for all users or a production percentile.
5. Disconnect observers/stop traces started by the audit and retain the results.

An absent LCP entry or a page with no qualifying interaction has no measured LCP
or INP result for this run. Use `unmeasured` with a reason, not `0` or a green
badge. Unsupported APIs likewise remain unmeasured. Only report zero when the
measurement method establishes a real zero. A request delay does not emulate
CPU throttling or realistic network bandwidth. Do not report TTI from DOMContentLoaded.

Use a project-agreed budget. Without one, present measurements and user-visible
latency evidence; do not invent a universal release gate. Performance is one
part of the scoped result, and missing requested measurements limit coverage.

Primary definitions and reference implementation:
- https://web.dev/articles/inp
- https://web.dev/articles/cls
- https://github.com/GoogleChrome/web-vitals
