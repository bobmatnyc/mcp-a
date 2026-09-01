---
MAEP: 0006
Title: Normative MCP binding and protocol hardening
Author: MCP-A maintainers
Status: Accepted
Created: 2026-09-01
Spec-Version-Target: 2.0.0-beta
---

> Accepted into the 2.0 beta normative artifacts and static validation suite on
> 2026-09-01. Runtime implementations and interoperability evidence remain open
> release-gate work; this proposal is not yet Final.

## Summary

Define MCP-A as a versioned MCP tool profile with a normative MCP
`2025-11-25` binding. Replace caller-asserted identity, ad hoc asynchronous
polling, unverifiable domain-shaped output, and optimistic action semantics
with negotiated capabilities, authorization-context identity, MCP Tasks,
concrete output schemas, immutable answers, and retry-safe action executions.

## Motivation

The `1.1.0-beta` artifacts describe a coherent compiled-answer architecture,
but leave enough wire, state, authorization, and failure behavior unspecified
that two schema-valid implementations can be incompatible. Some of those gaps
are security-sensitive: a required request `user_id` can be misused as an
identity assertion; a natural-language action has no idempotency or partial
effect model; and an arbitrary API-surface URL can induce unsafe client fetches.

## Specification

The complete candidate contract is incorporated into `SPEC.md`,
`MCP-BINDING.md`, `THREAT-MODEL.md`, `BENCHMARKING.md`, and the JSON Schemas.
The principal changes are enumerated in `REVIEW-REMEDIATION.md`.

## MCP Interaction

`MCP-BINDING.md` defines exact-version initialization negotiation, canonical
tool names, self-contained tool schemas, `structuredContent`, protocol versus
tool errors, tool annotations, Tasks, Elicitation, and resource handling. The
profile baseline is MCP `2025-11-25`.

## Security and Privacy

`THREAT-MODEL.md` makes authorization-context binding, downstream token
isolation, prompt/data separation, SSRF controls, resource limits, approval
binding, retention, safe explanation, and audit integrity normative. The
request schemas reject caller-asserted identity and state handles are not bearer
capabilities.

## Failure and Recovery

Queries distinguish complete, partial, and input-required states and preserve
per-source status. MCP Tasks own durable async status and cancellation. Actions
separate no-effect failure from partial completion, retain every applied or
failed effect, and bind safe retries to idempotency keys and preconditions.

## Backwards Compatibility

This proposal is intentionally breaking and therefore targets `2.0.0-beta`.
Servers may expose both v1 and v2 tool sets during migration, but the namespaced
v2 tools and negotiated profile capability must be used for v2 behavior. A
server must never return a v1 response under a negotiated v2 tool definition.

## Conformance and Test Vectors

The static suite validates schemas, current payload examples, binding examples,
caller-identity rejection, mixed-state rejection, exact structured output,
immutable follow-up parentage, and partial-effect invariants. `CONFORMANCE.md`
defines the live authorization, Task, retry, cancellation, and abuse tests still
required of implementations.

## Implementation Evidence

The repository includes machine-readable schemas, positive examples, negative
vectors, MCP envelope vectors, and a conformance harness. Production SDK and
server implementations remain follow-on work and must not be implied by the
static validator.

## Open Questions

1. Whether the next stable MCP revision should replace the `2025-11-25`
   baseline before MCP-A 2.0 reaches stable.
2. Whether a future structured-query algebra should be standardized outside
   MCP-A and referenced here.
3. Which independent implementations will participate in the first
   interoperability event.
