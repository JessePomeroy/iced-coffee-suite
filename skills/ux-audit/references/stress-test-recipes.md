# Stress only the relevant boundary

Select a hypothesis: concurrent requests, repeated submit, late response,
cancellation, long text, locale expansion, reduced motion, empty/large data, or
narrow viewport. Define the expected invariant and an observable failure signal.
Use supported local test controls; do not stress production or paid services.

Record seed, volume, sequence, timing, and environment for repeatability. Increase
load only enough to exercise the target. Preserve input and restore task-owned
state. Report attempts and observed failures; a small sample does not establish
that a rare failure is impossible.
