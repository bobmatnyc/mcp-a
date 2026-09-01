# Provenance and partial results

Provenance should answer four separate questions:

1. What assertions did the server make?
2. Which evidence supports each assertion?
3. Which intended sources succeeded, failed, or were skipped?
4. What authorized data scope and time does the answer represent?

Represent material assertions as `claims`. Link each citation to one or more
claim IDs; for structured results, also attach relevant JSON Pointer paths to
claims. A citation is evidence metadata, not proof that a statement is true.

`retrieved_at` is when the server read evidence. Source `as_of` is the time the
evidence represents. Top-level `as_of` defaults to the oldest contributing
source unless the query used a documented consistency snapshot.

Create one `source_statuses` item per planned source. A required timeout,
authorization-safe omission, malformed payload, or stale result beyond policy
makes the result partial. State the omitted coverage without leaking source or
record names the principal cannot see.

Record unresolved contradictions in `conflicts`. Do not silently choose a
winner based on model preference. Deterministic resolution rules may choose a
source only when those rules are documented and the answer still preserves the
evidence necessary to audit the choice.
