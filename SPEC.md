---
Status: DRAFT
Version: 2.0.0-beta
Date: 2026-09-01
MCP-Baseline: 2025-11-25
---

# MCP-A — MCP Answers Profile Specification (2.0.0-beta)

## 1. Abstract

MCP-A is a versioned Model Context Protocol tool profile for servers that
compile answers and actions across one or more information domains. It defines
seven namespaced MCP tools, common provenance and failure semantics, a domain
semantic model, structured query plans, immutable answer handles, and
retry-safe action executions.

MCP-A's design hypothesis is that server-side classification, deterministic
data operations, and consolidation can reduce client-model orchestration work
for suitable workloads. It does not guarantee lower latency, cost, or higher
accuracy merely by conforming. Performance and quality claims MUST be supported
by measurements conforming to `BENCHMARKING.md`.

## 2. Normative language and artifacts

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are to be
interpreted as described by RFC 2119 and RFC 8174.

The normative artifacts are:

- this specification;
- `MCP-BINDING.md`;
- `THREAT-MODEL.md` where it states required mitigations;
- top-level JSON Schemas under `schemas/`;
- `CONFORMANCE.md`.

If prose and a JSON Schema disagree, the stricter requirement applies until the
erratum is resolved. Examples and guides are non-normative.

## 3. Scope

MCP-A specifies:

- a binding to MCP revision `2025-11-25`;
- profile version and feature negotiation;
- seven tools: `mcpa.discover`, `mcpa.schema`, `mcpa.query`, `mcpa.action`,
  `mcpa.follow_up`, `mcpa.context`, and `mcpa.explain`;
- domain, query, answer, provenance, action, and error semantics;
- authorization-context binding and safe state handles;
- conformance bundles and executable validation requirements.

MCP-A does not specify routing models, backend APIs, storage engines, user
interfaces, or a universal ontology. It constrains their externally observable
behavior only where interoperability or safety requires it.

## 4. Relationship to MCP

Every MCP-A server is an MCP server. MCP initialization, authorization,
`tools/list`, `tools/call`, tool results, Tasks, Elicitation, progress,
cancellation, and protocol errors retain their MCP meanings. MCP-A does not
redefine them.

`MCP-BINDING.md` is the normative wire binding. In particular:

- profile support is negotiated during MCP initialization;
- MCP-A tool inputs are the corresponding request schemas;
- successful and domain-level failure payloads are returned in MCP
  `structuredContent`;
- tool execution failures use MCP `isError: true`;
- malformed MCP messages and unknown tools use MCP protocol errors;
- MCP Tasks are used for durable asynchronous execution;
- MCP Elicitation is preferred for interactive input and approval when the
  client declares it.

## 5. Terminology

- **Authenticated principal**: identity established by the MCP authorization
  context. It is never established by a tool argument.
- **Authorization context**: verified principal, client, tenant, audience,
  scopes, and relevant policy attributes for a request.
- **Domain**: an authorization-filtered semantic boundary over information and
  operations.
- **Ontology**: the domain's entity, field, measure, dimension, relationship,
  unit, and operation vocabulary.
- **Query plan**: a typed description of selections, filters, grouping,
  aggregations, ordering, and limits.
- **Output schema**: the exact JSON Schema against which `structured` is
  validated. It is distinct from the ontology and query plan.
- **Answer**: an immutable compiled result identified by `answer_id`.
- **Claim**: an addressable assertion in an answer. Citations refer to claim
  IDs rather than merely accompanying the answer as an unlinked list.
- **Operation**: an action definition identified by `operation_id`.
- **Execution**: one invocation of an operation, identified by `execution_id`.
- **Effect**: an attempted or applied external state change.
- **Completeness**: `complete`, `partial`, or `unknown` assessment of the
  requested source coverage.

## 6. Profile negotiation

Servers MUST advertise the `io.modelcontextprotocol/mcpa` capability during MCP
initialization as defined by `schemas/profile.capability.json` and
`MCP-BINDING.md`. Clients MAY advertise supported exact versions and features using
`schemas/profile.client-capability.json`. The server capability includes:

- `versions`: supported exact MCP-A semantic versions;
- `selectedVersion`: the version used for the connection;
- `conformance`: the version-scoped convenience bundle;
- `features`: individual feature identifiers;
- `schemaBaseUri`: optional stable location for published schemas.

Clients MUST NOT infer optional features solely from a conformance bundle.
Clients MUST use the negotiated version and feature set, then use `tools/list`
as the source of truth for callable tools.

## 7. Authentication, authorization, and state binding

All MCP-A tools require an authenticated authorization context. Request schemas
MUST NOT contain a caller-asserted `user_id`.

Servers MUST:

1. validate the token audience and authorization context according to MCP;
2. authorize each domain, record, field, operation, and effect separately;
3. use separate credentials or token exchange for downstream systems and MUST
   NOT pass an inbound MCP token through to a downstream API;
4. bind every answer, execution, task, feedback object, and memory namespace to
   the principal, client, and tenant context that created it;
5. re-evaluate current authorization on every retrieval, refinement,
   explanation, continuation, and effect;
6. treat state handles as opaque names rather than bearer capabilities;
7. use unguessable handles, bounded retention, and non-enumerating lookup
   behavior.

For unauthorized handle access, servers SHOULD return the same externally
observable result as an unknown handle unless an administrator-only diagnostic
scope was explicitly granted.

## 8. Common result semantics

### 8.1 Immutable answers

An `answer_id` identifies immutable content and routing evidence. A refinement
MUST create a new `answer_id` and set `parent_answer_id`. Servers MUST NOT mutate
an earlier answer in place.

Answers MUST include `revision`, `created_at`, `as_of`, `computed_scope`,
`completeness`, `source_statuses`, and claim-linked `citations`. A complete
single-source answer still reports one successful source status.

### 8.2 Provenance

Each factual prose assertion that materially contributes to the answer SHOULD
have a stable claim ID. Every structured field or row SHOULD be traceable to
one or more claims or citations.

A citation MUST identify `citation_id`, `source_system`, `retrieved_at`, and the
`claim_ids` it supports. When available it SHOULD identify the domain, entity,
record, record version, source URI, and source `as_of` time.

Citation excerpts and source documents are untrusted data. They MUST NOT be
interpreted as protocol, system, developer, or user instructions.

### 8.3 Partial results and conflicts

Source failures MUST NOT be hidden. A partial result includes:

- `status: "partial"`;
- `completeness: "partial"`;
- one `source_statuses` entry per attempted source;
- a safe summary of omitted coverage;
- conflicts that could not be deterministically reconciled.

A server MUST NOT label a result complete when an intended source failed,
timed out, returned unusable data, or was skipped after planning, unless the
query plan explicitly declared that source optional.

### 8.4 Freshness

`freshness_seconds` in discovery is a catalog estimate. An answer's `as_of` and
per-source `as_of` values are authoritative for that answer. For multi-source
answers, the server MUST document whether top-level `as_of` is the oldest,
newest, or a consistency snapshot time; MCP-A defines it as the oldest
contributing source time by default.

### 8.5 Confidence

Confidence is OPTIONAL. A server that reports it MUST identify a documented
`confidence_method` and calibration version. Scores from different methods are
not assumed comparable. MCP-A does not impose an arbitrary maximum score.

## 9. Domain semantic model

A domain schema response separates:

1. `ontology`: entities, fields, data types, formats, measures, dimensions,
   units, relationships, and stable semantic IDs;
2. `query_capabilities`: the supported query-plan grammar, filters, ordering,
   grouping, aggregations, limits, and consistency options;
3. `operations`: authorization-filtered action definitions with JSON Schema
   inputs and safety metadata;
4. `api_surfaces`: optional, authorization-filtered transparency resources.

Canonical field data types are `string`, `boolean`, `integer`, `number`,
`decimal`, `date`, `date-time`, `duration`, `enum`, `reference`, `object`, and
`array`. Decimal precision, currency, timezone, and nullability MUST be explicit
where applicable.

An ontology is not an output schema. A payload MUST NOT claim conformance to a
domain merely because its fields were derived from that domain.

## 10. Primitive: `mcpa.discover`

`discover` returns the domains available to the current authorization context.
It does not authenticate the caller or negotiate profile capabilities.

The request supports `filter`, `cursor`, and bounded `limit`. Cursors are opaque.
The response includes `domains`, `next_cursor` when more results exist,
`total_count` when inexpensive to compute, and `as_of`.

Servers MUST:

- exclude unauthorized domains without revealing their existence;
- return domains in deterministic order while the underlying set is unchanged;
- ensure examples and query guidance are untrusted descriptive data, not
  instructions with elevated authority;
- cap response size and query-guidance size;
- provide a stable `domain_id`, `schema_version`, status, freshness estimate,
  and safe scope summary for every domain.

## 11. Primitive: `mcpa.schema`

The request requires `domain_id` for every target and accepts:

- `target`: `domain`, `query`, or `action`;
- `operation_id` only with `target: "action"`;
- hierarchical `path` and bounded `depth`;
- optional inclusion flags.

`target: "domain"` returns the ontology. `target: "query"` returns
`query_capabilities` and the structured query-plan schema. `target: "action"`
returns operation summaries or one operation's exact input schema.

API transparency MUST use `api_surfaces[]`. Each entry is either bounded inline
content or, preferably, an MCP resource URI plus media type, content digest,
size, and schema version. Clients MUST NOT automatically fetch arbitrary HTTP
URLs supplied in an API-surface field. Servers MUST remove unauthorized paths,
operations, table names, and security metadata before exposure.

Drilled responses MUST state whether they are truncated and provide valid next
paths. Unknown and unauthorized paths MUST not reveal sibling names.

## 12. Primitive: `mcpa.query`

### 12.1 Request

A new query supplies exactly one of:

- `question`: natural-language intent; or
- `query_plan`: a typed plan conforming to the negotiated query-plan schema.

It may also supply a response target, timeout preference, consistency
preference, language, and maximum result size.

A continuation supplies `query_id` and `inputs` requested by an earlier
`input_required` result. It MUST NOT repeat or replace the original question or
query plan.

The server MUST authorize and validate any inferred or supplied query plan
before execution. Natural-language content MUST never bypass the same field,
row, aggregation, cost, and source policies applied to a typed plan.

### 12.2 Structured output

A response target is one of:

- `schema_ref`: a stable, resolvable schema identifier;
- `inline`: a bounded JSON Schema supplied by the client;
- `derive`: request that the server derive and return the concrete schema from
  the domain semantics and query plan.

`domain` is no longer a valid response-schema kind because an ontology does not
define a concrete result shape.

Whenever `structured` is present, `output_schema_id` and `output_schema` MUST be
present, and `structured` MUST validate against `output_schema`. The schema ID
SHOULD be content-addressed. Inline schemas are untrusted input and MUST be
subject to size, reference-depth, regex-complexity, and evaluation-time limits.

### 12.3 Response states

A query response has exactly one state:

- `completed`: complete answer; requires prose or structured content;
- `partial`: usable but incomplete answer with source failures or conflicts;
- `input_required`: no answer yet; requires a structured input request.

An `input_required` response MUST NOT contain final answer or structured result
fields. A server MUST attempt safe deterministic defaults and entity resolution
before requesting input, but MUST NOT silently choose among materially
different interpretations.

Long-running queries MUST use MCP Tasks when that feature is negotiated. They
MUST NOT create an ad hoc polling answer.

## 13. Primitive: `mcpa.follow_up`

`follow_up` refines or drills an existing immutable answer. The request requires
`answer_id` and exactly one of `refinement` or `drill_id`.

The response uses the query response contract and MUST create a new answer with
`parent_answer_id` set to the requested answer. The server MAY reuse prior
routing only when it remains semantically valid, authorization-correct, and
fresh enough for the refinement. `routing.reuse` MUST state `reused`,
`replanned`, or `recomputed_for_authorization`.

Post-hoc filtering MUST NOT be used when authorization changes or aggregate
data prevents correct removal of newly inaccessible contributions.

`follow_up` is not a task polling operation.

## 14. Primitive: `mcpa.context`

`context` manages user-approved preferences and bounded application memory. It
does not accept or establish identity, and it does not expose raw role lists,
security policy, or internal authorization topology.

Requests use an explicit `mode`: `read`, `set`, `append`, or `clear`. Writes are
namespaced and may include an expected version for optimistic concurrency.
Responses include namespace versions, retention/expiry metadata, and enforced
size limits.

Servers MUST support deletion, MUST isolate namespaces by authorization
context, MUST define append behavior per value type, and MUST NOT store secrets,
credentials, or source instructions in ordinary profile memory. Memory is
OPTIONAL for query behavior and MUST NOT silently broaden authorization.

## 15. Primitive: `mcpa.explain`

`explain` accepts exactly one `answer_id` or `execution_id`. It returns evidence
about the authenticated principal's own object only.

For answers it SHOULD include the authorized domains considered, query-plan
summary, routing reuse, source statuses, conflict handling, confidence method,
and freshness. For executions it SHOULD include operation resolution, policy
and approval decisions, precondition evaluation, attempts, and effect statuses.

Alternative routings and scores are OPTIONAL; servers MUST NOT invent
counterfactuals merely to satisfy a field. Explanations MUST filter inaccessible
domain names, backend topology, policy internals, secrets, and other users'
feedback.

Feedback storage requires a disclosed retention policy and deletion mechanism.

## 16. Primitive: `mcpa.action`

### 16.1 Operation discovery

Operations are discovered through `mcpa.schema` with `target: "action"`. Each
operation definition includes:

- `operation_id`, immutable `operation_version`, title, and description;
- exact input JSON Schema and immutable `input_schema_id`;
- required authorization scopes;
- `risk`: `low`, `moderate`, `high`, or `critical`;
- `effect_class`: `read`, `create`, `update`, `delete`, `send`, `financial`,
  `execute`, or `other`;
- `approval`: `never`, `policy`, or `always`;
- `idempotency`: `required`, `supported`, or `unsafe`;
- reversibility and compensation metadata;
- relevant MCP tool annotations.

### 16.2 Request

A new action supplies either:

- `operation_id` plus typed `inputs`; or
- a natural-language `request` to resolve.

A typed request MAY include `operation_version` to pin the definition observed
during discovery. If it no longer matches, the server MUST return `CONFLICT`
without applying effects and provide safe guidance to refresh the operation.
Every action response identifies the operation version actually used.

A natural-language-only request MUST NOT apply effects on its first turn. It
must first return a preview, input request, or approval request containing the
resolved operation and normalized inputs.

Effectful operations require `idempotency_key` unless their operation definition
explicitly declares idempotency unsafe and approval is always required. The
request may include preconditions, preview preference, and timeout.

A continuation supplies `execution_id` and exactly one of additional `inputs`,
an `approval` decision, or `cancel: true`.

### 16.3 Response states

An action response has exactly one state:

- `input_required`;
- `approval_required`;
- `preview`;
- `completed`;
- `partially_completed`;
- `failed`;
- `cancelled`.

`execution_id` is stable across the execution lifecycle. Every effect reports
its own status: `planned`, `applied`, `failed`, `compensated`, or
`compensation_failed`.

Servers MUST:

- authorize immediately before each effect;
- verify preconditions immediately before mutation;
- deduplicate retries by authorization context, operation, and idempotency key;
- return the prior execution state for a safe duplicate;
- distinguish no-effect failure from partial completion;
- never claim rollback or atomicity that the backing systems did not provide;
- include applied effects even when later effects fail;
- require explicit approval for critical risk and for irreversible destructive,
  financial, or external-communication operations unless a separately audited
  policy and user grant explicitly permits unattended execution;
- preserve a tamper-evident audit record.

RBAC alone is not evidence of user intent.

## 17. Deterministic data operations

Advertised aggregations and deterministic transformations MUST be computed by
database, resolver, or ordinary program logic over authorized source data.
They MUST NOT be numerically estimated by a learned model.

The ontology MUST identify supported aggregations per measure and the query
capability MUST identify valid groupings and filters. A result MUST identify the
query plan actually executed. Disambiguation decisions that materially affect
results MUST be exposed as resolved terms or as an input request.

## 18. Asynchronous execution

MCP Tasks are the normative durable execution state machine. When the negotiated
MCP and MCP-A capabilities allow a task-augmented tool call, servers MUST use
MCP task IDs, statuses, TTLs, polling intervals, result retrieval, progress,
ownership binding, and cancellation semantics.

MCP-A answer and execution IDs remain domain objects and MUST NOT be substituted
for task IDs. A completed task returns the ordinary MCP-A tool result.

Servers MUST enforce per-principal concurrency, maximum TTL, polling-rate, and
retained-result limits.

## 19. Input and approval interaction

When MCP Elicitation is negotiated, a server SHOULD use form elicitation for
non-sensitive structured input and SHOULD present approval context through the
client's human-interaction flow. Secrets and credentials MUST NOT be requested
through ordinary form elicitation or stored in MCP-A context.

When Elicitation is unavailable, the portable `input_required` and
`approval_required` result states allow the client to collect and return user
input in a subsequent call. Clients MUST show the requesting server, resolved
operation, normalized inputs, risk, and planned effects before approval.

## 20. Error model

MCP-A defines abstract execution error codes in `schemas/error.json`. They are
carried inside tool execution errors or state-specific failure payloads. MCP-A
does not reserve private JSON-RPC numeric codes.

Protocol-level malformed messages, unknown tools, and invalid MCP envelopes use
the MCP/JSON-RPC errors defined by MCP. Domain validation, authorization,
upstream, precondition, schema, rate-limit, and business errors are tool
execution errors so clients and models can recover.

Errors include `code`, safe `message`, `retryable`, optional `retry_after_ms`,
and namespaced detail. Error messages MUST NOT reveal inaccessible resource
existence, secrets, internal URLs, SQL text containing sensitive values, or
other tenants' identifiers.

## 21. Security, privacy, and resource controls

`THREAT-MODEL.md` is required reading for implementers. Conformant servers MUST
implement its required mitigations, including prompt-injection boundaries,
input/output sanitization, least privilege, rate limits, handle binding, SSRF
protection, retention controls, secure audit logging, and safe explanations.

All collection and storage of query text, source excerpts, answers, action
inputs, effects, feedback, and memory MUST have documented purpose, retention,
access, export, and deletion behavior. Sensitive values SHOULD be redacted or
tokenized in logs. Logging a complete answer is not required for conformance.

## 22. Conformance

Conformance claims are scoped to an MCP-A version and MCP baseline.

- **Core 2.0**: negotiation, `discover`, `query`, provenance, authorization,
  partial failure, errors, and Core security controls.
- **Full 2.0**: Core plus `schema`, structured query/output, `follow_up`,
  `context`, `explain`, safe `action`, MCP Tasks when supported by the baseline,
  and Full security controls.
- **Extended 2.0**: Full plus namespaced extensions.

The negotiated `features` list is authoritative. A bundle name is shorthand.
A server MUST NOT claim runtime conformance solely because its examples pass
JSON Schema validation. It must pass the applicable schema, negative,
authorization-isolation, task, retry/idempotency, partial-failure, and MCP
envelope tests defined by `CONFORMANCE.md`.

The standardized feature identifiers and dependencies are:

| Feature | Requires |
|---|---|
| `discovery` | `mcpa.discover` |
| `query.prose` | `mcpa.query` |
| `provenance.claims` | `query.prose` |
| `failure.partial` | `provenance.claims` |
| `schema.ontology` | `mcpa.schema` |
| `schema.query-plan` | `mcpa.schema` |
| `query.structured` | `schema.query-plan`, `provenance.claims` |
| `answer.follow-up` | `query.prose`, `mcpa.follow_up` |
| `context.preferences` | `mcpa.context` |
| `explain` | `provenance.claims`, `mcpa.explain` |
| `action.safe` | `mcpa.schema`, `mcpa.action` |

Servers MUST NOT advertise a feature without its dependencies. Vendor feature
identifiers MUST begin with a reverse-DNS owner prefix, such as
`com.example.batch-query`; they MUST NOT reuse or redefine standardized names.

## 23. Versioning and extensions

MCP-A uses Semantic Versioning.

- Major: incompatible request, response, state, security, or conformance change.
- Minor: optional negotiated feature that does not change existing feature
  semantics or invalidate an existing version-scoped claim.
- Patch: compatible clarification or defect correction.

Adding a required tool or behavior to an existing conformance bundle is a major
change. Domain schemas have independent immutable `schema_version` and
`schema_id` values; evolution and deprecation rules are advertised per domain.

Extensions MUST appear beneath `extensions` and use reverse-DNS names, for
example `{"com.example/trace": {...}}`. Clients MUST ignore unknown extension
namespaces but MUST NOT ignore unknown normative top-level fields. Extension
data MUST NOT weaken required authorization, validation, approval, provenance,
or failure semantics.

## 24. Open implementation work

Before 2.0 stable, the project requires:

1. at least two independent server implementations and two independent clients;
2. a cross-language interoperability event;
3. published benchmark results for representative workloads;
4. adversarial security review of query, source content, handles, and actions;
5. stable hosted and bundled schema artifacts;
6. a reference implementation that passes the behavioral conformance suite.

These are release gates, not evidence currently claimed by this repository.

## 25. References

- `MCP-BINDING.md`
- `THREAT-MODEL.md`
- `BENCHMARKING.md`
- `CONFORMANCE.md`
- `REVIEW-REMEDIATION.md`
- `MAEP/0006-mcp-binding-and-protocol-hardening.md`
- Model Context Protocol revision `2025-11-25`
- RFC 2119, RFC 8174, RFC 8707, RFC 9728, OAuth 2.1
