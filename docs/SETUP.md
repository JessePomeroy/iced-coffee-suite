# Agent adapters

The instructions and skill content are shared; discovery is host-specific.
The installer supports local agents with documented filesystem discovery paths.
Optional `agents/openai.yaml` files are UI metadata, not a runtime dependency.

| Installer target | Skill links | Global instruction link, when requested |
| --- | --- | --- |
| `codex` | `~/.agents/skills/<name>` | `~/.codex/AGENTS.md` |
| `claude` | `~/.claude/skills/<name>` | `~/.claude/CLAUDE.md` |
| `gemini` | `~/.agents/skills/<name>` | `~/.gemini/GEMINI.md` |
| `pi` | `~/.pi/agent/skills/<name>` | `~/.pi/agent/AGENTS.md` |

Codex and Gemini share the same skill destination; selecting both creates one
link per skill. The installer intentionally does not add legacy Codex links or
separate Gemini skill aliases. Existing aliases may still expose another copy:
inspect the host's full discovery list, and do not delete them without authority.

The default paths assume the agents' normal configuration homes. If the user sets
a custom configuration home, use `--skills-dir` and, if needed,
`--instructions-target` with the documented custom paths instead of `--agent`.
The installer does not guess custom environment settings or organization policy.

## Other tools

Verify the tool's current documentation before choosing a discovery directory.
Use `--skills-dir /documented/discovery/path` for skills. Global guidance needs
`--instructions /personal/file --instructions-target /documented/global/file`.
The instruction source must already exist. These are opt-in links, not an attempt
to make every tool understand the same filename.

An agent without skill discovery can still read the relevant `skills/<name>/SKILL.md`
and supporting resources when explicitly directed. This does not automatically
load every package or supply missing tool integrations.

## Operating systems and remote sessions

The installer requires Python 3.10+ and filesystem symlink support. Its automated
apply/remove tests run in isolated directories on Linux. macOS and Windows agent
sessions have not been exercised for this distribution. Windows may require
Developer Mode or another locally approved symlink configuration. A permission
failure is reported; the installer does not elevate or silently fall back to copies.

Local links do not make files available in a cloud session, container, or remote
machine. Install the files in that environment using its supported mechanism.
In particular, Claude Cowork has different import/symlink restrictions from local
Claude Code; this adapter targets local Claude Code, not Cowork.

## Official references

Checked 2026-11-05; recheck when a host changes discovery behavior.

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex global and project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code instructions and shared imports](https://code.claude.com/docs/en/memory)
- [Gemini CLI skills and aliases](https://geminicli.com/docs/cli/skills/)
- [Gemini CLI global context](https://geminicli.com/docs/cli/gemini-md/)
- [Rhubarb's Pi integration guide](https://github.com/JessePomeroy/rhubarb/blob/main/GLOBAL-CONFIG.md)
