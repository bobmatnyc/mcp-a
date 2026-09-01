# Implementation architecture

A practical MCP-A server can be divided into six layers.

1. **MCP edge** handles initialization, authorization integration, tools,
   resources, Tasks, Elicitation, cancellation, and protocol errors.
2. **Authorization context** resolves principal, client, tenant, scopes, and
   policy attributes. No tool argument can override it.
3. **Semantic catalog** publishes authorization-filtered domains, ontology,
   query capabilities, operation definitions, and immutable schema versions.
4. **Planner** converts natural language or accepts a typed plan, then runs the
   same semantic, cost, authorization, and output-schema checks.
5. **Connectors and deterministic executor** use least-privilege downstream
   credentials, parameterized queries, bounded fan-out, and ordinary code for
   aggregation.
6. **Result and audit store** persists authorization-bound immutable answers,
   executions, effects, task references, expiry, and redacted evidence.

Keep the planner's proposed plan separate from the executed plan. Authorization
or source capability may require the executor to reject or safely rewrite a
proposal; the response reports what actually ran.

## Backend mapping

GraphQL, REST, SQL, search, and application APIs are implementation details.
Map their types to stable semantic IDs and declare only operations the server
can enforce correctly. Raw backend schemas should be exposed only as filtered,
bounded MCP resources when they materially help a client.

For SQL, parameterize all values and allowlist identifiers. For REST and
GraphQL, enforce origin allowlists, redirect policy, response limits, and field
authorization. Never treat retrieved descriptions or records as instructions.

## State and lifecycle

Answer and execution IDs identify profile objects; Task IDs identify MCP async
jobs. Store their distinct ownership and retention metadata. A Task result may
contain an answer or execution, but one handle cannot substitute for another.

The safest default is short bounded retention, explicit deletion behavior,
constant-shape lookup failures, and current-policy authorization on every read.
