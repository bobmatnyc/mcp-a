---
Status: DRAFT NORMATIVE
Version: 2.0.0-beta
MCP-Baseline: 2025-11-25
---

# Normative MCP Binding

## 1. Baseline and precedence

MCP-A 2.0 is bound to Model Context Protocol revision `2025-11-25`. The MCP
lifecycle, authorization, capability, tool, Task, Elicitation, progress,
cancellation, logging, resource, and error rules apply unchanged.

When this profile and MCP overlap, MCP governs the envelope and transport;
MCP-A governs the `mcpa.*` tool arguments and `structuredContent` semantics.

## 2. Initialization capability

A server supporting MCP-A MUST include the following namespaced capability in
its MCP `initialize` result's `capabilities.experimental` object:

```json
{
  "capabilities": {
    "tools": { "listChanged": true },
    "experimental": {
      "io.modelcontextprotocol/mcpa": {
        "versions": ["2.0.0-beta"],
        "selectedVersion": "2.0.0-beta",
        "mcpBaseline": "2025-11-25",
        "conformance": "Full",
        "features": [
          "discovery",
          "query.prose",
          "query.structured",
          "provenance.claims",
          "failure.partial",
          "schema.ontology",
          "schema.query-plan",
          "answer.follow-up",
          "context.preferences",
          "explain",
          "action.safe"
        ],
        "schemaBaseUri": "https://example.com/mcpa/2.0/schemas/"
      }
    }
  }
}
```

The server value MUST validate against `schemas/profile.capability.json`.

The client may advertise a capability of the same name in its
`capabilities.experimental` object containing supported exact profile versions
and optional features. The client value MUST validate against
`schemas/profile.client-capability.json`. The server selects a mutually
supported profile version. Exact-version lists avoid imposing a separate range
grammar on implementers.

The selected version MUST occur in both exact-version lists. A server MAY apply
local policy when several versions intersect; it SHOULD select the highest by
Semantic Version precedence. The server response's `selectedVersion` MUST also
occur in its `versions` list. If the client capability is absent or the lists do
not intersect, the server MUST omit the MCP-A server capability. It MAY still
expose otherwise useful tools as ordinary MCP tools, but that connection does
not have a negotiated MCP-A conformance claim.
If there is no common version, it MUST omit the MCP-A capability and MCP-A tools.

The individual `features` list is authoritative. `conformance` is a convenience
summary. Clients MUST use `tools/list` to determine which tools are callable.
The server MUST NOT select or advertise a standardized feature the client did
not list when the client supplied a `features` list. An absent client feature
list means that version negotiation, not optional-feature support, was declared.

## 3. Tool names and schemas

The canonical names are:

| Tool | Request schema | Response schema |
|---|---|---|
| `mcpa.discover` | `discover.request.json` | `discover.response.json` |
| `mcpa.schema` | `schema.request.json` | `schema.response.json` |
| `mcpa.query` | `query.request.json` | `query.response.json` |
| `mcpa.follow_up` | `follow_up.request.json` | `query.response.json` |
| `mcpa.context` | `context.request.json` | `context.response.json` |
| `mcpa.explain` | `explain.request.json` | `explain.response.json` |
| `mcpa.action` | `action.request.json` | `action.response.json` |

Every `tools/list` definition MUST include a self-contained root object
`inputSchema`. It MUST NOT rely on a client resolving an external root `$ref`.
The `outputSchema` MUST likewise be self-contained or bundled so all references
resolve without unauthenticated network access.

Schema publication URIs are distribution identifiers, not instructions for a
client to fetch arbitrary network content. Servers SHOULD publish content
digests and SHOULD make schema bundles available as MCP resources.

## 4. Tool annotations

Annotations are hints and do not replace policy or approval.

- `mcpa.discover`, `mcpa.schema`, `mcpa.query`, `mcpa.follow_up`, and
  `mcpa.explain` SHOULD declare `readOnlyHint: true`.
- `mcpa.context` MUST declare `readOnlyHint: false` because some modes write;
  it SHOULD declare `destructiveHint: true` because `clear` deletes memory.
- `mcpa.action` MUST declare `readOnlyHint: false`, `destructiveHint: true`,
  `idempotentHint: false`, and `openWorldHint: true`.
- Long-running `mcpa.query` and `mcpa.action` definitions SHOULD declare
  `execution.taskSupport: "optional"` when Tasks are negotiated.

Operation-specific safety metadata is returned by `mcpa.schema`; a generic
`mcpa.action` annotation cannot make a high-risk operation safe.

## 5. Calls and successful results

The MCP `tools/call.params.arguments` value is the MCP-A request object.

A successful MCP-A result MUST be returned in `structuredContent` and conform
to the tool's declared output schema. For compatibility, the server SHOULD also
return a concise serialized or human-readable representation in a text content
block. The text content MUST NOT contradict `structuredContent`.

Example:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [
      { "type": "text", "text": "Revenue was computed from an available but stale source." }
    ],
    "structuredContent": {
      "status": "partial",
      "answer_id": "ans_01J...",
      "revision": 1,
      "answer": "Revenue was computed from an available but stale source.",
      "executed_query_plan": {
        "schema_versions": { "finance": "3.1.0" },
        "domains": ["finance"],
        "select": ["finance.Revenue.current"],
        "consistency": "best_effort"
      },
      "claims": [
        { "claim_id": "claim_revenue", "text": "Revenue came from the available source." }
      ],
      "citations": [
        {
          "citation_id": "cit_revenue",
          "claim_ids": ["claim_revenue"],
          "source_system": "finance-warehouse",
          "retrieved_at": "2026-09-01T12:00:00Z",
          "as_of": "2026-09-01T11:45:00Z"
        }
      ],
      "conflicts": [],
      "completeness": "partial",
      "computed_scope": { "summary": "authorized account scope" },
      "source_statuses": [
        {
          "source_system": "finance-warehouse",
          "status": "stale",
          "required": true,
          "as_of": "2026-09-01T11:45:00Z",
          "retrieved_at": "2026-09-01T12:00:00Z"
        }
      ],
      "routing": {
        "reuse": "new",
        "domains": ["finance"],
        "plan_digest": "sha256:binding-example",
        "safe_rationale": "The question targeted the authorized finance domain."
      },
      "created_at": "2026-09-01T12:00:00Z",
      "as_of": "2026-09-01T11:45:00Z"
    },
    "isError": false
  }
}
```

## 6. Error mapping

MCP-A does not allocate JSON-RPC numeric error codes.

Use MCP protocol errors for:

- malformed JSON-RPC or MCP envelopes;
- unknown tool names;
- arguments that cannot be decoded as the declared root input type;
- internal failures that prevent production of a tool result at all.

Use MCP tool execution errors (`isError: true`) for:

- authentication or authorization failure discovered during execution;
- domain, handle, operation, or record lookup failure;
- query-plan or business validation;
- schema nonconformance;
- upstream failure;
- rate limiting, timeout, conflict, or precondition failure.

The `structuredContent` of a tool execution error SHOULD validate against
`schemas/error.json`; the text content SHOULD contain concise recovery guidance.
Clients SHOULD make actionable tool execution errors available to the model but
MUST redact secrets and authorization-sensitive detail.

An action with applied effects followed by a failure is not a tool error with
no result. It is a successful protocol/tool exchange whose MCP-A state is
`partially_completed` and whose per-effect results are preserved.

## 7. Tasks

When the server advertises MCP `tasks.requests.tools.call` and the tool declares
task support, a client MAY task-augment `mcpa.query` or `mcpa.action`.

The Task ID is the sole polling/cancellation handle. The server MUST implement
MCP Task ownership, TTL, status, result, progress, cancellation, and related
task metadata rules. The eventual task result is the ordinary MCP-A output.

An `answer_id` or `execution_id` MUST NOT be accepted by MCP task methods as a
substitute for `taskId`. `mcpa.follow_up` MUST NOT poll tasks.

## 8. Elicitation and approval

If the client advertises form Elicitation, the server SHOULD use it to obtain
non-sensitive missing inputs. If URL Elicitation is negotiated, it MAY be used
for sensitive out-of-band flows as allowed by MCP.

The portable MCP-A `input_required` state remains valid when Elicitation is not
available or when an interaction must outlive one request. The client returns
values through the appropriate continuation request.

Approval MUST remain a visible client/user decision. Before returning an
approval, the client MUST show the server identity, operation, normalized
inputs, risk, planned effects, reversibility, and relevant authorization scope.
The model alone is not the approving human.

## 9. Resources

Large ontologies, output schemas, and API-surface transparency documents SHOULD
be exposed as MCP resources rather than placed inline. Resource URIs MUST be
authorization-scoped. Returned resource links MUST carry media type, size, and
digest in the surrounding MCP-A metadata.

Clients MUST NOT automatically fetch ordinary HTTP URLs found inside domain
metadata. A network fetch requires normal client security policy and explicit
handling outside this profile.

## 10. Compatibility

Servers may expose v1 and v2 concurrently only through distinct tool names or
distinct negotiated connections. A response MUST match the negotiated version
and declared output schema. Clients MUST ignore unknown namespaced extensions
but MUST reject unknown normative top-level state fields when strict validation
is enabled.
