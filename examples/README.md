# MCP-A 2.0 examples

Top-level JSON files are the current `2.0.0-beta` profile vectors and are
validated in CI. They form one sales-oriented scenario while emphasizing
different protocol states.

| Steps | What they demonstrate |
|---|---|
| `00` | Negotiated profile capability. |
| `01` | Bounded, authorization-filtered discovery. |
| `02`–`04` | Separate domain ontology, query capabilities, and action operations. |
| `05` | Typed query plan and exact structured output schema. |
| `06`–`06b` | Portable input request and continuation. |
| `07` | Partial source coverage. |
| `08` | Immutable follow-up with a new answer ID. |
| `09`–`10` | Natural-language action resolution, approval, and completion. |
| `11` | Partial multi-effect completion. |
| `12` | Bounded context read. |
| `13` | Authorization-filtered answer explanation. |
| `14` | Structured tool execution error. |

`mcp/` contains complete MCP envelope vectors for initialization, a tool call,
and a tool execution error. These are intentionally separate from the profile
payload manifest because the top-level JSON Schemas describe tool arguments and
results, not JSON-RPC envelopes.

`v1.1/` preserves the former examples for migration work. They do not validate
against the 2.0 schemas and MUST NOT be presented as current conformance cases.
