# Positioning and non-goals

MCP-A is an application profile on top of MCP, not a replacement transport and
not a competing authorization protocol. It standardizes the boundary between a
client and a server that already owns domain semantics and answer compilation.

## When it fits

Use MCP-A when most of these are true:

- one question routinely spans several sources or domain concepts;
- the server can publish a stable ontology and typed query capabilities;
- provenance, completeness, and conflicts matter to the caller;
- deterministic aggregation belongs next to the data;
- multi-turn refinement should preserve an auditable prior result;
- operations need typed discovery, previews, approval, idempotency, and effect logs.

Direct MCP tools are often simpler when the catalog is small, calls are already
well scoped, or the client must control orchestration. MCP-A adds server
complexity and creates a larger trust boundary; it should earn that cost through
measured workload results.

## Relationship to adjacent patterns

| Pattern | Primary concern | MCP-A relationship |
|---|---|---|
| MCP tools/resources | General model-to-service interoperability | MCP-A uses them and adds a compiled-answer contract. |
| RAG | Retrieve context for generation | A server may use RAG internally, but must still expose provenance and coverage. |
| GraphQL/OpenAPI/SQL | Backend data or operation surface | These may back a domain; MCP-A publishes filtered semantic capabilities, not the raw surface by default. |
| Agent frameworks | Planning and orchestration | MCP-A may reduce some client planning but does not standardize agents. |
| Workflow/transaction engines | Durable business execution | MCP-A actions report effects; they do not create cross-system atomicity. |

## Claims

The repository does not currently claim universal performance, precision, or
cost superiority over ordinary MCP. Comparative claims must state the workload,
baseline, models, token accounting, latency percentiles, correctness metric,
failure behavior, and reproducible artifacts as required by
[`BENCHMARKING.md`](./BENCHMARKING.md).

## Naming

“MCP Answers Profile” describes the profile's compiled-result focus. The name
does not imply endorsement by the Model Context Protocol project or inclusion
in the base MCP specification.
