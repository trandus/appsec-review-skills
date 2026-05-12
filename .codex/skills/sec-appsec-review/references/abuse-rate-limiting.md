# Abuse cases/rate limiting

## Review Checks

- Expensive, repeatable, public, message-sending, resource-creating, upload, search, export, and integration-triggering endpoints.
- Limits per user, IP, tenant, resource, action, identity-provider subject, payment account, or time window.
- Brute force, enumeration, spam, scraping, workflow replay, duplicate submission, and costly fan-out paths.
- Whether business validation still holds under concurrent requests, retries, idempotency keys, and queued work.
- User-visible throttling, lockout, backoff, quotas, and audit/logging of abuse signals.

## Evidence Signals

- Rate-limit middleware/config, app-level quotas, uniqueness constraints, idempotency stores, concurrency checks, and queue deduplication.
- Public routes that create records, send notifications, perform search, upload files, export data, or trigger external calls.
- Tests for repeated requests, parallel requests, replay, enumeration, brute force, and quota exhaustion.
- Logs or audit events that identify abuse attempts without leaking sensitive data.

## Common Findings

- Public or authenticated endpoint can be repeated to spam, enumerate, create cost, or overwhelm a resource without controls.
- Rate limit exists only at a proxy or platform layer with no local evidence and no app-level fallback for business-specific limits.
- Missing idempotency or uniqueness allows duplicate high-impact operations.
- Error responses or timing reveal account, token, resource, or tenant existence.

## Offline Boundaries

- Do not assume WAF, CDN, gateway, identity-provider lockout, or cloud rate limiting without local config/IaC evidence.
- If current platform or SDK rate-limiting behavior is needed to decide, record a `Follow-up`.
- Without load testing or runtime metrics, keep capacity claims as `Observation` or `Follow-up`.
- A finding requires the abused operation and the missing or ineffective server-side control in the traced path.

## Sources

See repository-root `SEC-README.md` for source links.
