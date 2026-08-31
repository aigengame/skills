# Repository guidance

## Purpose and scope

This repository is the shared upstream for reusable Agent Skills maintained by aigengame. Add a skill here only when it is useful beyond one consumer repository. Keep repository-specific private skills in the consumer that owns them.

Do not implement or prescribe a consumer installation method here. Each consumer owns its submodule, symbolic-link, vendoring, plugin, or other integration choice.

## Repository layout

Each skill has one non-hidden top-level directory. Its `SKILL.md` is required, and its optional scripts, references, assets, templates, and agent metadata stay inside that directory. Repository infrastructure lives in `.github`, `docs`, `scripts`, and `tests`.

Read `README.md` for the public repository contract and validation setup. Follow `CONTRIBUTING.md` when you add, change, rename, or remove a skill.

## Language

Write tracked files, commit messages, issues, pull requests, and review comments in English. Use ASD-STE100 Simplified Technical English as the default writing reference for technical prose. Use the user's preferred language for direct conversation.

## Required validation and review

Before you propose a merge:

1. Read the complete changed skill and each affected bundled resource.
2. Keep reusable skill changes separate from consumer-repository changes.
3. Run `python -m unittest discover -s tests -v`.
4. Run `python scripts/validate_catalog.py`.
5. Confirm that GitHub Actions passes and that a maintainer reviews the change.

Do not treat passing validation as proof that a skill is correct or reusable. Review its instructions, selection description, relative references, terminology, and prose.
