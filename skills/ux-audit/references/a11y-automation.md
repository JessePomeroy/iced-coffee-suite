# Accessibility evidence

Prefer the project's existing accessibility checks or an available browser tool.
Use an already installed axe integration when present; do not fetch and execute
remote scripts without authority. Record tool/version, tested state, rule, node,
and impact. Automated tools cover only part of accessibility.

Exercise relevant keyboard navigation, focus order/restoration, labels, error
feedback, and supported zoom/reflow. A DOM snapshot does not prove keyboard
operation. Tool severity is evidence; explain the actual user consequence in the
report. If tooling is unavailable, report the manual checks and automated coverage
gap rather than inventing a conformance result.
