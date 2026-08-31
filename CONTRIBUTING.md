# Contributing

## Scope and ownership

This repository accepts Agent Skills whose guidance is reusable across repositories. Bundle each skill's reusable resources inside its skill directory. A shared skill can operate on consumer-owned project files at runtime, but it must not embed one consumer's private policy or configuration. Changes to other repositories are outside this repository's scope.

aigengame maintainers own catalog acceptance, publication, and review. Contributors own the accuracy and completeness of their proposed changes. See `README.md` for the supported catalog publication and usage flow.

## Make a skill change

### Add a skill

- Create one top-level directory whose name matches the `name` in `SKILL.md`.
- State what the skill does and when to use it in the frontmatter description. Explain the cross-repository use case in the pull request.
- Bundle only the scripts, references, assets, templates, or agent metadata that the skill needs.
- Use relative links for bundled files.

### Change a skill

- Read the complete `SKILL.md` and each affected bundled resource before editing.
- Keep the frontmatter description, instructions, resources, and relative links consistent.
- Describe required project inputs generically. Do not embed one consumer's private policy or configuration.

### Rename a skill

- Move the complete skill directory and update the frontmatter `name` in the same change.
- Update repository references to the old name.
- State the old name, new name, and expected catalog compatibility impact in the pull request.

### Remove a skill

- Remove the complete skill directory and its repository references.
- State why the shared skill is no longer maintained and describe known catalog compatibility impact in the pull request.

## Validate and review

Follow the environment setup in `README.md`, then run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_catalog.py
```

Both commands and the `Skill catalog` GitHub Actions check must pass before merge. A maintainer must review each skill change for reusable scope, correct instructions, accurate frontmatter, valid bundled resources, consistent terminology, and clear prose.

Passing automated checks is structural evidence only. The review must also confirm that the skill fulfills its declared purpose without embedding one consumer's private policy or configuration.

## Pull requests

Keep a pull request to one logical catalog change. State whether it adds, changes, renames, or removes a skill; explain the reusable need and catalog compatibility impact; and report the validation commands that ran.
