# Risk Baseline

Use this as a compact tiered priority model, not a checklist catalog. The model should reason over the reviewed code, start where exploitability and expected yield are highest, and only spend review budget on tiers that match the selected `Review Depth` and real repository surface.

## Tier 1

Start here. These are usually the most exploitable and most cost-effective paths to trace in a local review.

- Access control and authorization boundaries: missing auth/authz, IDOR/BOLA, BOPLA, tenant escape, wrong-role access, forced browsing, frontend-only controls.
- Business workflow authorization: role, owner, tenant, approval, quota, state transition, and server-side context checks around operations that change state or grant access.
- Auth, session, token, and identity flows: JWT/OAuth/OIDC validation, cookies, sessions, password reset, invite/magic links, logout, privilege changes, stale access, cached authorization decisions.
- Injection and unsafe sinks: SQL/NoSQL/LDAP, command/process, template/expression, header/log injection, XXE, unsafe deserialization, unsafe redirects.
- XSS and unsafe rendering: frontend DOM sinks, backend templates, raw HTML, Markdown/rich text, JavaScript/CSS/URL contexts, sanitizer bypass APIs.
- SSRF and unsafe outbound calls: user-controlled URL/host/webhook/callback/file import/metadata/upstream response reaching HTTP clients or trusted parsers, including redirects, internal networks, and cloud metadata.
- Unsafe file operations: upload/download/export/import/archive extraction, path traversal, attacker-controlled names, public storage, missing object authorization.
- Secrets and credentials: credentials, connection strings, API keys, tokens, private keys, certificates, webhook secrets, signing keys in code/config/IaC/CI/scripts/docs/samples/logs/diagnostics, plus lifecycle gaps such as unsafe defaults, rotation, revocation, and build artifact leakage.
- Exposed API docs, diagnostics, and internal surfaces: Swagger, OpenAPI, ReDoc, GraphQL playground, health, metrics, debug, diagnostics, admin/dev/internal endpoints.

## Tier 2

Continue here for standard review coverage and representative deeper traces.

- Destructive or high-impact operations: delete, revoke, refund, payout, transfer, publish/unpublish, account deletion, permission changes, webhook replay, duplicate submission, race, TOCTOU, missing idempotency, weak audit.
- Client-trust and workflow bypass: server trusting client-supplied price, role, owner, tenant, status, limits, approvals, or next-step parameters instead of deriving them from trusted state.
- Sensitive data exposure: responses, logs, telemetry, errors, exports, caches, bundles, files, broad roles, deletion gaps.
- Browser-auth controls: CSRF, CORS, SameSite/Secure/HttpOnly, cache headers, state-changing GETs.
- Dependency and supply-chain risk: lockfiles, broad versions, package sources, dependency confusion, package scripts, containers, CI actions, vulnerable components confirmed by local/tool evidence.
- Abuse and resource consumption: enumeration, spam, brute force, expensive search/export/upload, duplicate submission, integration fan-out, account/token workflows, queue/event amplification.
- Crypto, key handling, randomness, and signing boundaries: custom crypto, weak randomness, hardcoded keys/IVs, weak hashes for security, disabled TLS/certificate validation, signing/encryption boundary mistakes.

## Tier 3

Use this tier when `Review Depth` is `deep`, when the architecture has a matching surface, or when earlier tiers point to a higher-level trust-boundary issue.

- Reverse proxy, cache, and header trust: request smuggling, cache poisoning, host/header confusion, forwarded header trust, origin/proxy mismatch.
- Parser and format boundary issues: parser differentials, unusual deserialization/parser behavior, unsafe archive/media/document parsing, mixed content-type assumptions.
- Service and deployment trust boundaries: multi-service trust assumptions, internal-only controls, service-to-service calls, queue/event integrity, actors/grains, deployment/IaC-only security assumptions, unsafe network exposure.
- Isolation and execution boundaries: sandbox escapes, unsafe native/process isolation, plugin/script execution, worker/job isolation mistakes, background processing with stale auth or partial failure.
- Advanced or uncommon crypto misuse: protocol misuse, signing scope confusion, key rotation gaps with direct exploitability, cross-service token trust mistakes.
- Privacy and lifecycle risks that need broad context: retention/deletion gaps, overbroad exports, audit trails that fail for material abuse paths.
- Distributed state and consistency risks: eventual-consistency abuse, stale authorization caches, duplicate event delivery, replayed messages, missing outbox/inbox integrity, and non-atomic cross-service state changes.

## Review Depth Guidance

- `quick`: mostly `Tier 1`, with very small sampling of obvious `Tier 2` issues when the surface is directly visible.
- `standard`: all relevant `Tier 1`, representative `Tier 2`, and selected `Tier 3` areas that clearly match the repository.
- `deep`: broader variants across `Tier 1` and `Tier 2`, plus stronger `Tier 3` coverage and cross-layer checks.

## Finding Threshold

Use the evidence gate and result types from `sec-appsec-review` and `sec-reporting`. This baseline only helps decide review order; it does not lower the proof threshold for a `Finding`.
