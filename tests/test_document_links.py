"""Keep relative Markdown links resolvable after versioned artifact moves."""
from __future__ import annotations

import re
from pathlib import Path

import pytest


def test_relative_markdown_links_resolve(repo_root: Path) -> None:
    missing: list[str] = []
    for document in repo_root.rglob("*.md"):
        if any(part in {".git", ".venv"} for part in document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = raw_target.strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            path_part = target.split("#", 1)[0]
            if path_part and not (document.parent / path_part).resolve().exists():
                relative_document = document.relative_to(repo_root)
                missing.append(f"{relative_document}: {target}")

    if missing:
        pytest.fail("Broken relative Markdown links:\n  " + "\n  ".join(sorted(missing)))
