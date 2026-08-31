# Contributing

## Scope and ownership

This repository accepts Agent Skills that are reusable across repositories. Keep project-specific private skills, repository-specific `STATE.md` and `PITFALLS.md` files, and consumer configuration in the consumer repository that owns them.

aigengame maintainers own catalog acceptance and review. Contributors own the accuracy and completeness of their proposed changes. Each consumer repository owns how it installs or exposes shared skills, including submodules, symbolic links, vendoring, plugins, or another method. Do not include consumer integration changes in this repository.

## Make a skill change

### Add a skill

- Create one top-level directory whose name matches the `name` in `SKILL.md`.
- State what the skill does and when to use it in the frontmatter description. Explain the cross-repository use case in the pull request.
- Bundle only the scripts, references, assets, templates, or agent metadata that the skill needs.
- Use relative links for bundled files.

### Change a skill

- Read the complete `SKILL.md` and each affected bundled resource before editing.
- Keep the frontmatter description, instructions, resources, and relative links consistent.
- Keep consumer-specific assumptions out of the shared skill.

### Rename a skill

- Move the complete skill directory and update the frontmatter `name` in the same change.
- Update repository references to the old name.
- State the old name, new name, and expected consumer impact in the pull request.

### Remove a skill

- Remove the complete skill directory and its repository references.
- State why the shared skill is no longer maintained and describe known consumer impact in the pull request.
- Do not remove consumer copies or change consumer integration as part of this repository change.

## Validate and review

Follow the environment setup in `README.md`, then run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_catalog.py
```

Both commands and the `Skill catalog` GitHub Actions check must pass before merge. A maintainer must review each skill change for reusable scope, correct instructions, accurate frontmatter, valid bundled resources, consistent terminology, and clear prose.

Passing automated checks is structural evidence only. The review must also confirm that the skill fulfills its declared purpose without depending on private consumer context.

## Pull requests

Keep a pull request to one logical catalog change. State whether it adds, changes, renames, or removes a skill; explain the reusable need and consumer impact; and report the validation commands that ran.
