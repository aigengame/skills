"""Focused tests for Skills CLI catalog-list validation."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_skills_cli_list import validate_list_output


def create_catalog(root: Path, *names: str) -> None:
    """Create catalog directories for list-output tests."""
    for name in names:
        (root / "skills" / name).mkdir(parents=True)


class ValidateSkillsCliListTests(unittest.TestCase):
    def test_accepts_the_exact_catalog_skill_set(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_catalog(root, "alpha-skill", "beta-skill")
            output = (
                "\x1b[?25h◇  Found 2 skills\n"
                "◇  Available Skills\n"
                "│    beta-skill\n"
                "│\n"
                "│      Beta description.\n"
                "│    alpha-skill\n"
                "│\n"
                "│      Alpha description.\n"
            )

            errors = validate_list_output(root, output)

        self.assertEqual([], errors)

    def test_rejects_a_different_name_set_with_the_same_count(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_catalog(root, "alpha-skill", "beta-skill")
            output = (
                "◇  Found 2 skills\n"
                "◇  Available Skills\n"
                "│    alpha-skill\n"
                "│    gamma-skill\n"
            )

            errors = validate_list_output(root, output)

        self.assertEqual(
            [
                "Skills CLI listed ['alpha-skill', 'gamma-skill']; expected "
                "['alpha-skill', 'beta-skill']"
            ],
            errors,
        )

    def test_ignores_hidden_catalog_directories(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_catalog(root, ".internal", "public-skill")
            output = "◇  Found 1 skill\n│    public-skill\n"

            errors = validate_list_output(root, output)

        self.assertEqual([], errors)

    def test_rejects_an_incorrect_reported_count(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_catalog(root, "alpha-skill")
            output = "◇  Found 2 skills\n│    alpha-skill\n"

            errors = validate_list_output(root, output)

        self.assertEqual(
            ["Skills CLI reported counts [2]; expected [1]"],
            errors,
        )


if __name__ == "__main__":
    unittest.main()
