# API baseline

## Review Checks

- Use this reference for web/API repositories after entry point recon. Treat OWASP API Security Top 10 as a risk lens, not as a replacement for ASVS mapping.
- For object-level authorization, trace every API operation that accepts or derives a resource identifier. Confirm the backend binds the object to the current user, tenant, organization, role, or explicit permission before read, write, export, import, delete, or bulk use.
- For object property authorization, check whether responses expose fields the caller should not see and whether request bodies allow mass assignment of owner, role, tenant, status, price, approval, or internal fields.
- For function-level authorization, verify that privileged API routes, methods, background-triggering endpoints, admin operations, and alternate HTTP methods enforce server-side policy checks.
- For resource consumption and sensitive business flows, look for expensive search, export, upload, notification, account creation, booking, checkout, invite, token, and integration-triggering paths. Check quotas, rate limits, idempotency, uniqueness, concurrency, and abuse logging where the repo owns them.
- For SSRF and unsafe API consumption, trace URL, host, webhook, callback, file import, metadata, and third-party API inputs before outbound calls. Check allowlists, protocol and host restrictions, timeout, redirect handling, response validation, authentication, and error handling.
- For API inventory and configuration, compare routed endpoints, versioned APIs, docs/OpenAPI files, generated clients, feature flags, CORS, auth schemes, debug routes, and deployment/IaC. Look for undocumented, stale, unauthenticated, deprecated, or environment-only endpoints.

## Evidence Signals

- Routes/controllers/minimal APIs/serverless functions, OpenAPI files, generated clients, endpoint tests, middleware, policies, handlers, services, repositories, DTOs, validators, serializers, and mappers.
- Queries constrained by current identity or tenant; field allowlists; separate read/write DTOs; explicit authorization policies; tests for wrong-user, wrong-role, cross-tenant, hidden-field, bulk, and replay variants.
- Rate-limit and quota configuration, idempotency stores, uniqueness constraints, queue deduplication, outbound HTTP clients, webhook validation, allowlists, timeout/retry settings, and response schema validation.
- Local API documentation, route maps, gateway/proxy/IaC config, versioning conventions, auth scheme registration, CORS policies, and environment-specific branches.

## Common Findings

- BOLA/IDOR: changing an object ID reads, changes, exports, deletes, or links another user's or tenant's resource.
- BOPLA: API response returns sensitive/internal fields, or request body can set fields such as role, tenant, owner, price, approval state, or security flags.
- Missing function-level authorization on admin, destructive, integration-triggering, or alternate-method API operations.
- Repeatable or expensive API flow lacks app-owned limits, idempotency, uniqueness, or abuse controls where local code shows the repo owns the control.
- User-controlled URL, host, webhook, callback, or upstream API response reaches an outbound request or trusted parser without sufficient local restrictions.
- API docs, generated clients, route registrations, or gateway config reveal stale, shadow, unauthenticated, or misconfigured API surface.

## Offline Boundaries

- Report a `Finding` only when local code, configuration, tests, manifests, OpenAPI files, generated clients, IaC, or a traced missing control supports it.
- Use `Observation` for partial evidence, such as a suspicious DTO, route, or config that needs runtime behavior, deployment configuration, or product-owner confirmation.
- Use `Follow-up` when deciding the issue requires framework, gateway, cloud, SaaS, identity-provider, scanner, or production configuration behavior that is not present locally.
- Do not assume gateway auth, WAF, CDN throttling, cloud defaults, third-party API guarantees, or unpublished API inventory unless local code, configuration, or bundled references support it. If support is missing, record a separate reference-refresh or environment-validation `Follow-up`.

## Sources

See repository-root `SEC-README.md` for source links.
