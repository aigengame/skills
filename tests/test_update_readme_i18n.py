"""Tests for the README translation marker update script."""

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import update_readme_i18n


class UpdateReadmeI18nTests(unittest.TestCase):
    def test_marker_hash_is_stable_across_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            translation = root / "README.zh-CN.md"
            readme.write_bytes(b"# Title\r\n\r\nBody\r\n")
            translation.write_text(
                "<!-- skills-readme-i18n: source=README.md "
                f"sha256={'0' * 64} -->\n\n# Title\n",
                encoding="utf-8",
            )

            with (
                patch.object(update_readme_i18n, "README", readme),
                patch.object(update_readme_i18n, "TRANSLATIONS", [translation]),
                patch.object(update_readme_i18n, "REPOSITORY_ROOT", root),
            ):
                update_readme_i18n.main()

            expected = hashlib.sha256(b"# Title\n\nBody\n").hexdigest()
            self.assertIn(
                f"sha256={expected}",
                translation.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
