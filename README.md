# aigengame/skills

Reusable Agent Skills maintained by aigengame.

## Purpose

This repository is the shared upstream for reusable Agent Skills maintained by aigengame. It gives maintainers and contributors one place to review, validate, publish, and evolve skills that are useful across repositories.

## Repository layout

Each skill uses one directory under `skills/`:

```text
skills/
└── <skill-name>/
    ├── SKILL.md
    ├── agents/       # Optional agent metadata
    ├── scripts/      # Optional executable resources
    ├── references/   # Optional reference documents
    ├── assets/       # Optional static assets
    └── templates/    # Optional reusable templates
```

`SKILL.md` is required. A skill can include only the bundled resources that it needs. Repository infrastructure stays outside `skills/`.

## Use the catalog

This repository is a Git source for the [Vercel Skills CLI](https://github.com/vercel-labs/skills). List the available skills without installing them:

```bash
npx skills add aigengame/skills --list
```

Start an interactive project-level installation:

```bash
npx skills add aigengame/skills
```

Install one named skill at project level or global user level:

```bash
npx skills add aigengame/skills --skill artifact-review
npx skills add aigengame/skills --skill artifact-review --global
```

The Skills CLI also accepts explicit agent and install-mode options. Run `npx skills add --help` for the current option set. Scope, target agent, and install mode are selected at installation time.

The `skills` package executed by `npx` is the Vercel CLI. The skill content comes directly from this Git repository; `aigengame/skills` does not publish a separate npm package. A selected installation contains the selected skill payload, not repository infrastructure such as `.github`, `docs`, `scripts`, or `tests`.

A source without a Git ref resolves the repository's current default branch when the command runs. It is a floating source, and an existing installation does not update automatically. An immutable catalog release uses a full SemVer tag in the form `vX.Y.Z`. After a tagged release is available, select a tag from [GitHub Releases](https://github.com/aigengame/skills/releases) and append it to the source as `aigengame/skills#vX.Y.Z`. For a reproducible installation, also use the Skills CLI version recorded for that release.

## Publishing

Issue [#10](https://github.com/aigengame/skills/issues/10) tracks the first tagged release and its automation. The planned release contract makes Release Please the only authority that creates catalog tags and GitHub Releases. Each release is one immutable repository revision with a full SemVer tag in the form `vX.Y.Z`; tags do not include a component prefix.

The planned release flow is:

1. merge reviewed catalog changes only after the required GitHub Actions check passes;
2. let Release Please create or update its release pull request;
3. review and merge the release pull request;
4. validate the exact resulting `main` revision with the catalog checks and a pinned Skills CLI version before Release Please can create a tag;
5. let Release Please create the `vX.Y.Z` tag and GitHub Release; and
6. in the same workflow, confirm that the emitted tag resolves to the validated revision and install a selected skill from that tag.

Until issue #10 is complete, this repository has no supported stable release tag and the commands above resolve the default branch. The first planned release is `v0.1.0`; do not present it as available until its tagged smoke validation passes.

## Validation

The catalog validator checks every non-hidden directory directly under `skills/`. It requires a readable `SKILL.md`, validates the supported Agent Skills frontmatter fields, requires the frontmatter name to match the directory, and checks relative Markdown links to bundled files.

Supported frontmatter consists of required `name` and `description` fields and the optional `license`, `compatibility`, `metadata`, and `allowed-tools` fields defined by the [Agent Skills specification](https://agentskills.io/specification). Repository infrastructure outside `skills/` is not part of the catalog.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for skill ownership, change, validation, and review rules.

## License

This repository is available under the [MIT License](LICENSE).

## Initial migration

The initial catalog was extracted from [`aigengame/godot-agent`](https://github.com/aigengame/godot-agent) at pinned revision [`04d3e089b32330aeffc7da98f4824bb21873c2b3`](https://github.com/aigengame/godot-agent/commit/04d3e089b32330aeffc7da98f4824bb21873c2b3). The import preserves the relevant history from the current `.agents/skills` path and the former `.claude/skills` path.

The migration excludes unrelated product files and source-repository release tags. See the [migration record](docs/migrations/2026-08-28-godot-agent.md) for the commands and evidence.
