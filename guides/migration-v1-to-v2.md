# Migrating from 1.1 to 2.0

Version 2.0 is intentionally breaking. A server should expose versions on
separate negotiated connections or distinct tool names during migration.

| 1.1 behavior | 2.0 replacement |
|---|---|
| Unnamespaced primitive names | `mcpa.*` MCP tools |
| Capability block returned by `discover` | MCP initialization experimental capability |
| Caller-provided `user_id` | Verified MCP authorization context |
| `response_schema.kind: domain` | Exact `schema_ref`, bounded `inline`, or `derive` output target |
| Ontology used as result schema | Separate ontology, query plan, and output schema |
| Mutable/reused follow-up answer ID | New immutable answer with `parent_answer_id` |
| Draft answer plus `follow_up` polling | MCP Tasks for durable async work |
| Citation list without claim linkage | Claims plus citation `claim_ids` |
| Implicit or incomplete source failure | Explicit source statuses, conflicts, and completeness |
| Natural-language action may execute immediately | Resolve first; typed approval/preview before effects |
| `action_id` combines definition and run | `operation_id` plus `execution_id` |
| Completed/failed action only | Seven-state lifecycle including partial completion |
| Private JSON-RPC error assignments | MCP protocol errors plus structured tool execution errors |
| Arbitrary unknown fields | Reverse-DNS entries under `extensions` only |

Move former examples and generated clients behind a 1.1 compatibility boundary.
Regenerate clients from the 2.0 schemas, then add live tests for authorization
isolation, idempotency, partial sources/effects, Tasks, and MCP envelopes before
advertising a 2.0 feature.
