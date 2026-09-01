"""Behavioral schema invariants that positive examples alone cannot prove."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mcpa_validation.registry import load_json


def _is_valid(instance: dict, schema_name: str, schemas_dir: Path, validator_for) -> bool:
    schema = load_json(schemas_dir / schema_name)
    return validator_for(schema).is_valid(instance)


@pytest.mark.parametrize(
    ("instance", "schema_name"),
    [
        ({"question": "Revenue?", "user_id": "caller-asserted"}, "query.request.json"),
        ({"answer_id": "ans", "refinement": "AMER", "user_id": "u"}, "follow_up.request.json"),
        ({"mode": "read", "key": "currency"}, "context.request.json"),
        (
            {
                "mode": "append",
                "namespace": "preferences",
                "key": "x",
                "value": 1,
                "ttl_seconds": 60,
            },
            "context.request.json",
        ),
    ],
)
def test_unsafe_or_ambiguous_requests_are_rejected(
    instance: dict, schema_name: str, schemas_dir: Path, validator_for
) -> None:
    assert not _is_valid(instance, schema_name, schemas_dir, validator_for)


def test_context_set_may_have_retention(schemas_dir: Path, validator_for) -> None:
    instance = {
        "mode": "set",
        "namespace": "preferences",
        "key": "currency",
        "value": "USD",
        "ttl_seconds": 3600,
    }
    assert _is_valid(instance, "context.request.json", schemas_dir, validator_for)


def test_structured_payload_conforms_to_embedded_output_schema(
    repo_root: Path, validator_for
) -> None:
    response = load_json(repo_root / "examples/05-query-structured.response.json")
    output_validator = Draft202012Validator(response["output_schema"])
    assert output_validator.is_valid(response["structured"])


def test_partial_action_requires_applied_and_failed_effects(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    response = load_json(repo_root / "examples/11-action-partial.response.json")
    assert _is_valid(response, "action.response.json", schemas_dir, validator_for)

    no_failure = deepcopy(response)
    no_failure["effects"][1]["status"] = "applied"
    no_failure["effects"][1].pop("error")
    assert not _is_valid(no_failure, "action.response.json", schemas_dir, validator_for)


def test_failed_action_cannot_hide_effects(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    response = load_json(repo_root / "examples/11-action-partial.response.json")
    response["status"] = "failed"
    assert not _is_valid(response, "action.response.json", schemas_dir, validator_for)


def test_follow_up_answer_requires_parent(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    response = load_json(repo_root / "examples/08-follow-up.response.json")
    assert _is_valid(response, "follow_up.response.json", schemas_dir, validator_for)
    response.pop("parent_answer_id")
    assert not _is_valid(response, "follow_up.response.json", schemas_dir, validator_for)


def test_schema_target_cannot_mix_contract_layers(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    response = load_json(repo_root / "examples/02-schema-domain.response.json")
    response["operations"] = []
    assert not _is_valid(response, "schema.response.json", schemas_dir, validator_for)


def test_mcp_error_vector_uses_tool_error_result(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    envelope = load_json(repo_root / "examples/mcp/tool-error.result.json")
    result = envelope["result"]
    assert envelope["jsonrpc"] == "2.0"
    assert result["isError"] is True
    assert _is_valid(result["structuredContent"], "error.json", schemas_dir, validator_for)


def test_mcp_initialize_vector_matches_profile_capability(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    envelope = load_json(repo_root / "examples/mcp/initialize.result.json")
    capability = envelope["result"]["capabilities"]["experimental"][
        "io.modelcontextprotocol/mcpa"
    ]
    assert envelope["result"]["protocolVersion"] == "2025-11-25"
    assert _is_valid(capability, "profile.capability.json", schemas_dir, validator_for)
    assert capability["selectedVersion"] in capability["versions"]


def test_mcp_initialize_request_matches_client_capability(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    envelope = load_json(repo_root / "examples/mcp/initialize.request.json")
    capability = envelope["params"]["capabilities"]["experimental"][
        "io.modelcontextprotocol/mcpa"
    ]
    assert envelope["params"]["protocolVersion"] == "2025-11-25"
    assert _is_valid(capability, "profile.client-capability.json", schemas_dir, validator_for)


def test_normative_binding_json_examples_are_valid(
    repo_root: Path, schemas_dir: Path, validator_for
) -> None:
    binding = (repo_root / "MCP-BINDING.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", binding, re.DOTALL)
    parsed = [json.loads(block) for block in blocks]
    assert len(parsed) >= 2

    result = parsed[1]["result"]
    assert result["isError"] is False
    assert _is_valid(result["structuredContent"], "query.response.json", schemas_dir, validator_for)
