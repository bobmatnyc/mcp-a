# MCP-A Enhancement Proposals

MAEPs record substantive design changes. See [`../RFC-PROCESS.md`](../RFC-PROCESS.md)
for review, versioning, and release rules and [`TEMPLATE.md`](./TEMPLATE.md) for
required proposal sections.

## Index

| MAEP | Title | State | Target |
|---|---|---|---|
| [0001](./0001-structured-responses-and-introspection.md) | Domain introspection and structured responses | Accepted historical design | 1.0 beta |
| [0002](./0002-session-management.md) | Session management | Draft; not adopted | 1.x |
| [0003](./0003-action-primitive.md) | Action primitive | Historical draft; superseded in 2.0 by 0006 | 1.x |
| [0004](./0004-hierarchical-schema.md) | Hierarchical and operation-aware schema | Historical draft; superseded in 2.0 by 0006 | 1.x |
| [0005](./0005-compiled-query-assistance.md) | Compiled query assistance | Implemented in 1.1; semantics revised by 0006 | 1.1 beta |
| [0006](./0006-mcp-binding-and-protocol-hardening.md) | MCP binding and protocol hardening | Accepted into the 2.0 beta artifacts | 2.0 beta |

Proposal metadata remains historically intact even when a later proposal
supersedes its behavior. The index states the current relationship so readers
do not mistake old wire shapes for the current contract.

## Submission summary

1. Search existing proposals and issues.
2. Copy `TEMPLATE.md` to `NNNN-short-title.md`.
3. Open a public issue and pull request.
4. Complete the required implementation, security, compatibility, and test analysis.
5. Address the review criteria and minimum review period in `RFC-PROCESS.md`.
6. Update the proposal state, normative artifacts, conformance suite, examples,
   migration guidance, and changelog together.
