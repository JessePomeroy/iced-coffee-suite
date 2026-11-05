# Testprune (local adaptation)

Audit or improve a test suite while preserving supported behavior, offline
execution, and the repository's runner and environment. This installed copy
adapts the upstream skill to local permission and verification rules.

Read [SKILL.md](SKILL.md) for the current workflow. An audit is read-only;
requested cleanup may edit the scoped tests/configuration. Prompt-first work
produces a plan, and follow-ups act only on named authorized items.

No universal runtime reduction is promised. Compare equivalent checks before
and after. A focused selector is not evidence that the entire suite got faster.
Do not replace the default test command or synchronize instruction files unless
that change is requested.

The [inventory helper](scripts/test_inventory.py) includes hidden project folders
but excludes common dependency/build folders. It finds candidate files, not the
runner's collected test cases. Check custom patterns and runner configuration.
The [gate template](references/gate_script_template.sh) is an optional pytest
example; other stacks should use their existing scripts.

Original project: https://github.com/NeuraCerebra-AI/testprune
License: [MIT](LICENSE). Historical illustrative assets remain upstream material;
current behavior is defined by the local skill, not those illustrations.
