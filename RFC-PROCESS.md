---
Status: DRAFT
Version: 2.0.0-beta
Date: 2026-09-01
---

# MCP-A change and release process

Normative changes use MCP-A Enhancement Proposals (MAEPs). The purpose is
public rationale, reviewable trade-offs, interoperability analysis, and a clear
record of which release adopted a change.

## Change classification

An issue or ordinary pull request is sufficient for editorial corrections,
broken links, tests that enforce existing normative text, or schema repairs that
unambiguously restore agreement with that text.

A MAEP is required for a new feature, tool, state, field semantics, error code,
security requirement, conformance requirement, extension point, or incompatible
schema change.

## Proposal states

`Draft` → `Under Review` → `Accepted` or `Rejected` → `Implemented` → `Final`

`Withdrawn` and `Superseded` are terminal alternatives. “Implemented” means the
normative artifacts and validation suite incorporate the proposal; it does not
claim a production reference server exists. Finalization occurs only in a tagged
release.

## Required proposal content

Every MAEP must describe motivation, observable behavior, MCP interaction,
security/privacy impact, compatibility, failure behavior, schema changes,
alternatives, conformance tests, and unresolved questions. The template in
`MAEP/TEMPLATE.md` is authoritative.

## Review

- Assign a public issue and pull request.
- Keep review open for at least 14 calendar days for a normative change unless
  an actively exploited security defect requires an emergency fix.
- Request at least one implementation-oriented and one security-oriented review
  for wire, authorization, state, or action changes.
- Record objections and their resolution in the proposal.
- The maintainer publishes an explicit acceptance or rejection rationale; silence
  alone is not acceptance.
- An emergency change must be narrowly scoped and receive retrospective review
  within 14 days.

The initial maintainer is Robert Matsuoka. Maintainer decisions, recusals, and
conflicts of interest should be recorded in the relevant issue. Once three or
more independent implementations exist, the project should publish a separate
multi-maintainer governance charter before claiming community governance.

## Semantic versioning

MCP-A uses Semantic Versioning, including during beta:

- **Major**: incompatible request, response, state, security, or existing bundle change.
- **Minor**: optional negotiated feature that preserves existing feature semantics.
- **Patch**: compatible correction or clarification.

Adding a requirement to an existing conformance bundle is major. A pre-release
label does not make an incompatible change a patch. Domain schemas evolve
independently with immutable schema IDs and explicit deprecation.

## Release gates

A beta may be tagged when normative text, schemas, examples, changelog, and
static tests agree. Stable 2.0 additionally requires the release gates in SPEC
§24: independent clients and servers, cross-language interoperability,
benchmarks, adversarial security review, hosted schema bundles, and a passing
reference implementation.

Release notes must list negotiated features, breaking changes, migration steps,
known deviations, security-impacting changes, and exact artifact digests.

This independent repository may later propose the profile through the MCP
project's then-current contribution process. That is an aspiration, not a claim
of endorsement or a predetermined governance outcome.
