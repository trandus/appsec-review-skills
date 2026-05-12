# Destructive Operations

## Review Checks

- Delete, revoke, disable, refund, payout, transfer, publish/unpublish, data export/import, account deletion, and permission changes.
- Server-side authentication and authorization enforcement.
- Ownership boundaries, tenant isolation, role transitions, and target-resource checks.
- Confirmation, idempotency, CSRF/antiforgery where applicable, audit logging, negative tests, and replay handling.
- Whether the operation removes, changes, or preserves all dependent data required by the product behavior.
- Recovery, rollback, or irreversible-operation warnings where the repo owns the UX or API contract.

## Evidence Signals

- Route/action, command handler, service, repository, stored procedure, blob operation, queue message, or external integration call for the operation.
- Cleanup code for dependent SQL rows, blobs, caches, indexes, scheduled jobs, and local integration records.
- Tests for wrong user, wrong role, cross-tenant target, repeated request, CSRF, partial failure, and dependent-data cleanup.
- Audit events and logs that record who did what to which resource without leaking sensitive data.

## Common Findings

- Destructive operation lacks server-side object-level authorization or tenant isolation.
- CSRF/antiforgery is missing for cookie-authenticated state-changing browser flows.
- Account/data deletion misses local user-owned tables, blobs, or other storage locations.
- Operation is not idempotent and repeated requests cause duplicate payout, refund, transfer, or inconsistent state.
- Audit trail is missing for high-impact changes.

## Offline Boundaries

- Do not rely on frontend confirmation, cloud retention, queue semantics, payment/provider behavior, or external cleanup without local code/config evidence.
- If current framework, SDK, cloud, payment, storage, or CLI behavior determines the control, record a `Follow-up`.
- Without runtime transaction traces, confirm only what local code guarantees across failure paths.
- Missing cleanup in external systems is `Follow-up` unless this repo owns the integration contract and local code proves the gap.

## Sources

See repository-root `SEC-README.md` for source links.
