# MCP-A 2.0 Review Remediation

Status: Working checklist for `2.0.0-beta`

This revision addresses the protocol-design review performed against
`1.1.0-beta`. It is intentionally a breaking revision: identity, capability
negotiation, result states, action safety, and extension behavior cannot be
made coherent through additive fields alone.

## Design decisions

1. MCP-A is a versioned MCP tool profile, not a transport-independent protocol.
   The normative binding targets MCP revision `2025-11-25`; later MCP revisions
   may be supported when their behavior is compatible.
2. Profile capabilities are negotiated during MCP `initialize`. `discover`
   lists domains; it is not the capability-negotiation bootstrap.
3. The authenticated principal comes exclusively from the MCP authorization
   context. Client-supplied `user_id` fields are removed.
4. MCP-A tool names are namespaced as `mcpa.*`.
5. MCP Tasks are the normative asynchronous mechanism. `follow_up` refines an
   immutable answer and does not double as a job protocol.
6. MCP Elicitation is preferred for in-call input and approval. Portable
   `input_required` and `approval_required` result states remain available for
   clients that do not negotiate elicitation.
7. Domain semantics, structured query plans, and concrete output JSON Schemas
   are separate contracts. A structured payload always carries the exact
   output schema identifier and schema used to validate it.
8. Answer objects are immutable and revisioned. A refinement creates a new
   `answer_id` with `parent_answer_id`.
9. Actions distinguish `operation_id` (definition) from `execution_id`
   (invocation), version operation definitions and input schemas, support typed initial inputs, require idempotency keys for
   effects, and represent approval, preview, partial completion, compensation,
   and preconditions explicitly.
10. Multi-source results report scope, completeness, source status, freshness,
    conflicts, and claim-linked citations.
11. Extensions live under namespaced `extensions` objects. Closed normative
    shapes and forward-compatible extensions no longer contradict one another.
12. Conformance is versioned and feature-based. `Core`, `Full`, and `Extended`
    are retained as convenience bundles, not substitutes for feature flags.

## Review issue coverage

| Review issue | Resolution |
|---|---|
| Overstated performance claims | Claims changed to testable hypotheses; `BENCHMARKING.md` defines comparison workloads and reporting rules. |
| Missing MCP wire binding | `MCP-BINDING.md` defines MCP revision, initialization capability, tool names, envelopes, errors, Tasks, Elicitation, and annotations. |
| Capability bootstrap contradiction | Capabilities move to MCP initialization; `discover` becomes a Core domain-catalog tool. |
| Spoofable `user_id` | Removed from request schemas; principal binding is normative. |
| Ontology is not an output schema | Added structured query plan and exact `output_schema`/`output_schema_id` response contract. |
| Unsafe action model | Added typed operations, initial inputs, preview/approval states, idempotency, preconditions, per-effect status, partial completion, and compensation metadata. |
| Duplicate async protocol | Polling via `follow_up` removed; MCP Tasks adopted. |
| Weak provenance/partial failure | Added claim IDs, enriched citations, source status, conflicts, completeness, and `as_of`. |
| Version/extension contradiction | Added exact-version negotiation, version-scoped conformance, feature flags, and namespaced extensions. |
| Schema/state invariants not enforced | Schemas use explicit `oneOf`, `dependentRequired`, and conditional exclusions; negative tests cover invalid combinations. |
| Missing threat model | `THREAT-MODEL.md` covers auth, delegation, prompt injection, handles, SSRF, privacy, rate limits, and audit controls. |
| No behavioral conformance | Added negative artifact tests and a live runtime matrix covering authorization, Tasks, retries, partial failure, and abuse cases. |
| Documentation/governance drift | Version/count/status references and examples are synchronized for the 2.0 candidate. |

## Deliberately deferred implementation work

The repository specifies and validates the protocol artifacts. A production
reference server, SDK-generated clients, cross-language interoperability lab,
and benchmark result corpus require separate executable projects. This
repository defines the acceptance criteria those projects must meet; it does
not claim that prose and JSON Schema alone prove runtime conformance.
