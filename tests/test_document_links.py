"""Keep relative Markdown links resolvable after versioned artifact moves."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# Directory names skipped by the scan, matched as whole path components so a
# file such as `docs/.claude-notes.md` is still checked. `.claude` holds agent
# harness assets whose skill docs carry template and example links (e.g.
# `docs/specs/foo.md`) that are deliberately unresolvable; they are tooling, not
# project documentation, so they are out of scope for this check.
SKIPPED_DIRECTORIES = {".claude", ".git", ".venv", "node_modules"}


def test_relative_markdown_links_resolve(repo_root: Path) -> None:
    missing: list[str] = []
    for document in repo_root.rglob("*.md"):
        if any(part in SKIPPED_DIRECTORIES for part in document.parts):
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
