# Mytho Compendium — shared omp capability pack

Shared custom agents, slash commands, skills, and rules for all three
Mytho Compendium repos (MCA, MCC, MCS). This is an omp **extension package**:
a plain directory with an entry point (`index.ts`) plus sibling capability
directories that omp's `omp-plugins` discovery provider scans once the
package loads.

## Why it lives in MCC

Custom agents/commands/skills/rules are discovered per-repository in omp
(`.omp/agents`, `.omp/commands`, `.omp/skills`, `.omp/rules` — no ancestor
walk-up, unlike `AGENTS.md`/`CLAUDE.md`). Three separate git repos can't share
a native `.omp/` location. Packaging the shared set as an extension here and
pointing every repo's `extensions:` setting at it is the supported way to
reuse one set of files across independent repos without duplication.

## Wiring

Each of the three repos' `.omp/config.yml` lists this directory, relative to
that repo's own root (MCA/MCS point at the sibling repo; MCC points at
itself):

```yaml
# mytho-compendium-app/.omp/config.yml
# mytho-compendium-server/.omp/config.yml
extensions:
  - ../mytho-compendium-content/omp-shared

# mytho-compendium-content/.omp/config.yml
extensions:
  - ./omp-shared
```

`extensions:` relative paths resolve against the session's **cwd**, not
against the config file's own directory, and there is no ancestor walk-up.
This only resolves correctly when omp is launched from that repo's own root
directory — the normal case, but worth knowing if you ever start a session
from a subdirectory. Use an absolute path instead if that's a problem for
your workflow (at the cost of portability across machines/checkout
locations).

MCC lists itself too — self-referencing keeps behavior identical across all
three repos instead of relying on native `.omp/extensions/` auto-discovery,
whose sibling-directory scanning rules are undocumented for that path.

## IMPORTANT — do not add documentation files inside the capability directories

`agents/`, `commands/`, `skills/`, and `rules/` below are scanned as **live
data**, not browsed as docs: every `*.md` file directly under `agents/`,
`commands/`, and `rules/` is parsed as a real definition, and every
`<name>/SKILL.md` one level under `skills/` is parsed as a real skill.

- A stray `commands/README.md` registers a working `/README` slash command
  (filename = command name, no opt-out). Same failure mode applies to Claude
  Code's `.claude/commands/**/*.md`, which is recursive — a `CLAUDE.md`
  anywhere under there becomes `/CLAUDE` or a namespaced alias.
- A stray `agents/README.md` fails `name`/`description` frontmatter parsing
  and is silently skipped with a logged warning — harmless but noisy.
- A stray `rules/README.md` registers as an unnamed/undescribed rule entry.
- A loose file directly under `skills/` (not inside `skills/<name>/SKILL.md`)
  is the one case that's actually inert, since skill scanning only matches
  one level of subdirectory.

Keep all documentation here, in this top-level `README.md`, which no
discovery provider scans.

## Layout and naming

```
omp-shared/
  index.ts        <- required entry point, registers nothing itself
  README.md       <- this file — the only doc file in the package
  agents/          <- <agent-name>.md
  commands/        <- <command-name>.md
  skills/          <- <skill-name>/SKILL.md
  rules/           <- <rule-name>.md
```

### Agents — `agents/<agent-name>.md`

```md
---
name: my-agent
description: One line — when task/hub should pick this agent.
tools: read, grep, glob, bash          # optional, CSV or YAML list
spawns: "*"                            # optional: "*" | CSV | list | "" (no subagents)
model: anthropic/claude-sonnet-4-5     # optional, one selector or a list tried in order
thinking-level: high                   # optional
output: {}                             # optional JSON-schema for structured output
autoloadSkills: [some-skill]           # optional, injected before the child's first prompt
---

System prompt body for the agent goes here.
```

`name` and `description` are required — a file missing either is skipped with
a warning, not a hard failure. Dispatch by name from `task`:
`{ "tasks": [{ "agent": "my-agent", "task": "..." }] }`.
Full frontmatter contract: `omp://task-agent-discovery.md`.

### Commands — `commands/<command-name>.md`

```md
---
description: Short description shown in autocomplete (optional — else first body line, 60 chars)
---

Review $1 against the coding standard in @../../CLAUDE.md.

Everything after $2 is context: $@[2]
```

No `name` field — the filename (minus `.md`) is the command name
(`command-name.md` -> `/command-name`). Non-recursive: only
`commands/*.md`, not subdirectories. Substitutions: `$1`, `$2`, ...,
`$@[start]` / `$@[start:length]`, `$ARGUMENTS` / `$@`.

### Skills — `skills/<skill-name>/SKILL.md`

One directory per skill, one level deep. Nested paths like
`skills/group/<skill>/SKILL.md` are **not** discovered.

```
skills/
  ticket-triage/
    SKILL.md
    reference/
      scoring-table.md      <- fetched via skill://ticket-triage/reference/scoring-table.md
```

```md
---
name: ticket-triage
description: Use when creating or scoring a backlog ticket. Covers ticket anatomy and the estimation matrix.
globs: ["**/*.ticket.md"]      # optional
alwaysApply: false             # optional
hide: false                    # optional — hidden skills stay reachable via skill://, just not listed
---

Body content: the workflow/knowledge the agent reads on demand via the
`read` tool (`skill://ticket-triage`) or `/skill:ticket-triage`.
```

`name` and `description` are both **required** — this package's skills are
discovered with `requireDescription: true`, same as native `.omp/skills`.

### Rules — `rules/<rule-name>.md`

```md
---
description: One line — when this rule applies (used for model-triggered attachment)
globs: ["**/*.kt"]          # optional — auto-attach when matching files are in context
alwaysApply: false          # optional — true makes it always-attach, not just on request/glob match
---

The rule body — a hard constraint or convention, not general background
(general background belongs in CLAUDE.md instead).
```

Readable as `rule://<rule-name>`. Unlike the top-level sticky `RULES.md`
(native-only, always-apply, no frontmatter override), files here support
conditional/opt-in behavior via `globs`/`alwaysApply`, and — because this
package loads through `extensions:` — apply in all three repos that
reference it.

## After editing

Restart the omp session (or `/reload-plugins`) in MCA/MCC/MCS to pick up
changes — there is no file watcher for these directories.
