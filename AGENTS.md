# Repository guidance

## Purpose and scope

This repository is the shared upstream for reusable Agent Skills maintained by aigengame. It publishes the catalog as a Git source for the Vercel Skills CLI. Add a skill here only when its guidance is reusable across repositories. A shared skill can operate on consumer-owned project files at runtime, but it must not embed one consumer's private policy or configuration.

Repository changes can cover catalog content, validation, release automation, release metadata, and usage documentation. Changes to another repository are outside this repository's scope.

## Repository layout

All skills live under `skills/`. Each non-hidden directory directly under `skills/` is one skill. Its `SKILL.md` is required, and its optional scripts, references, assets, templates, and agent metadata stay inside that directory. Repository infrastructure stays outside `skills/`.

Read `README.md` for the public repository contract and validation setup. Follow `CONTRIBUTING.md` when you add, change, rename, or remove a skill.

## Language

Write tracked files, commit messages, issues, pull requests, and review comments in English. Use ASD-STE100 Simplified Technical English as the default writing reference for technical prose. Use the user's preferred language for direct conversation.

## Required validation and review

Before you propose a merge:

1. Read the complete changed skill and each affected bundled resource.
2. Keep catalog changes separate from changes to other repositories.
3. Run `python -m unittest discover -s tests -v`.
4. Run `python scripts/validate_catalog.py`.
5. Confirm that GitHub Actions passes and that a maintainer reviews the change.

Do not treat passing validation as proof that a skill is correct or reusable. Review its instructions, selection description, relative references, terminology, and prose.
