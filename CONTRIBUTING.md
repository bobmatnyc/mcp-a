---
Version: 2.0.0-beta
---

# Contributing

Use an issue for questions, editorial fixes, broken links, and reports that the
schemas or tests disagree with existing normative text. Use a MAEP for any
change to observable protocol behavior, security requirements, wire shapes,
feature bundles, or extension semantics.

Normative work must update all affected artifacts in one change:

- `SPEC.md` and `MCP-BINDING.md`;
- threat model and benchmarking rules where relevant;
- JSON Schemas and current examples;
- conformance and negative tests;
- migration guidance and changelog;
- a MAEP with compatibility and security analysis.

Run `make check` before opening a pull request. Include the exact test result and
state whether the change is major, minor, or patch under `RFC-PROCESS.md`.

Keep examples fictional and free of real secrets, identities, customer data,
tokens, or internal endpoints. Security reports that could enable exploitation
should use the repository's private security-reporting channel when one is
configured; otherwise contact the maintainer before opening a public exploit.

Contributions to specification text, schemas, and examples are accepted under
CC BY 4.0. If executable implementation code is added later, its software
license must be declared separately rather than assumed from the document
license.

Critique the design directly and treat contributors respectfully.
