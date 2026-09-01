# Repository working guide

MCP-A is a draft MCP tool profile. The current line is `2.0.0-beta`, bound to
MCP `2025-11-25`.

Before changing a contract, read `SPEC.md`, `MCP-BINDING.md`,
`THREAT-MODEL.md`, and `RFC-PROCESS.md`. Normative behavior, schemas, examples,
conformance tests, migration notes, and changelog must move together.

Use the seven canonical tool names: `mcpa.discover`, `mcpa.schema`,
`mcpa.query`, `mcpa.follow_up`, `mcpa.context`, `mcpa.explain`, and
`mcpa.action`. Do not add caller identity fields, private JSON-RPC error codes,
answer polling, or arbitrary top-level extensions.

Top-level examples and schemas are current. Directories named `v1.1` are
historical migration material. Run `make check` after changes.
