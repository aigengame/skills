#!/usr/bin/env python3
"""Stamp translated READMEs with the current English README hash.

``README.md`` is the authoritative source. Each translated README records the
SHA-256 of the English version that a maintainer last reviewed:

    <!-- skills-readme-i18n: source=README.md sha256=<64-hex> -->

After updating a translation, run:

    python scripts/update_readme_i18n.py

The marker proves that a maintainer acknowledged the current source version. It
does not prove that a translation is accurate or natural; that requires review.
The marker format is also defined in ``tests/test_readme_i18n_sync.py``.
"""

import hashlib
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README = REPOSITORY_ROOT / "README.md"
TRANSLATIONS = [REPOSITORY_ROOT / "docs" / "README.zh-CN.md"]
MARKER_RE = re.compile(r"<!--\s*skills-readme-i18n:.*?-->", re.DOTALL)


def main() -> None:
    digest = hashlib.sha256(README.read_bytes()).hexdigest()
    marker = f"<!-- skills-readme-i18n: source=README.md sha256={digest} -->"

    for path in TRANSLATIONS:
        if not path.exists():
            print(f"skipped (missing): {path.relative_to(REPOSITORY_ROOT)}")
            continue

        body = MARKER_RE.sub("", path.read_text(encoding="utf-8")).lstrip("\n")
        path.write_text(f"{marker}\n\n{body}", encoding="utf-8")
        print(f"stamped {path.relative_to(REPOSITORY_ROOT)} -> {digest[:12]}…")


if __name__ == "__main__":
    main()
