"""README translation discovery and freshness checks.

``README.md`` is authoritative. The Chinese README starts with a marker that
records the SHA-256 of the English version a maintainer last reviewed. A source
change therefore fails this test until the translation is reviewed and stamped
with ``python scripts/update_readme_i18n.py``.

The marker is a freshness acknowledgement, not proof of translation quality.
Its format is also defined in ``scripts/update_readme_i18n.py``.
"""

import hashlib
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README = REPOSITORY_ROOT / "README.md"
ZH_CN_README = REPOSITORY_ROOT / "docs" / "README.zh-CN.md"
MARKER_RE = re.compile(
    r"<!--\s*skills-readme-i18n:\s*source=README\.md\s+"
    r"sha256=([0-9a-f]{64})\s*-->"
)


def english_readme_hash() -> str:
    return hashlib.sha256(README.read_bytes()).hexdigest()


def recorded_source_hash(text: str) -> str | None:
    match = MARKER_RE.match(text)
    return match.group(1) if match else None


class ReadmeI18nSyncTests(unittest.TestCase):
    def test_chinese_translation_is_present(self) -> None:
        self.assertTrue(
            ZH_CN_README.is_file(),
            "docs/README.zh-CN.md is missing",
        )

    def test_english_readme_links_to_chinese_translation(self) -> None:
        text = README.read_text(encoding="utf-8")

        self.assertIn(
            "docs/README.zh-CN.md",
            text,
            "README.md must link to docs/README.zh-CN.md so readers can find it",
        )

    def test_sync_marker_is_the_leading_content(self) -> None:
        text = ZH_CN_README.read_text(encoding="utf-8")

        self.assertIsNotNone(
            MARKER_RE.match(text),
            "the skills-readme-i18n marker must be the leading content in "
            "docs/README.zh-CN.md; run `python scripts/update_readme_i18n.py`",
        )

    def test_chinese_translation_matches_english_readme(self) -> None:
        expected = english_readme_hash()
        recorded = recorded_source_hash(ZH_CN_README.read_text(encoding="utf-8"))

        self.assertEqual(
            expected,
            recorded,
            "docs/README.zh-CN.md is stale; update the translation, then run "
            "`python scripts/update_readme_i18n.py`",
        )


if __name__ == "__main__":
    unittest.main()
