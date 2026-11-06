# Iced Coffee Suite

Reusable working agreements and skills for local coding agents. Keep one editable
skill checkout, then link selected packages into each agent's discovery directory.

There are 26 top-level packages, including Bug Hunter's 10 nested workflows.
The [catalog](docs/CATALOG.md) explains when to use each skill, why it exists, and
which tools it needs. [Sources and licenses](SOURCES.md) distinguish maintained
local editions from their upstream projects.

## Start here

Ask your agent to follow [INSTALL.md](INSTALL.md), or inspect the installer yourself.
Python 3.10+ is the only requirement for the installer; it uses the standard library
and never downloads dependencies, authenticates accounts, or runs a skill's helpers.
Clone the public repository, then run commands from its checkout. Examples use
zsh-compatible syntax.

```zsh
git clone https://github.com/JessePomeroy/iced-coffee-suite.git
cd iced-coffee-suite
```

```zsh
python3 install.py --list
python3 install.py --agent codex --skill diagnosing-bugs --skill blast-radius
```

The second command previews links without creating files. After reviewing the plan:

```zsh
python3 install.py --agent codex --skill diagnosing-bugs --skill blast-radius --apply
python3 install.py --agent codex --skill diagnosing-bugs --skill blast-radius --check
```

Use `--agent claude`, `--agent gemini`, or `--agent pi` for another supported local
agent. Repeat `--agent` to share the same packages across agents. For another tool,
use its documented discovery directory with `--skills-dir /path/to/skills`.
Choose relevant skills before using `--all`; a larger discovery list costs context.

For a Codex host that also needs the older `~/.codex/skills` location, add
`--codex-compat` to the same preview, apply, check, and removal commands. Both
links point to one package; this option does not copy skill contents. The default
shared path remains `~/.agents/skills`. See [adapter details](docs/SETUP.md).

`--check` verifies links. To check whether a fresh local Codex CLI actually lists
the selected manifests from this checkout, run:

```zsh
python3 scripts/check_codex_discovery.py --skill diagnosing-bugs --skill blast-radius --cwd /path/to/project
```

This separate diagnostic makes no model request. It reports missing, disabled,
and differently sourced skills; refresh the agent session you intend to use too.

No existing file, directory, or unrelated symlink is overwritten. Conflicts stop
the entire plan before changes; compare and merge them manually. If link creation
fails partway through, newly created links are rolled back. Empty parent directories
may remain. Removal also checks every selected target before changing anything.

## Share working agreements

`AGENTS.md` at the repository root is for maintaining this repo. **Do not install it
as your global instructions.** Start with
[the personal instruction template](instructions/AGENTS.example.md), merge your
preferences, and keep the result in a personal file such as the ignored
`instructions/AGENTS.local.md`. Do not overwrite existing agreements to create it.

Once that personalized file exists, preview its links:

```zsh
python3 install.py --agent codex --agent claude --instructions instructions/AGENTS.local.md
```

Add `--apply` only after reviewing the plan. Global instructions are entirely opt-in;
installing skills alone does not change them. Repository-specific instructions stay
in each project. See [agent adapters and limitations](docs/SETUP.md).

## Use a skill

Ask naturally: “Use diagnosing-bugs to investigate this error; do not edit files.”
Or explicitly select the skill using your agent's supported skill command.
A matching description can also trigger a skill automatically; some packages
retain an explicit-invocation policy supported by particular hosts.

Read the selected skill, resolve helper paths relative to its installed `SKILL.md`,
and use the active agent's actual tools. Skills do not grant permission for edits,
delegation, paid calls, Git actions, publishing, or access to other people's data.

For specification-driven work, `slice-loop-workflow` follows one ordered slice
through implementation, independent PR review, authorized merge, and required
Obsidian closeout. It is an instruction skill and does not require a named
workflow launcher. Configure the specification, handoff, and vault for your project.

## Update or remove

Keep this checkout at a stable path: links point to it. Review Git state and the
upstream diff before pulling; preserve your local edits. Updating this checkout
changes the files linked agents can read after their appropriate reload.
Your personalized instructions are separate and should be reviewed independently.

To preview removal, repeat the original selection with `--remove`:

```zsh
python3 install.py --agent codex --skill diagnosing-bugs --skill blast-radius --remove
```

Add `--apply` to remove matching links. Source packages and personalized instruction
files are kept. An entry pointing elsewhere is a conflict and is left alone.
If installation used `--codex-compat`, repeat it during removal to select both roots.
If you move the checkout, inspect and remove the old links before relinking; the
installer will not adopt or replace links to another checkout automatically.

## Verify the distribution

```zsh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
```

These check packaging, catalog consistency, and installer behavior in isolated
directories. They do not claim every workflow ran in every agent or that optional
external services are configured. See [verification](docs/VERIFY.md).

Rhubarb is an optional [Pi configuration](https://github.com/JessePomeroy/rhubarb)
providing extensions and tools. It is not required for this collection.
