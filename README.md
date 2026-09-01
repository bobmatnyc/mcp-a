---
Status: DRAFT
Version: 2.0.0-beta
Date: 2026-09-01
MCP-Baseline: 2025-11-25
---

# MCP-A — the MCP Answers Profile

MCP-A is an experimental, versioned profile for MCP servers that compile
answers and actions across one or more domains. It defines seven namespaced MCP
tools, a typed semantic/query layer, claim-linked provenance, explicit partial
failure, immutable answer handles, and retry-safe action lifecycles.

The design hypothesis is deliberately narrower than the original claim: for
multi-source or semantically rich workloads, moving classification,
deterministic computation, and consolidation server-side may reduce client
orchestration. Conformance alone does not prove that it is faster, cheaper, or
more accurate. Those claims require the measurements in
[`BENCHMARKING.md`](./BENCHMARKING.md).

## Why a profile

MCP defines transport, lifecycle, authorization integration, tools, resources,
Tasks, and Elicitation. It does not prescribe how a compiled-answer service
represents domain semantics, query plans, provenance, partial coverage, or
multi-effect actions. MCP-A supplies that application-level contract without
redefining MCP.

The profile is useful when a server owns meaningful cross-source semantics. A
small server with a few direct, well-designed tools may not need it.

## The seven tools

| Tool | Responsibility |
|---|---|
| `mcpa.discover` | List authorization-filtered information domains. |
| `mcpa.schema` | Describe ontology, query capabilities, and operations. |
| `mcpa.query` | Execute a natural-language or typed query plan. |
| `mcpa.follow_up` | Create an immutable refinement of an answer. |
| `mcpa.context` | Manage bounded user-approved preferences and memory. |
| `mcpa.explain` | Return a safe, authorization-filtered execution explanation. |
| `mcpa.action` | Resolve and execute typed, approved, retry-safe operations. |

These are ordinary MCP tools. Support is negotiated in MCP `initialize`, tool
availability comes from `tools/list`, results use `structuredContent`, durable
async work uses MCP Tasks, and interactive input may use MCP Elicitation.

## Design boundaries

- Identity comes from the MCP authorization context, never `user_id` in tool arguments.
- An ontology, a query plan, and an output schema are distinct contracts.
- Structured output includes the exact schema it validates against.
- Claims link citations to specific prose or structured paths.
- Source failures and conflicts are explicit; incomplete results cannot claim completeness.
- Answer content is immutable; refinements receive new IDs.
- Actions separate operation definitions from executions and record every effect.
- Extensions live only under reverse-DNS namespaces.

## Start here

1. Read [`SPEC.md`](./SPEC.md) and the normative
   [`MCP-BINDING.md`](./MCP-BINDING.md).
2. Review [`THREAT-MODEL.md`](./THREAT-MODEL.md) before implementing handles,
   memory, source retrieval, or actions.
3. Walk through [`examples/`](./examples/) and the
   [`QUICKSTART.md`](./QUICKSTART.md).
4. Run the validation suite described in [`VALIDATION.md`](./VALIDATION.md).
5. Use [`CONFORMANCE.md`](./CONFORMANCE.md) for a version-scoped runtime claim.

## Repository map

| Path | Purpose |
|---|---|
| [`SPEC.md`](./SPEC.md) | Normative application semantics. |
| [`MCP-BINDING.md`](./MCP-BINDING.md) | Normative MCP wire binding. |
| [`schemas/`](./schemas/) | Draft 2020-12 request, response, error, and capability schemas. |
| [`examples/`](./examples/) | Current 2.0 vectors plus archived 1.1 vectors. |
| [`THREAT-MODEL.md`](./THREAT-MODEL.md) | Threats, trust boundaries, and required mitigations. |
| [`BENCHMARKING.md`](./BENCHMARKING.md) | Reproducible performance and quality claim rules. |
| [`CONFORMANCE.md`](./CONFORMANCE.md) | Feature bundles and executable/runtime requirements. |
| [`guides/`](./guides/) | Non-normative implementation guidance and migration notes. |
| [`MAEP/`](./MAEP/) | Enhancement proposals and governance history. |
| [`REVIEW-REMEDIATION.md`](./REVIEW-REMEDIATION.md) | Traceability from design critique to changes. |

## Maturity

`2.0.0-beta` is a breaking design draft, not a production standard. Stable
release requires independent implementations, cross-language interop,
benchmarks, adversarial review, and hosted schema bundles. See SPEC §24.

Specification text and examples are licensed under
[CC BY 4.0](./LICENSE). Implementation code in this repository is limited to
validation utilities; adopters should make their own implementation licensing
clear.
