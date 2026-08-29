"""Focused tests for the repository-owned skill catalog validator."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_catalog import validate_catalog


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def write_skill(
    root: Path,
    directory_name: str,
    *,
    frontmatter: str | None = None,
    body: str = "# Test skill\n",
) -> Path:
    """Create one test skill and return its directory."""
    skill_directory = root / directory_name
    skill_directory.mkdir()
    if frontmatter is None:
        frontmatter = (
            "---\n"
            f"name: {directory_name}\n"
            "description: A focused test skill.\n"
            "---\n"
        )
    (skill_directory / "SKILL.md").write_text(
        f"{frontmatter}\n{body}", encoding="utf-8"
    )
    return skill_directory


class ValidateCatalogTests(unittest.TestCase):
    def test_current_catalog_is_valid(self) -> None:
        skill_count, errors = validate_catalog(REPOSITORY_ROOT)

        self.assertGreater(skill_count, 0)
        self.assertEqual([], errors)

    def test_rejects_a_top_level_skill_without_skill_md(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "missing-skill").mkdir()
            (root / "docs").mkdir()

            skill_count, errors = validate_catalog(root)

        self.assertEqual(1, skill_count)
        self.assertEqual(
            ["missing-skill/SKILL.md: file is missing"],
            errors,
        )

    def test_rejects_malformed_frontmatter(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_skill(
                root,
                "broken-frontmatter",
                frontmatter=(
                    "---\n"
                    "name: broken-frontmatter\n"
                    "description: [missing closing bracket\n"
                    "---\n"
                ),
            )

            _, errors = validate_catalog(root)

        self.assertEqual(
            ["broken-frontmatter/SKILL.md: frontmatter is not valid YAML"],
            errors,
        )

    def test_rejects_a_name_that_does_not_match_its_directory(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_skill(
                root,
                "expected-name",
                frontmatter=(
                    "---\n"
                    "name: another-name\n"
                    "description: The name does not match.\n"
                    "---\n"
                ),
            )

            _, errors = validate_catalog(root)

        self.assertEqual(
            [
                "expected-name/SKILL.md: frontmatter name 'another-name' "
                "does not match directory 'expected-name'"
            ],
            errors,
        )

    def test_rejects_a_broken_relative_reference(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_skill(
                root,
                "broken-reference",
                body="Read [the reference](REFERENCE.md).\n",
            )

            _, errors = validate_catalog(root)

        self.assertEqual(
            [
                "broken-reference/SKILL.md: relative reference "
                "'REFERENCE.md' does not name a repository file"
            ],
            errors,
        )

    def test_accepts_supported_folded_description_and_existing_reference(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_directory = write_skill(
                root,
                "folded-description",
                frontmatter=(
                    "---\n"
                    "name: folded-description\n"
                    "description: >-\n"
                    "  A supported folded description that spans\n"
                    "  more than one source line.\n"
                    "---\n"
                ),
                body="Read [the reference](REFERENCE.md#details).\n",
            )
            (skill_directory / "REFERENCE.md").write_text(
                "# Details\n", encoding="utf-8"
            )

            skill_count, errors = validate_catalog(root)

        self.assertEqual(1, skill_count)
        self.assertEqual([], errors)

    def test_accepts_supported_optional_frontmatter(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_skill(
                root,
                "optional-frontmatter",
                frontmatter=(
                    "---\n"
                    "name: optional-frontmatter\n"
                    "description: The optional fields follow the Agent Skills specification.\n"
                    "license: MIT\n"
                    "compatibility: Requires Python 3.9 or newer.\n"
                    "metadata:\n"
                    "  owner: aigengame\n"
                    "allowed-tools: Read\n"
                    "---\n"
                ),
            )

            skill_count, errors = validate_catalog(root)

        self.assertEqual(1, skill_count)
        self.assertEqual([], errors)

    def test_rejects_an_unsupported_frontmatter_field(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_skill(
                root,
                "unsupported-field",
                frontmatter=(
                    "---\n"
                    "name: unsupported-field\n"
                    "description: The extra field is not supported.\n"
                    "owner: aigengame\n"
                    "---\n"
                ),
            )

            _, errors = validate_catalog(root)

        self.assertEqual(
            [
                "unsupported-field/SKILL.md: unsupported frontmatter field "
                "'owner'"
            ],
            errors,
        )


if __name__ == "__main__":
    unittest.main()
