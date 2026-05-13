# Backend web

## Review Checks

- HTTP pipeline: middleware order, authentication, authorization, exception handling, HTTPS, security headers, CORS, antiforgery, response caching, and static files.
- Controllers/minimal APIs/Razor Pages: binding, validation, authorization, response caching, redirects, downloads, and uploads.
- Cookies: Secure, HttpOnly, SameSite, lifetime, scope, and environment-specific overrides.
- Data access: parameterized queries, ORM raw SQL, Dapper/ADO usage, transaction boundaries, and concurrency assumptions.
- Race/replay/TOCTOU and idempotency for delete, revoke, refund, payout, transfer, permission-change, export/import, publish/unpublish, and expensive operations.
- Crypto/data protection: avoid custom cryptography, use safe randomness, protect keys, and verify signing/encryption boundaries.
- Logging: keep PII, secrets, tokens, cookies, and payment data out of logs.
- Background work, health/diagnostic endpoints, and operational routes.

## Evidence Signals

- Startup/program pipeline, service registration, filters, endpoint attributes, and environment-specific branches.
- Cookie, CORS, antiforgery, HTTPS, HSTS, data-protection, cache, and exception-handler configuration.
- Controller/page/API handlers showing validation, authorization, query construction, redirects, file handling, and logging.
- Tests for unauthenticated, unauthorized, CSRF, replay, duplicate submission, invalid input, cache, and error behavior.
- Transaction, concurrency token, idempotency key, audit logging, and retry handling code for high-impact operations.

## Common Findings

- Middleware order or endpoint metadata leaves routes unauthenticated, unauthorized, or missing CSRF protection.
- CORS, cookies, redirects, cache headers, or exception handling are configured too permissively for sensitive flows.
- Raw SQL, shell/file operations, or URL fetches use untrusted input without safe APIs.
- High-impact operation can be replayed, raced, or partially applied because authorization, state checks, transaction boundaries, or idempotency are missing.
- Sensitive data is logged or returned in production error responses.

## Offline Boundaries

- Do not assume ASP.NET Core, reverse-proxy, hosting, browser, or cloud defaults beyond local configuration and current documentation.
- If the current behavior of a framework, SDK, CLI, cloud service, or hosting feature is required to decide, record a `Follow-up` to refresh references or check official docs.
- Without running the app, treat middleware execution and environment-specific branches as code-review evidence only.
- Deployment-only controls such as WAF, gateway auth, TLS policy, or platform headers need local IaC/config evidence before they can reduce a finding.

## Sources

See repository-root `SEC-README.md` for source links.
