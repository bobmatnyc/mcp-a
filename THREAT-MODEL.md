---
Status: DRAFT NORMATIVE SECURITY REQUIREMENTS
Version: 2.0.0-beta
---

# MCP-A Threat Model

## 1. Assets and trust boundaries

Protected assets include source data, authorization metadata, downstream
credentials, query and action inputs, compiled answers, citations, memory,
feedback, state handles, operation definitions, effects, and audit records.

The following are separate trust boundaries:

- MCP client and model;
- MCP-A server;
- routing or compilation model;
- source systems and retrieved content;
- downstream authorization servers and APIs;
- storage for answers, executions, tasks, memory, and logs;
- user approval UI.

Source content, tool arguments, ontology descriptions, API descriptions,
examples, citations, and model output are untrusted data. None receive protocol
or policy authority because they are fluent or appear instruction-like.

## 2. Required mitigations

### 2.1 Identity, audience, and delegation

Servers MUST derive the principal from verified authorization context, validate
token audience, and reject caller-asserted identity. State objects MUST be bound
to principal, client, tenant, and intended audience.

Inbound MCP tokens MUST NOT be passed through to downstream APIs. Servers MUST
use service credentials, token exchange, or separately authorized delegated
tokens with least privilege. Delegation chains and scope elevation MUST be
auditable.

### 2.2 Authorization

Authorization MUST be enforced at domain, entity, field, row, aggregation,
operation, and effect boundaries. It MUST be re-evaluated immediately before a
source query or effect and on every handle retrieval.

Unknown and unauthorized objects SHOULD be externally indistinguishable.
Aggregates MUST be computed over the currently authorized record set. Cached
aggregates MUST be recomputed when revoked access cannot be subtracted exactly.

### 2.3 Prompt and data injection

Servers MUST structurally separate instructions, query plans, source data, and
citations. Retrieved text MUST NOT be concatenated into privileged prompts
without delimiting, provenance labels, and an instruction to treat it as data.

Servers MUST validate a model-produced query plan against ontology,
authorization, cost, and operation allowlists before execution. A model MUST
NOT directly select credentials, endpoints, authorization scopes, or approval
outcomes.

Output sanitization MUST prevent source content from forging MCP messages,
citations, approval UI, or action results. Clients SHOULD label citations and
excerpts as untrusted source material.

### 2.4 Actions and user intent

Authorization is not approval. Critical, irreversible, destructive, financial,
and external-communication operations require explicit user approval unless an
audited policy and prior user grant permit unattended execution.

Servers MUST bind approvals to the exact operation, normalized inputs, planned
effects, principal, client, expiry, and execution. Material changes invalidate
approval. Approvals MUST be single-use unless the user explicitly grants a
bounded repeat policy.

Effectful requests MUST use idempotency and precondition controls as required by
the operation definition. Partial effects MUST be reported and never hidden as
a generic failure.

### 2.5 Handles, tasks, and replay

Handles MUST have at least 128 bits of unpredictable entropy or equivalent
resistance, bounded TTLs, secure storage, and authorization-context binding.
Servers MUST rate-limit failed lookups and polling to resist enumeration.

Idempotency records MUST live at least as long as the maximum legitimate retry
window. Reusing a key with different normalized inputs MUST fail with
`IDEMPOTENCY_CONFLICT`.

Task cancellation does not prove downstream cancellation. If an effect may
continue after cancellation, the resulting execution MUST accurately report
the eventual effect state.

### 2.6 SSRF and transparency resources

Clients MUST NOT automatically fetch HTTP URLs found in `api_surfaces` or other
MCP-A metadata. Servers SHOULD use authorization-scoped MCP resources.

Any component that fetches a supplied URL MUST enforce scheme and host policy,
block private/link-local/metadata destinations unless explicitly required,
validate every redirect, constrain DNS rebinding, limit response size and time,
and avoid forwarding ambient credentials.

### 2.7 Resource exhaustion

Servers MUST enforce limits for:

- query text and inline-schema size;
- schema reference depth, regex complexity, and validation time;
- fan-out source count and backend cost;
- result rows, citations, claims, and API-surface size;
- hierarchical schema depth;
- concurrent and retained Tasks;
- polling and failed handle lookups;
- context namespaces, values, and retention;
- action attempts and clarification/approval rounds.

Rate-limit errors SHOULD include safe retry guidance.

### 2.8 Privacy and retention

Operators MUST document purpose, retention, access, export, and deletion for
queries, answers, citations, feedback, memory, executions, effects, and logs.
Clients and servers MUST NOT put credentials or payment secrets in ordinary
MCP-A memory or form input.

Logs SHOULD store identifiers, hashes, policy decisions, and redacted summaries
rather than complete sensitive prompts or answers. Deletion requests MUST cover
derived memory and feedback unless retention is legally required.

### 2.9 Explainability and metadata leakage

`explain` and errors MUST filter unauthorized domain names, resource existence,
record counts, backend endpoints, query text containing sensitive values,
credentials, policy internals, and other users' feedback. Timing and source
status can be side channels; return only information needed to understand the
caller's own result.

### 2.10 Audit integrity

Action audit records MUST include authenticated principal, client, tenant,
operation ID and version, input-schema ID, normalized-input digest, idempotency key digest, policy decision,
approval evidence, preconditions, attempts, effects, compensation, timestamps,
and correlation IDs. Records SHOULD be append-only or tamper-evident and MUST
have access and retention controls.

## 3. Abuse cases for conformance testing

Full security testing includes at least:

1. forged `user_id` or tenant fields;
2. cross-user answer, task, execution, and memory handle access;
3. source text instructing the model to alter routing or perform an action;
4. unauthorized fields hidden inside a model-produced query plan;
5. aggregate recomputation after mid-session access revocation;
6. duplicate action delivery before and after timeout;
7. partial multi-system mutation and failed compensation;
8. approval replay after normalized inputs change;
9. private-network and redirect URLs in API-surface metadata;
10. schema bombs, poll storms, fan-out amplification, and memory exhaustion;
11. explanation requests designed to enumerate hidden domains;
12. log and error inspection for secret or cross-tenant leakage.

## 4. Security non-claims

Schema validation, citations, RBAC checks, deterministic aggregates, model
confidence, and an approval boolean do not independently establish security.
Conformance requires the combined controls above and deployment-specific risk
analysis.
