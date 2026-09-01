"""Explicit current-version example-to-schema manifest.

Version 1.1 examples are retained under examples/v1.1 as historical vectors and
are intentionally excluded from the 2.0 conformance suite.
"""
from __future__ import annotations

MANIFEST: list[tuple[str, str]] = [
    ("examples/00-profile-capability.json", "profile.capability.json"),
    ("examples/01-discover.request.json", "discover.request.json"),
    ("examples/01-discover.response.json", "discover.response.json"),
    ("examples/02-schema-domain.request.json", "schema.request.json"),
    ("examples/02-schema-domain.response.json", "schema.response.json"),
    ("examples/03-schema-query.request.json", "schema.request.json"),
    ("examples/03-schema-query.response.json", "schema.response.json"),
    ("examples/04-schema-action.request.json", "schema.request.json"),
    ("examples/04-schema-action.response.json", "schema.response.json"),
    ("examples/05-query-structured.request.json", "query.request.json"),
    ("examples/05-query-structured.response.json", "query.response.json"),
    ("examples/06-query-input-required.request.json", "query.request.json"),
    ("examples/06-query-input-required.response.json", "query.response.json"),
    ("examples/06b-query-continuation.request.json", "query.request.json"),
    ("examples/07-query-partial.request.json", "query.request.json"),
    ("examples/07-query-partial.response.json", "query.response.json"),
    ("examples/08-follow-up.request.json", "follow_up.request.json"),
    ("examples/08-follow-up.response.json", "follow_up.response.json"),
    ("examples/09-action-resolve.request.json", "action.request.json"),
    ("examples/09-action-resolve.response.json", "action.response.json"),
    ("examples/10-action-approve.request.json", "action.request.json"),
    ("examples/10-action-completed.response.json", "action.response.json"),
    ("examples/11-action-partial.request.json", "action.request.json"),
    ("examples/11-action-partial.response.json", "action.response.json"),
    ("examples/12-context-read.request.json", "context.request.json"),
    ("examples/12-context-read.response.json", "context.response.json"),
    ("examples/13-explain-answer.request.json", "explain.request.json"),
    ("examples/13-explain-answer.response.json", "explain.response.json"),
    ("examples/14-tool-error.json", "error.json"),
]
