# aigengame/skills

Reusable Agent Skills maintained by aigengame.

> [!IMPORTANT]
> This repository is being bootstrapped. It is not ready for consumer use until the [readiness review](https://github.com/aigengame/skills/issues/5) is complete.

## Purpose

This repository is the shared upstream for reusable Agent Skills maintained by aigengame. It gives maintainers and contributors one place to review, validate, and evolve skills that are useful across repositories.

Repository-specific private skills remain owned by their consumer repositories.

## Repository layout

Each skill uses one top-level directory:

```text
<skill-name>/
├── SKILL.md
├── agents/       # Optional agent metadata
├── scripts/      # Optional executable resources
├── references/   # Optional reference documents
├── assets/       # Optional static assets
└── templates/    # Optional reusable templates
```

`SKILL.md` is required. A skill can include only the bundled resources that it needs.

## Validation

The catalog validator checks every top-level skill directory. It requires a readable `SKILL.md`, validates the supported Agent Skills frontmatter fields, requires the frontmatter name to match the directory, and checks relative Markdown links to bundled files.

Supported frontmatter consists of required `name` and `description` fields and the optional `license`, `compatibility`, `metadata`, and `allowed-tools` fields defined by the [Agent Skills specification](https://agentskills.io/specification). Repository infrastructure lives in `.github`, `docs`, `scripts`, and `tests`; other non-hidden top-level directories are treated as skills.

Python 3.10 or newer is required. Create a local environment and install the pinned validator dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the focused tests and validate the complete catalog:

```bash
python -m unittest discover -s tests -v
python scripts/validate_catalog.py
```

A valid checkout ends the catalog command with:

```text
Catalog validation passed.
```

## Initial migration

The initial catalog was extracted from [`aigengame/godot-agent`](https://github.com/aigengame/godot-agent) at pinned revision [`04d3e089b32330aeffc7da98f4824bb21873c2b3`](https://github.com/aigengame/godot-agent/commit/04d3e089b32330aeffc7da98f4824bb21873c2b3). The import preserves the relevant history from the current `.agents/skills` path and the former `.claude/skills` path.

The migration excludes unrelated product files and source-repository release tags. See the [migration record](docs/migrations/2026-08-28-godot-agent.md) for the commands and evidence.

Track the bootstrap work in these issues:

- [Import shared skill history](https://github.com/aigengame/skills/issues/2)
- [Add catalog validation](https://github.com/aigengame/skills/issues/3)
- [Establish governance](https://github.com/aigengame/skills/issues/4)
- [Review migration evidence and readiness](https://github.com/aigengame/skills/issues/5)

## Consumer integration

Each consumer repository chooses and maintains its own integration mechanism. A consumer can use a submodule, symbolic links, vendoring, a plugin, or another mechanism that fits its requirements.

This repository does not create or maintain consumer-side paths. It also does not prevent a consumer from keeping its own project-scoped skills in `.agents/skills` or another local directory.

## Current status

The repository contract is tracked in [issue #1](https://github.com/aigengame/skills/issues/1). Do not add this repository as a consumer dependency until the [readiness review](https://github.com/aigengame/skills/issues/5) records a ready decision.
