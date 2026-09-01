"""Guard the current-version boundary from accidental 1.1 drift."""
from __future__ import annotations

import json
from pathlib import Path

from mcpa_validation.mapping import MANIFEST
from mcpa_validation.registry import load_json


def test_current_schema_ids_are_versioned(schemas_dir: Path) -> None:
    expected_prefix = "https://mcp-a.dev/schemas/2.0/"
    for path in schemas_dir.glob("*.json"):
        schema = load_json(path)
        assert schema["$id"] == expected_prefix + path.name


def test_current_manifest_excludes_historical_vectors() -> None:
    assert all("/v1.1/" not in example for example, _schema in MANIFEST)


def test_current_request_schemas_do_not_define_caller_identity(schemas_dir: Path) -> None:
    for path in schemas_dir.glob("*.request.json"):
        serialized = json.dumps(load_json(path), sort_keys=True)
        assert "user_id" not in serialized


def test_normative_documents_name_all_canonical_tools(repo_root: Path) -> None:
    text = (repo_root / "SPEC.md").read_text() + (repo_root / "MCP-BINDING.md").read_text()
    tools = {
        "mcpa.discover",
        "mcpa.schema",
        "mcpa.query",
        "mcpa.follow_up",
        "mcpa.context",
        "mcpa.explain",
        "mcpa.action",
    }
    assert all(tool in text for tool in tools)
