# Choose checks for the scoped task

Start at the user's real entry point. Verify discovery, required inputs, primary
action, pending state, completion feedback, and the resulting state. Where
relevant, exercise cancel/back, validation, empty/error/loading states, reload,
and persistence. Check keyboard navigation and focus for affected controls.

Select controls by role/label or stable project handles. Disabled actions may be
correct; establish preconditions. Clipboard writes, downloads, native dialogs,
and focus changes need the appropriate observer, not necessarily DOM/network
changes. Do not submit externally visible actions without authority.

Inspect layout at device states relevant to the brief. Use screenshots and
rendered measurements; source CSS is insufficient. Check console/network signals
around a failure and trace actual impact before assigning severity.
