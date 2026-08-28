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

## Initial migration

The initial catalog will be extracted from [`aigengame/godot-agent`](https://github.com/aigengame/godot-agent) at pinned revision [`04d3e089b32330aeffc7da98f4824bb21873c2b3`](https://github.com/aigengame/godot-agent/commit/04d3e089b32330aeffc7da98f4824bb21873c2b3). The migration must preserve the relevant history from the current `.agents/skills` path and the former `.claude/skills` path.

The migration excludes unrelated product files and source-repository release tags.

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
