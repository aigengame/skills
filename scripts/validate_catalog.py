#!/usr/bin/env python3
"""Validate the repository's Agent Skills catalog under ``skills/``."""

from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml
from yaml.constructor import ConstructorError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_FRONTMATTER_FIELDS = frozenset(
    {
        "allowed-tools",
        "compatibility",
        "description",
        "license",
        "metadata",
        "name",
    }
)
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
YAML_BOOLEAN_TAG = "tag:yaml.org,2002:bool"
YAML_12_BOOLEAN_PATTERN = re.compile(r"^(?:true|false)$", re.IGNORECASE)
MARKDOWN = MarkdownIt("commonmark")


class FrontmatterLoader(yaml.SafeLoader):
    """Parse YAML 1.2 boolean values and reject duplicate mapping keys."""


FrontmatterLoader.yaml_implicit_resolvers = {
    first_character: [
        resolver for resolver in resolvers if resolver[0] != YAML_BOOLEAN_TAG
    ]
    for first_character, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
FrontmatterLoader.add_implicit_resolver(
    YAML_BOOLEAN_TAG,
    YAML_12_BOOLEAN_PATTERN,
    list("tTfF"),
)


def _construct_unique_mapping(
    loader: FrontmatterLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, Hashable):
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            )
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


FrontmatterLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _skill_directories(catalog_root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in catalog_root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        ),
        key=lambda path: path.name,
    )


def _parse_frontmatter(
    skill_file: Path, text: str, root: Path
) -> tuple[dict[str, Any] | None, list[str]]:
    display_path = _relative_path(skill_file, root)
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, [
            f"{display_path}: frontmatter must start with an exact '---' line"
        ]

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return None, [
            f"{display_path}: frontmatter must end with an exact '---' line"
        ]

    source = "\n".join(lines[1:closing_index])
    try:
        data = yaml.load(source, Loader=FrontmatterLoader)
    except yaml.YAMLError:
        return None, [f"{display_path}: frontmatter is not valid YAML"]

    if not isinstance(data, dict):
        return None, [f"{display_path}: frontmatter must be a YAML mapping"]

    errors: list[str] = []
    non_string_fields = sorted(repr(key) for key in data if not isinstance(key, str))
    for field in non_string_fields:
        errors.append(f"{display_path}: frontmatter field {field} must be a string")

    fields = {key: value for key, value in data.items() if isinstance(key, str)}
    for field in sorted(fields.keys() - SUPPORTED_FRONTMATTER_FIELDS):
        errors.append(f"{display_path}: unsupported frontmatter field '{field}'")

    for required_field in ("name", "description"):
        if required_field not in fields:
            errors.append(
                f"{display_path}: required frontmatter field '{required_field}' is missing"
            )

    return fields, errors


def _validate_frontmatter(
    skill_directory: Path,
    skill_file: Path,
    frontmatter: dict[str, Any],
    root: Path,
) -> list[str]:
    display_path = _relative_path(skill_file, root)
    errors: list[str] = []

    name = frontmatter.get("name")
    if "name" in frontmatter:
        if not isinstance(name, str):
            errors.append(f"{display_path}: frontmatter name must be a string")
        elif not NAME_PATTERN.fullmatch(name) or len(name) > 64:
            errors.append(
                f"{display_path}: frontmatter name must be 1-64 lowercase letters, "
                "numbers, or single hyphens"
            )
        elif name != skill_directory.name:
            errors.append(
                f"{display_path}: frontmatter name '{name}' does not match directory "
                f"'{skill_directory.name}'"
            )

    description = frontmatter.get("description")
    if "description" in frontmatter:
        if not isinstance(description, str) or not description.strip():
            errors.append(
                f"{display_path}: frontmatter description must be a non-empty string"
            )
        elif len(description) > 1024:
            errors.append(
                f"{display_path}: frontmatter description must not exceed 1024 characters"
            )

    for field, maximum_length in (("compatibility", 500),):
        value = frontmatter.get(field)
        if value is not None and (
            not isinstance(value, str)
            or not value.strip()
            or len(value) > maximum_length
        ):
            errors.append(
                f"{display_path}: frontmatter {field} must be a non-empty string "
                f"of at most {maximum_length} characters"
            )

    for field in ("license", "allowed-tools"):
        value = frontmatter.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(
                f"{display_path}: frontmatter {field} must be a non-empty string"
            )

    metadata = frontmatter.get("metadata")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        )
    ):
        errors.append(
            f"{display_path}: frontmatter metadata must map strings to strings"
        )

    return errors


def _markdown_destinations(text: str) -> list[str]:
    destinations: list[str] = []
    for token in MARKDOWN.parse(text):
        for child in token.children or ():
            attribute = {"image": "src", "link_open": "href"}.get(child.type)
            if attribute is not None:
                destination = child.attrGet(attribute)
                if destination is not None:
                    destinations.append(destination)
    return destinations


def _validate_relative_references(
    skill_file: Path, text: str, root: Path
) -> list[str]:
    display_path = _relative_path(skill_file, root)
    resolved_root = root.resolve()
    errors: list[str] = []
    checked_targets: set[str] = set()

    for target in _markdown_destinations(text):
        parsed = urlsplit(target)
        if (
            not target
            or target.startswith("#")
            or target.startswith("/")
            or parsed.scheme
            or parsed.netloc
            or not parsed.path
        ):
            continue

        relative_target = unquote(parsed.path)
        if relative_target in checked_targets:
            continue
        checked_targets.add(relative_target)

        resolved_target = (skill_file.parent / relative_target).resolve()
        try:
            resolved_target.relative_to(resolved_root)
        except ValueError:
            errors.append(
                f"{display_path}: relative reference '{relative_target}' "
                "resolves outside the repository"
            )
            continue

        if not resolved_target.is_file():
            errors.append(
                f"{display_path}: relative reference '{relative_target}' "
                "does not name a repository file"
            )

    return errors


def _validate_skill(skill_directory: Path, root: Path) -> list[str]:
    skill_file = skill_directory / "SKILL.md"
    display_path = _relative_path(skill_file, root)
    if not skill_file.is_file():
        return [f"{display_path}: file is missing"]

    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [f"{display_path}: file is not readable UTF-8 ({error})"]

    frontmatter, errors = _parse_frontmatter(skill_file, text, root)
    if frontmatter is not None:
        errors.extend(
            _validate_frontmatter(skill_directory, skill_file, frontmatter, root)
        )
    errors.extend(_validate_relative_references(skill_file, text, root))
    return errors


def validate_catalog(root: Path) -> tuple[int, list[str]]:
    """Return the number of skill directories and all validation errors."""
    catalog_root = root / "skills"
    if not catalog_root.is_dir():
        return 0, ["skills: catalog directory is missing"]

    skill_directories = _skill_directories(catalog_root)
    if not skill_directories:
        return 0, ["skills: catalog must contain at least one skill"]

    errors: list[str] = []
    for skill_directory in skill_directories:
        errors.extend(_validate_skill(skill_directory, root))
    return len(skill_directories), errors


def main() -> int:
    _, errors = validate_catalog(REPOSITORY_ROOT)
    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Catalog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
