---
name: security-audit-3
description: Single-file exploit-path-first local AppSec review skill for repositories. Use when Codex should maximize discovery of realistic, exploitable vulnerabilities in local code and write a concise Polish report without ASVS, standards mapping, scripts, or extra reference files.
---

# security-audit-3

Run a local security code review focused on finding the maximum number of real, exploitable vulnerabilities. Effectiveness comes first: spend thinking budget on attack-path hunting, cross-file correlation, and defensible evidence, then write the shortest report that remains useful for triage and fixing.

If there is a choice between polishing wording and checking another realistic attack path, check the next attack path.

This skill is intentionally self-contained. Do not load additional skill reference files for its normal workflow. Do not add ASVS, compliance, certification, or standards-mapping work unless the user separately asks for it.

## Defaults

- `Review Depth`: `standard`.
- Report language: Polish, unless the user explicitly provides `Report Language: <language>`.
- Output file: `./security-audit-3-<YYYY-MM-DD-HHmm>.md` in the reviewed repository root, unless the user provides another path.
- Normal mode: offline, local repository only, no internet, no GitHub, no SaaS, no runtime access, no external scanners, and no fixes unless the user separately asks.

After writing the report, answer in chat only with the report path and result counts, for example:

`security-audit-3-2026-05-20-1430.md - Findings: 2, Candidate Findings: 3, Observations: 1, Follow-up: 4`

## Internal Recon

Start with a short internal repository profile. Use it to choose relevant attack paths and to fill a brief `Repository Context`; do not spend report budget on architecture documentation.

Identify:

- application type and main technologies;
- entry points such as HTTP routes, RPC handlers, message consumers, cron jobs, CLI commands, file watchers, webhooks, admin panels, API docs, and diagnostics;
- trust boundaries and all places where untrusted input enters the system;
- authentication, authorization, ownership, tenant, organization, role, approval, and workflow boundaries;
- sensitive data, secrets, tokens, credentials, financial or regulated data, and high-impact operations;
- persistence, caches, queues, object storage, files, search indexes, and generated artifacts;
- external integrations, outbound HTTP clients, webhooks, identity providers, brokers, cloud services, and service-to-service authentication;
- deployment, IaC, containers, reverse proxies, CI/CD, environment configuration, public exposure, and internal-only assumptions.

Respect local repository instructions such as `AGENTS.md`, `CLAUDE.md`, README files, and project docs. Treat ignored, generated, vendored, or build-output files cautiously unless they are deployment-relevant evidence.

## Hunting Strategy

Hunt exploit paths before categories. Start where exploitability and expected yield are highest, then spend remaining review budget only on areas that match `Review Depth`, the repository surface, and user scope.

The examples below are triggers for tracing and correlation, not a checklist catalog and not limits on review scope. Also look for other realistic vulnerabilities that follow from the audited technology, architecture, trust boundaries, and business workflows.

### Tier 1: Start Here

Prioritize these paths first:

- Access control and authorization boundaries: missing auth/authz, IDOR/BOLA, tenant escape, wrong-role access, forced browsing, frontend-only controls. Correlate route exposure, middleware, policy checks, object lookup filters, and caller-controlled identifiers.
- Business workflow authorization: owner, tenant, role, approval, quota, state transition, and server-side context checks around operations that change state or grant access. Correlate state machines, trusted server-side state, replay/duplicate handling, and side effects.
- Auth, session, token, and identity flows: JWT/OAuth/OIDC validation, cookies, reset/invite/magic-link flows, privilege changes, stale access, cached authorization decisions. Correlate issuer/audience/lifetime checks, key selection, session invalidation, privilege transitions, and recovery or invitation paths.
- Injection and unsafe sinks: SQL/NoSQL/LDAP, command/process, template/expression, unsafe deserialization, XXE, redirects, header/log injection. Correlate input sources, validation/encoding layers, query builders or shell wrappers, parser settings, and reachable sinks.
- XSS and unsafe rendering: DOM sinks, templates, raw HTML, Markdown/rich text, context mistakes, sanitizer bypass APIs.
- SSRF and unsafe outbound calls: user-controlled URLs, hosts, webhooks, callbacks, imports, or upstream responses reaching HTTP clients or trusted parsers. Correlate allowlists, redirect behavior, DNS/IP filtering, metadata/internal targets, and response-to-parser flows.
- Unsafe file operations: upload/download/export/import/archive extraction, path traversal, public storage, missing object authorization. Correlate filename/path construction, archive extraction, storage ACLs, content-type trust, and object ownership checks.
- Secrets and credentials: credentials, keys, tokens, connection strings, certificates, webhook/signing secrets in code, config, IaC, CI, scripts, docs, samples, logs, diagnostics, or build artifacts.
- Exposed API docs, diagnostics, and internal surfaces: API docs/playgrounds, health, metrics, debug, diagnostics, admin/dev/internal endpoints.

### Tier 2: Continue For Standard Coverage

Use these after Tier 1 or when they are directly visible in scope:

- Destructive or high-impact operations: delete, revoke, refund, payout, transfer, publish, permission changes, replay, duplicate submission, race, TOCTOU, missing idempotency, weak audit. Correlate command handlers, transaction boundaries, queues/jobs, external callbacks, and audit records.
- Client-trust and workflow bypass: server trusting client-supplied price, role, owner, tenant, status, limits, approvals, or next-step values instead of trusted state. Correlate request DTOs, hidden fields, frontend-derived values, server recalculation, and persistence updates.
- Sensitive data exposure: responses, logs, telemetry, errors, exports, caches, bundles, files, broad roles, deletion gaps.
- Browser-auth controls: CSRF, CORS, SameSite/Secure/HttpOnly, cache headers, state-changing GETs.
- Dependency and supply-chain risk: lockfiles, broad versions, package sources, dependency confusion, package scripts, containers, CI actions, vulnerable components confirmed by local/tool evidence.
- Abuse and resource consumption: enumeration, spam, brute force, expensive operations, integration fan-out, account/token workflows, queue/event amplification.
- Crypto, key handling, randomness, signing, and transport boundaries: custom crypto, weak randomness, hardcoded keys/IVs, weak hashes, disabled TLS/certificate validation, HTTPS-to-HTTP fallback, signing/encryption boundary mistakes. For service credentials and transport risk, correlate production-like `http://` values in keys such as `EndpointUrl`, `BaseUrl`, `ApiUrl`, or `ServiceUrl` with HTTP clients and auth methods such as credentials, tokens, cookies, or NTLM/`DefaultCredentials`.

### Tier 3: Use When Surface Justifies It

Use this tier when `Review Depth` is `deep`, when the architecture has a matching surface, or when earlier tiers point to a higher-level trust-boundary issue:

- Reverse proxy, cache, and header trust: request smuggling, cache poisoning, host/header confusion, forwarded header trust, origin/proxy mismatch.
- Parser and format boundary issues: parser differentials, unusual deserialization/parser behavior, unsafe archive/media/document parsing, mixed content-type assumptions.
- Service and deployment trust boundaries: multi-service assumptions, internal-only controls, service calls, queue/event integrity, deployment/IaC-only assumptions, unsafe network exposure. Correlate service-to-service identity, transport protection, network reachability, broker permissions, and config that marks internal paths as implicitly trusted.
- Isolation and execution boundaries: sandbox escapes, unsafe native/process isolation, plugin/script execution, worker/job isolation mistakes, stale auth in background work.
- Advanced or uncommon crypto misuse: protocol misuse, signing scope confusion, exploitable key-rotation gaps, cross-service token trust mistakes.
- Privacy and lifecycle risks that need broad context: retention/deletion gaps, overbroad exports, audit trails that fail for material abuse paths.
- Distributed state and consistency risks: eventual-consistency abuse, stale authorization caches, duplicate event delivery, replay, missing outbox/inbox integrity, non-atomic cross-service changes.

## Tiny Always-Check Reminder

Use this only to avoid missing obvious high-yield issues while hunting deeper paths. Pick only areas that match the audited technology, scope, and exposed surface. Do not report anything from this reminder without a concrete local evidence path and realistic abuse scenario.

- Access control and workflows: missing auth on public routes, APIs, files, admin/debug panels; missing owner, tenant, organization, role, approval, state-transition checks; IDOR/BOLA.
- Unsafe input to sinks: SQL/NoSQL/LDAP/query, command, template/expression, path traversal, unsafe redirect; SSRF, unsafe file import/export/archive handling, attacker-controlled outbound URLs.
- Browser and rendering: reflected, stored, or DOM XSS through raw HTML, Markdown/rich text, or missing encoding/sanitization; CSRF, unsafe CORS, and weak sensitive-cookie flags on browser-auth flows.
- Secrets and sensitive data: credentials, API keys, tokens, connection strings, private keys, weak defaults, production-like sample values; secrets, PII, auth headers, request bodies, stack traces in logs/errors/responses; production-like `http://` endpoints used with credentials, tokens, cookies, sensitive data, or Windows/NTLM auth.
- Public debug surfaces: Swagger/OpenAPI/ReDoc exposed outside development; debug, diagnostics, health, metrics, logs, admin/dev endpoints without clear protection.

## Review Depth

- `quick`: mostly Tier 1, with very small sampling of obvious Tier 2 issues when the surface is directly visible.
- `standard`: relevant Tier 1, representative Tier 2, and selected Tier 3 areas that clearly match the repository.
- `deep`: broader variants across Tier 1 and Tier 2, plus stronger Tier 3 coverage and cross-layer checks.

Severity comes from impact, exploitability, and application context, not from tier number. A Tier 2 issue can be `critical`, and a Tier 1 signal can remain an `Observation` if local evidence does not support a realistic abuse path. Correlate small weaknesses before deciding final severity, especially around authorization, tenancy, async processing, stale state, replay, and idempotency.

Use OWASP Web/API Top 10 categories and the older `security-audit` category set only as practical reminders. Do not march through them mechanically, and do not report categories that do not match the application surface.

## Evidence Gate

Report a `Finding` only when local code, configuration, IaC/deployment, routing/exposure evidence, tests, or a traced absence of a required control supports a realistic abuse path.

Use:

- `Finding` for a confirmed vulnerability or material security risk with local evidence and a realistic exploit or risk path.
- `Candidate Finding` for a likely vulnerability with concrete local evidence and plausible abuse, but missing confirmation such as runtime behavior, production configuration, reachability, dependency usage, exploitability in the deployed context, active secret validity, cloud/gateway behavior, or scanner data.
- `Observation` for a short hardening/posture signal, partial evidence, weakened control, or suspicious pattern that does not meet the finding threshold.
- `Follow-up` for a validation task that cannot be resolved from the repository.

Do not report generic best practices, style issues, missing tests alone, or scanner/tool output alone. Promote tool output only when local evidence confirms reachability, version, configuration, dependency use, or exploitability.

Do not assume cloud, gateway, CDN, WAF, identity-provider, SaaS, framework, SDK, CLI, or production configuration behavior unless it is proven by local repository evidence or user-provided context.

For secrets, redact values. Report only location, type, pattern, and evidence of use or deployment relevance. Distinguish real secrets from public identifiers, placeholders, sample values, encrypted values, encoded values, hashes, and non-secret IDs. Do not automatically downgrade realistic secrets just because offline validity cannot be checked.

## Report Shape

Write reports in this order:

1. `Repository Context`
2. `Executive Summary`
3. `Summary`
4. `Final Findings Overview`
5. `Findings`
6. `Candidate Findings`
7. `Observations`
8. `Follow-up`

Keep `Repository Context`, `Executive Summary`, `Summary`, and `Final Findings Overview` short. The `Summary` count table must include `Findings`, `Candidate Findings`, `Observations`, and `Follow-up`, with `0` for empty sections. The overview table should use columns `Type | ID | Severity / Candidate Severity | Area | Decision`, where decisions are `fix`, `validate`, `observe`, or `follow-up`.

Each `Finding` must include at minimum:

- `Type`: `Finding`
- `Title`
- `Severity`: `critical`, `high`, `medium`, or `low`
- `Location`: file, line, symbol, route, or configuration key
- `Evidence`
- `Exploit/Risk Path`
- `Impact`
- `Remediation Requirement`
- `Regression Test`

Each `Candidate Finding` must include at minimum:

- `Type`: `Candidate Finding`
- `Title`
- `Candidate Severity`: `critical`, `high`, `medium`, or `low`
- `Confidence`: `high`, `medium`, or `low`
- `Location`
- `Evidence`
- `Missing Confirmation`
- `Potential Exploit/Risk Path`
- `Validation Test`

`Observations` and `Follow-up` must be short and must not pretend to be findings. State why an `Observation` is not a `Finding`. For each `Follow-up`, name the hypothesis or check that needs validation.

Expand mainly for `critical`, `high`, access control, tenant escape, injection/RCE, SSRF, serious secret exposure, async/distributed abuse, replay/idempotency, and non-obvious business logic. Keep `medium`, `low`, `Observation`, and `Follow-up` entries brief. Consolidate repeated instances of the same vulnerability class into one result with representative examples.

## Severity

- `critical`: unauthenticated RCE, full system compromise, mass data breach, broad tenant escape, or equivalent business-critical compromise.
- `high`: auth bypass, serious privilege escalation, arbitrary file read/write, SSRF to sensitive internal/cloud targets, exploitable injection with sensitive data access or command execution, serious secret exposure, or cross-tenant access.
- `medium`: constrained exploitability, limited sensitive data exposure, authenticated abuse with meaningful impact, or misconfiguration with realistic but bounded risk.
- `low`: plausible but limited impact, unusual preconditions, or defense-in-depth weakness with a credible abuse scenario.

