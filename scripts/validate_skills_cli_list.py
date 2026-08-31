#!/usr/bin/env python3
"""Check that Skills CLI list output contains the exact catalog skill set."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
FOUND_COUNT_PATTERN = re.compile(r"\bFound ([0-9]+) skills?\b")
SKILL_LINE_PATTERN = re.compile(
    r"^\s*│ {4}([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", re.MULTILINE
)


def catalog_skill_names(root: Path) -> list[str]:
    """Return the sorted names of non-hidden catalog skill directories."""
    catalog_root = root / "skills"
    if not catalog_root.is_dir():
        return []
    return sorted(
        path.name
        for path in catalog_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def validate_list_output(root: Path, output: str) -> list[str]:
    """Return errors when CLI output differs from the repository catalog."""
    expected_names = catalog_skill_names(root)
    plain_output = ANSI_ESCAPE_PATTERN.sub("", output)
    reported_counts = [
        int(match.group(1)) for match in FOUND_COUNT_PATTERN.finditer(plain_output)
    ]
    listed_names = SKILL_LINE_PATTERN.findall(plain_output)

    errors: list[str] = []
    expected_count = len(expected_names)
    if reported_counts != [expected_count]:
        errors.append(
            f"Skills CLI reported counts {reported_counts!r}; expected "
            f"[{expected_count}]"
        )
    if sorted(listed_names) != expected_names:
        errors.append(
            f"Skills CLI listed {sorted(listed_names)!r}; expected {expected_names!r}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Captured Skills CLI list output")
    arguments = parser.parse_args()

    try:
        output = arguments.output.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Cannot read Skills CLI output: {error}", file=sys.stderr)
        return 1

    errors = validate_list_output(REPOSITORY_ROOT, output)
    if errors:
        print("Skills CLI list validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skills CLI listed the exact catalog skill set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
