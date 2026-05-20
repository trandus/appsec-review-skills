# Risk Baseline

Use this as a compact tiered priority model and risk prompt set, not a checklist catalog. Start where exploitability and expected yield are highest, then spend review budget only on tiers that match `Review Depth` and the real repository surface.

The examples below are not exhaustive. Treat them as triggers for tracing and correlation, not as required preconditions for a report and not as limits on review scope. Also look for other realistic vulnerabilities that follow from the audited technology, architecture, trust boundaries, and user-defined scope.

## Tier 1

Start here. These are usually the most exploitable and most cost-effective paths to trace in a local review.

- Access control and authorization boundaries: missing auth/authz, IDOR/BOLA, tenant escape, wrong-role access, forced browsing, frontend-only controls. Correlate route exposure, middleware, policy checks, object lookup filters, caller-controlled identifiers, public slugs, invite codes, tokenized links, and anonymous lookup flows that resolve private objects or relationships.
- Business workflow authorization: owner, tenant, role, approval, quota, state transition, and server-side context checks around operations that change state or grant access. Correlate the workflow state machine, trusted server-side state, replay/duplicate handling, side effects, and whether public or anonymous steps expose only the intended public view of recipients, destinations, profiles, payout/payment targets, integration settings, or workflow configuration.
- Auth, session, token, and identity flows: JWT/OAuth/OIDC validation, cookies, reset/invite/magic-link flows, privilege changes, stale access, cached authorization decisions. Correlate issuer/audience/lifetime checks, key selection, session invalidation, privilege transitions, and recovery or invitation paths.
- Injection and unsafe sinks: SQL/NoSQL/LDAP, command/process, template/expression, unsafe deserialization, XXE, redirects, header/log injection. Correlate input sources, validation/encoding layers, query builders or shell wrappers, parser settings, and reachable sinks.
- XSS and unsafe rendering: DOM sinks, templates, raw HTML, Markdown/rich text, context mistakes, sanitizer bypass APIs.
- SSRF and unsafe outbound calls: user-controlled URLs, hosts, webhooks, callbacks, imports, or upstream responses reaching HTTP clients or trusted parsers. Correlate allowlists, redirect behavior, DNS/IP filtering, metadata/internal targets, and response-to-parser flows.
- Unsafe file operations: upload/download/export/import/archive extraction, path traversal, public storage, missing object authorization. Correlate filename/path construction, archive extraction, storage ACLs, content-type trust, and object ownership checks.
- Secrets and credentials: credentials, keys, tokens, connection strings, certificates, webhook/signing secrets in code, config, IaC, CI, scripts, docs, samples, logs, diagnostics, or build artifacts.
- Exposed API docs, diagnostics, and internal surfaces: API docs/playgrounds, health, metrics, debug, diagnostics, admin/dev/internal endpoints.

## Tier 2

Continue here for standard review coverage and representative deeper traces.

- Destructive or high-impact operations: delete, revoke, refund, payout, transfer, publish, permission changes, replay, duplicate submission, race, TOCTOU, missing idempotency, weak audit. Correlate command handlers, transaction boundaries, queues/jobs, external callbacks, and audit records.
- Client-trust and workflow bypass: server trusting client-supplied price, role, owner, tenant, status, limits, approvals, or next-step values instead of trusted state. Correlate request DTOs, hidden fields, frontend-derived values, server recalculation, and persistence updates.
- Sensitive data exposure: responses, logs, telemetry, errors, exports, caches, bundles, files, broad roles, deletion gaps, and business-private metadata such as recipients, destinations, payout/payment targets, contact channels, integration configuration, preferences, or relationship mappings exposed outside their intended authorization context.
- Browser-auth controls: CSRF, CORS, SameSite/Secure/HttpOnly, cache headers, state-changing GETs.
- Dependency and supply-chain risk: lockfiles, broad versions, package sources, dependency confusion, package scripts, containers, CI actions, vulnerable components confirmed by local/tool evidence.
- Abuse and resource consumption: enumeration, spam, brute force, expensive operations, integration fan-out, account/token workflows, queue/event amplification.
- Crypto, key handling, randomness, signing, and transport boundaries: custom crypto, weak randomness, hardcoded keys/IVs, weak hashes, disabled TLS/certificate validation, HTTPS-to-HTTP fallback, signing/encryption boundary mistakes. For service credentials and transport risk, correlate production-like `http://` values in keys such as `EndpointUrl`, `BaseUrl`, `ApiUrl`, or `ServiceUrl` with HTTP clients and auth methods such as credentials, tokens, cookies, or NTLM/`DefaultCredentials`.

## Tier 3

Use this tier when `Review Depth` is `deep`, when the architecture has a matching surface, or when earlier tiers point to a higher-level trust-boundary issue.

- Reverse proxy, cache, and header trust: request smuggling, cache poisoning, host/header confusion, forwarded header trust, origin/proxy mismatch.
- Parser and format boundary issues: parser differentials, unusual deserialization/parser behavior, unsafe archive/media/document parsing, mixed content-type assumptions.
- Service and deployment trust boundaries: multi-service assumptions, internal-only controls, service calls, queue/event integrity, deployment/IaC-only assumptions, unsafe network exposure. Correlate service-to-service identity, transport protection, network reachability, broker permissions, and config that marks internal paths as implicitly trusted.
- Isolation and execution boundaries: sandbox escapes, unsafe native/process isolation, plugin/script execution, worker/job isolation mistakes, stale auth in background work.
- Advanced or uncommon crypto misuse: protocol misuse, signing scope confusion, exploitable key-rotation gaps, cross-service token trust mistakes.
- Privacy and lifecycle risks that need broad context: retention/deletion gaps, overbroad exports, audit trails that fail for material abuse paths.
- Distributed state and consistency risks: eventual-consistency abuse, stale authorization caches, duplicate event delivery, replay, missing outbox/inbox integrity, non-atomic cross-service changes.

## Review Depth Guidance

- `quick`: mostly `Tier 1`, with very small sampling of obvious `Tier 2` issues when the surface is directly visible.
- `standard`: all relevant `Tier 1`, representative `Tier 2`, and selected `Tier 3` areas that clearly match the repository.
- `deep`: broader variants across `Tier 1` and `Tier 2`, plus stronger `Tier 3` coverage and cross-layer checks.

## Finding Threshold

Use the evidence gate and result types from `sec-appsec-review` and `sec-reporting`. This baseline only helps decide review order; it does not lower the proof threshold for a `Finding`.
