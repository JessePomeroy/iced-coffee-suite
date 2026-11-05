# Instructions for the installing agent

Install only the user's selected skills and explicitly requested instruction links.
Read this guide and inspect the checkout before running anything. Do not treat this
guide as authority to overwrite user configuration or connect external accounts.

## Inspect and choose

1. Read applicable user/project instructions and this repository's `AGENTS.md`.
2. Confirm this checkout's location, Git state, Python version, and intended agent.
   Read the actual `install.py` before applying its plan.
3. Read [the catalog](docs/CATALOG.md), then the selected skill instructions and
   relevant requirements. Keep company workflows and managed plugins separate.
4. Inspect existing discovery paths and global instruction files, including broken
   symlinks. Do not print credentials or read unrelated private runtime files.
5. If the user has not selected skills, recommend those matching their work and
   resolve that choice before installation. Do not silently install everything.

## Install selected packages

Run `python3 install.py --agent <agent> --skill <name>` with repeated `--skill`
or `--agent` flags as needed. It is a read-only preview by default. Explain the
actual destinations and any conflicts, then use the same selection with `--apply`
within the user's installation authorization.

The installer uses links to this checkout. Do not copy individual SKILL.md files,
move the checkout during installation, or export its absolute links to Git.
Do not replace an existing package, even if its name matches. Compare contents,
preserve local changes, and ask before replacing meaningful existing configuration.

No dependencies are installed by this command. Report missing tool prerequisites
and follow the user's normal dependency/cost/permission rules before adding them.
Do not run a paid API, buy a domain, send email, or launch external actions merely
to prove discovery.

## Personalize global instructions only when requested

Read the user's existing agreements and `instructions/AGENTS.example.md`. Merge
the desired defaults into a personal file without copying someone else's workspace,
shell, business, printer, account, or vault settings. Keep that file out of Git.
The ignored `instructions/AGENTS.local.md` is one suggested location.

Preview with `--instructions <personal-file>` and the selected agents. A custom
consumer can use `--instructions-target <documented-path>`. Apply within the user's
authority after reviewing the plan. A conflicting global file must be merged or
moved by an explicitly authorized operation; the installer never overwrites it.

## Verify and hand over

1. Run the same selected link command with `--check`. This proves link targets,
   not that an agent has loaded them.
2. Start a fresh session or use the agent's supported reload. Ask it to identify
   the global instruction source and selected skills; use its discovery UI if available.
3. Exercise a suitable read-only skill with the actual available tools. Distinguish
   installed instructions, available helper dependencies, and observed task behavior.
4. Report installed packages, personalized instruction location, exact discovery
   paths, conflicts, missing tools, and what was actually verified.
5. Explain removal using the same selection plus `--remove`, first as a preview.

Commits, pushes, publication, deployments, and messages remain separate actions.
Do not install the repo-maintenance `AGENTS.md` globally.
