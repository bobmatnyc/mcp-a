# Safe action implementation

An operation is a versioned definition; an execution is one attempt to invoke
it. Publish immutable operation versions and input-schema IDs plus explicit risk, effect class, approval,
idempotency, reversibility, and compensation metadata through `mcpa.schema`.

Natural language may resolve an operation and normalize inputs, but it cannot
apply effects on the first turn. Return a preview, missing-input request, or
approval request. The client must present the resolved operation and planned
effects to the user rather than asking for approval of the original prose alone.

For effectful operations, bind idempotency to authorization context, operation,
and normalized inputs. A duplicate returns the existing execution; reuse with
different inputs returns `IDEMPOTENCY_CONFLICT`. Check preconditions and current
authorization immediately before each external effect.

Clients may pin `operation_version` on typed requests. Reject a stale version
with `CONFLICT` and no effects; do not silently run materially changed semantics.

Do not imply cross-system atomicity. Record effects independently:

- `preview` contains only `planned` effects;
- `completed` contains only `applied` or `compensated` effects;
- `partially_completed` contains at least one successful and one failed effect;
- `failed` means no effects were applied and therefore contains no effects.

Retries after partial completion require an operation-specific recovery plan.
They must not blindly repeat already applied effects. Compensation is itself an
effect and may fail; report that state rather than claiming rollback.
