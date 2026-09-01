---
Status: DRAFT NORMATIVE
Version: 2.0.0-beta
MCP-Baseline: 2025-11-25
---

# MCP-A 2.0 conformance

A conformance claim is scoped to the profile version, MCP baseline, declared
features, implementation build, and test report. JSON Schema validity is
necessary but not sufficient.

## Bundles

| Bundle | Required features |
|---|---|
| Core | `discovery`, `query.prose`, `provenance.claims`, `failure.partial` |
| Full | Core plus `schema.ontology`, `schema.query-plan`, `query.structured`, `answer.follow-up`, `context.preferences`, `explain`, `action.safe` |
| Extended | Full plus one or more reverse-DNS extension namespaces |

The negotiated feature list is authoritative. Bundle names are shorthand and
MUST NOT be used to infer undeclared optional behavior (SPEC §Profile negotiation).

## Static artifact requirements

- [ ] The server negotiates MCP revision `2025-11-25` and MCP-A `2.0.0-beta`.
- [ ] Its profile capability validates against `profile.capability.json`.
- [ ] Each advertised tool has a self-contained input and output schema.
- [ ] Successful profile results are in MCP `structuredContent`.
- [ ] Tool definitions use the annotations and Task declarations required by
  `MCP-BINDING.md`.
- [ ] Unknown normative top-level fields are rejected; extension fields appear
  only beneath reverse-DNS keys (SPEC §Versioning and extensions).
- [ ] Every shipped example and schema passes `make check`.

## Core runtime requirements

### Authorization isolation

- [ ] No tool accepts `user_id`, tenant, or equivalent caller identity as an
  authority-bearing argument.
- [ ] Domain, record, field, source, and handle access is derived from the MCP
  authorization context and rechecked on every call.
- [ ] Cross-principal, cross-client, and cross-tenant answer-handle probes do
  not reveal whether the object exists.
- [ ] Inbound MCP bearer tokens are not passed to downstream services.
- [ ] Revoked access is reflected on the next call, including follow-up and
  explain paths (SPEC §Authentication).

### Discovery

- [ ] Unauthorized domains are omitted without disclosure.
- [ ] Ordering is deterministic for an unchanged catalog.
- [ ] Cursor and limit behavior is bounded and repeatable.
- [ ] Descriptive guidance is size-limited and treated as untrusted content
  (SPEC §Primitive: `mcpa.discover`).

### Queries and provenance

- [ ] Natural-language and typed plans pass the same validation, cost, and
  authorization gates.
- [ ] Every answer is immutable; refinements cannot change earlier content.
- [ ] Material claims have stable IDs and citations link to those IDs.
- [ ] Structured paths are traceable where structured content is returned.
- [ ] Returned aggregation values are computed deterministically over
  authorized data (SPEC §Deterministic data operations).
- [ ] `as_of`, computed scope, and source statuses describe the actual result.
- [ ] A required source timeout or unusable response produces `partial`, not
  `completed` (SPEC §Partial results and conflicts).

### Error and MCP behavior

- [ ] Malformed MCP envelopes and unknown tools use MCP protocol errors.
- [ ] Recoverable domain failures use MCP tool execution errors with
  `isError: true` and an `error.json` payload.
- [ ] A partial action is a state result, not a no-result tool error.
- [ ] Error text is safe, actionable, and non-enumerating (SPEC §Error model).

## Full runtime requirements

### Schema and structured output

- [ ] Ontology, query capabilities, operations, and output schemas are distinct.
- [ ] Field types, nullability, units, decimal precision, currency, and timezone
  are explicit where applicable.
- [ ] `target: action` returns only operations the principal may invoke.
- [ ] API-surface resources are authorization-filtered, bounded, and never
  automatically fetched from arbitrary HTTP locations.
- [ ] Every `structured` value validates against the returned exact
  `output_schema` (SPEC §Structured output).

### Follow-up, context, and explain

- [ ] A follow-up creates a new ID and sets `parent_answer_id`.
- [ ] Routing reuse is reported and is recomputed after authorization changes.
- [ ] Context modes, namespace isolation, optimistic concurrency, size limits,
  expiry, export, and deletion are tested.
- [ ] Context cannot broaden authorization or store credentials.
- [ ] Explain output is filtered for the current principal and does not expose
  backend topology, secrets, policies, or inaccessible domains
  (SPEC §Primitive: `mcpa.explain`).

### Safe actions

- [ ] Operation definitions include immutable operation/input-schema versions,
  an exact input schema, and safety metadata.
- [ ] A stale pinned operation version fails with `CONFLICT` and no effects.
- [ ] A natural-language action cannot apply effects on its first turn.
- [ ] Effectful operations enforce idempotency policy and preconditions.
- [ ] Duplicate keys return the same execution; changed inputs with the same key
  produce `IDEMPOTENCY_CONFLICT`.
- [ ] Approval displays server, operation, normalized inputs, risk, scope,
  reversibility, and planned effects.
- [ ] Authorization and preconditions are checked immediately before each effect.
- [ ] Applied and failed effects remain visible in `partially_completed`.
- [ ] No-effect failure contains no effects; completed effects are only applied
  or compensated; preview effects are only planned.
- [ ] Cancellation, compensation, audit integrity, and retry behavior are tested
  (SPEC §Primitive: `mcpa.action`).

### Tasks and Elicitation

- [ ] Durable asynchronous work uses MCP Tasks, not answer or execution IDs.
- [ ] Task ownership, TTL, polling interval, progress, cancellation, result
  retrieval, and resource limits pass live tests.
- [ ] Form Elicitation is not used for secrets or credentials.
- [ ] Portable continuation states work when Elicitation is unavailable
  (SPEC §Asynchronous execution).

## Security and abuse tests

- [ ] Source content that contains tool instructions cannot alter routing,
  authorization, output schema, or action decisions.
- [ ] Inline JSON Schemas hit deterministic size, depth, regex, and time limits.
- [ ] Resource references cannot cause SSRF or unauthorized network access.
- [ ] Oversized queries, catalogs, results, citations, task sets, and memory are
  rejected or truncated according to documented limits.
- [ ] Logs redact secrets and support retention, export, and deletion policy.
- [ ] Handle guessing, replay, confused-deputy, stale-approval, and partial-effect
  scenarios from `THREAT-MODEL.md` are covered (SPEC §Security).

## Error-code coverage

Implementations MUST preserve these abstract codes in structured tool errors or
state failures: `UNAUTHENTICATED`, `FORBIDDEN`, `INVALID_REQUEST`,
`DOMAIN_NOT_FOUND`, `ANSWER_NOT_FOUND`, `EXECUTION_NOT_FOUND`,
`OPERATION_NOT_FOUND`, `SCHEMA_NONCONFORMANT`, `AGGREGATION_NOT_ALLOWED`,
`TIMEOUT`, `SOURCE_UNAVAILABLE`, `CONFLICT`, `PRECONDITION_FAILED`,
`RATE_LIMITED`, `IDEMPOTENCY_CONFLICT`, `ACTION_FAILED`, `CANCELLED`, and
`INTERNAL`.

## Claim format

A published claim SHOULD state:

```text
MCP-A 2.0.0-beta / MCP 2025-11-25 / Full
Implementation: <name and immutable build>
Features: <negotiated feature list>
Schema suite: <commit and result>
Runtime suite: <report URI and date>
Security review: <scope and date>
Known deviations: <none or explicit list>
```

Self-attestation is permitted during beta, but MUST be labeled as such. The
project currently provides no certification authority or official badge.
