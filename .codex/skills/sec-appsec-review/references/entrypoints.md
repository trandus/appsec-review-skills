# Entry Points

## Review Checks

- Public and internal routes, controllers, minimal APIs, Razor Pages, GraphQL, webhooks, uploads, callbacks, serverless functions, queues, jobs, and CLI/admin commands.
- Middleware, filters, endpoint metadata, route groups, and framework conventions expected to enforce authentication, authorization, CSRF, CORS, rate limiting, validation, or response headers.
- Frontend routes and client actions that initiate server-side operations.
- Inputs from path parameters, query strings, bodies, files, headers, cookies, bearer tokens, claims, and external callbacks.
- Error, redirect, download, export, import, and health/diagnostic endpoints.

## Evidence Signals

- Route maps, endpoint registrations, annotations, attributes, filters, middleware order, generated OpenAPI files, frontend route tables, and form actions.
- Handler code showing the first server-side authorization, validation, state change, or sensitive data access.
- Tests covering unauthenticated, unauthorized, malformed, replayed, and cross-owner requests.
- Configuration that changes endpoint exposure by environment.

## Common Findings

- Public endpoint misses server-side authentication or authorization.
- Endpoint assumes middleware, route group, or frontend guard applies but local code shows a gap.
- Callback, webhook, upload, export, diagnostic, or admin path lacks validation, CSRF protection, or abuse controls.
- Sensitive data or stack/configuration details exposed through errors or diagnostic endpoints.

## Offline Boundaries

- Do not infer cloud gateway, CDN, WAF, identity-provider, or reverse-proxy protections without local IaC/configuration evidence.
- If a framework's current routing, binding, or middleware behavior decides the risk and local references are insufficient, record a `Follow-up` for official documentation.
- Without running the app, treat generated route completeness and environment-only exposure as limited unless route maps or build artifacts are present.
- A finding requires a concrete entry point and a traced missing control or vulnerable sink.

## Sources

See repository-root `SEC-README.md` for source links.
