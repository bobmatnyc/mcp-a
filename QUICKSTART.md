# Implementation quickstart

This guide describes the smallest credible MCP-A 2.0 Core server. It assumes an
existing MCP server with authorization and ordinary tool support.

## 1. Choose and declare a version

Target one exact draft version first. Add
`capabilities.experimental["io.modelcontextprotocol/mcpa"]` to the MCP
`initialize` result and validate it against `schemas/profile.capability.json`.
Use `examples/mcp/initialize.result.json` as the envelope vector.

Do not advertise a feature until its runtime behavior and negative tests pass.

## 2. Register namespaced tools

Core requires `mcpa.discover` and `mcpa.query`. Publish self-contained
`inputSchema` and `outputSchema` values in `tools/list`; bundle referenced
definitions so clients do not need network access during validation.

Return profile payloads in MCP `structuredContent`. Keep a concise text content
block for clients that do not render structured output.

## 3. Bind authorization

Build a verified authorization context from MCP authentication. Never accept a
caller-supplied user or tenant ID. Apply domain, source, record, field, and
operation authorization after planning and immediately before data access or
mutation.

Store answer and execution handles with principal, client, tenant, expiry, and
policy-relevant context. Unknown and unauthorized handles should be
indistinguishable to ordinary callers.

## 4. Implement discovery

Return a bounded, deterministic, authorization-filtered domain catalog. Include
schema versions and safe scope summaries. Add opaque cursor pagination before
catalog size makes a single response unsafe.

## 5. Implement query execution

Normalize natural language into the same typed plan accepted from callers.
Validate the plan against the domain's allowed fields, filters, groupings,
aggregations, cost limits, and authorization. Execute numeric operations in
ordinary program logic or the backing data system, never by model estimation.

Create an immutable result with claims, linked citations, source statuses,
conflicts, computed scope, freshness, and the executed plan. If an intended
source fails, return `partial`; do not hide the omitted coverage.

For structured output, select or derive one exact JSON Schema, validate the
payload, and return both `output_schema_id` and `output_schema`.

## 6. Use MCP lifecycle features

Use MCP Tasks for durable query or action work and MCP Elicitation when the
client supports it. Do not invent an answer-handle polling method. Honor MCP
cancellation and cap concurrency, task TTL, retained bytes, and polling rate.

## 7. Add Full features deliberately

Add `mcpa.schema`, `mcpa.follow_up`, `mcpa.context`, `mcpa.explain`, and
`mcpa.action` one feature at a time. Before enabling actions, implement typed
operation discovery, idempotency, preconditions, visible approval, per-effect
authorization, partial completion, compensation reporting, and audit retention.

## 8. Validate and claim

Run:

```text
make check
```

Then run the authorization-isolation, retry, Task, cancellation, source-failure,
and MCP envelope tests in `CONFORMANCE.md` against the live server. Schema-valid
examples alone are not a runtime conformance claim.
