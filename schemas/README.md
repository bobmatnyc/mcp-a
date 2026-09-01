# MCP-A 2.0 JSON Schemas

The top-level files are the normative draft 2020-12 contracts for MCP-A
`2.0.0-beta`. Their logical IDs use:

```text
https://mcp-a.dev/schemas/2.0/<filename>
```

The URI is an identifier, not an instruction to fetch over the network. Build
an offline registry or publish a bundled schema resource with all references.

## Files

| File group | Purpose |
|---|---|
| `profile.client-capability.json` | Client-supported versions and optional features. |
| `profile.capability.json` | Server-selected version, bundle, and features. |
| `common.defs.json` | Shared query, provenance, input, operation, and effect definitions. |
| `error.json` | Abstract tool execution error. |
| `<tool>.request.json` | `tools/call.params.arguments` contract. |
| `<tool>.response.json` | Successful `structuredContent` contract. |

`follow_up.response.json` references `query.response.json` because a refinement
creates an ordinary immutable answer. The ontology, query-plan schema, and
output schema are separate objects by design.

## Strictness and extensions

Normative objects use `additionalProperties: false`. Extensions belong under
the `extensions` property and use reverse-DNS keys. This avoids the former
contradiction between closed schemas and instructions to ignore arbitrary
unknown top-level fields.

## Validation

Run `make check` from the repository root. The validation registry loads every
top-level schema by `$id`, checks schema well-formedness, validates the current
example manifest, and runs negative invariant tests. See
[`../VALIDATION.md`](../VALIDATION.md).
