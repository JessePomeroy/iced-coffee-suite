# Observe the intended effect

For a control, establish its expected effect, perform the actual user action,
and verify that effect. Check DOM, network, focus, clipboard, downloads, native
UI, or persisted state as appropriate. No DOM/request change alone is not a bug.

A form can be correctly blocked by native validity. A disabled action can be
intentional. Trace event handling and prerequisites before blaming wiring. For
async actions, distinguish pending feedback, request success, and persisted
completion. Verify reload or a second view when that is the real contract.
