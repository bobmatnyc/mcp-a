# Implementer guides

These guides are non-normative. Use `SPEC.md`, `MCP-BINDING.md`, the top-level
schemas, and `CONFORMANCE.md` to resolve contract questions.

- [`implementation.md`](./implementation.md) describes a layered server architecture.
- [`provenance.md`](./provenance.md) covers claims, citations, freshness, conflicts, and partial coverage.
- [`actions.md`](./actions.md) covers operation discovery, approval, idempotency, and partial effects.
- [`migration-v1-to-v2.md`](./migration-v1-to-v2.md) lists breaking changes from 1.1.
- [`v1.1/`](./v1.1/) contains the former backend mapping and prompt guides for historical reference only.

The archived guides use 1.1 fields and semantics. They should not be copied into
a 2.0 implementation without applying the migration guide.
