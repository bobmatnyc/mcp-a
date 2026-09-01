# Changelog

This project follows Semantic Versioning. Dates describe repository artifacts,
not production adoption.

## [Unreleased]

- Cross-language reference implementations, runtime harness, interoperability
  event, benchmarks, and adversarial review remain release-gate work.

### Fixed

- Excluded `.claude/` from the document link check; test-only change.

## [2.0.0-beta] - 2026-09-01

### Changed

- Bound the profile normatively to MCP `2025-11-25` and namespaced all tools as
  `mcpa.*`.
- Moved version and feature negotiation from `discover` to MCP initialization.
- Removed caller-asserted identity and bound state to verified authorization context.
- Separated ontology, query plan, and exact structured output schema.
- Made answers immutable and linked citations to claims and structured paths.
- Replaced implicit failures with source statuses, conflicts, and completeness.
- Replaced draft-answer polling with MCP Tasks and aligned input with Elicitation.
- Split action definitions from executions and added preview, approval,
  idempotency, preconditions, cancellation, partial effects, and audit semantics.
- Replaced private JSON-RPC error assignments with MCP protocol/tool error mapping.
- Restricted extensions to reverse-DNS namespaces under `extensions`.

### Added

- Normative MCP binding, threat model, benchmarking rules, remediation record,
  migration guide, MCP envelope vectors, and negative behavioral tests.
- Explicit stable-release gates and version-scoped conformance claims.

### Compatibility

This release is intentionally incompatible with 1.1. See
`guides/migration-v1-to-v2.md`. Historical 1.1 examples and backend guides are
archived in versioned directories.

## [1.1.0-beta] - 2026-07-01

- Added compiled query assistance, optional API-surface transparency, query
  clarification, and backend mapping examples.

## [1.0.1-beta] - 2026-06-23

- Added static validation, conformance traceability, and GraphQL/REST/SQL guides.

## [1.0.0-beta] - 2026-06-18

- Published the initial seven-primitive compiled-answer design and schemas.
