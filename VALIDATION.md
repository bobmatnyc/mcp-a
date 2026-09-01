# Validation

The repository has three distinct validation layers.

## Static suite

`make check` runs formatting/lint checks, validates every top-level schema as
JSON Schema draft 2020-12, validates every current example against its assigned
schema, checks manifest completeness, tests cross-document error-code coverage,
and exercises negative protocol invariants.

The suite resolves `$ref` values from an offline registry. Network access is
not required and should not be enabled merely to validate a schema bundle.

## Behavioral invariants

The tests explicitly cover rules that positive examples cannot prove:

- caller-asserted identity is rejected;
- ambiguous context shapes are rejected;
- structured content validates against its exact embedded output schema;
- partial actions contain both successful and failed effects;
- failed actions cannot hide applied effects;
- MCP initialization and tool-error vectors use the expected envelope shape.

These tests validate the design artifacts, not an implementation.

## Live conformance

A runtime claim also requires the authorization isolation, source-failure,
idempotency, approval, cancellation, Task, Elicitation, retention, and abuse
tests in [`CONFORMANCE.md`](./CONFORMANCE.md). Implementations should publish an
immutable test report tied to a build and profile version.

## Historical vectors

Version 1.1 examples are retained under `examples/v1.1/` and
`schemas/examples/v1.1/`. They are migration inputs, not 2.0 conformance cases.
