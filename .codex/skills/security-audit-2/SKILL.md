---
name: security-audit-2
description: Standalone exploit-path-first local AppSec review skill for repositories. Use when Codex should hunt for the maximum number of realistic, exploitable vulnerabilities in local code and write a concise Polish report with Findings, Candidate Findings, Observations, and Follow-up.
---

# security-audit-2

Run a local security code review focused on finding real, exploitable vulnerabilities. Optimize for hunting, correlation, and defensible exploit paths first; use reporting only to preserve the result clearly enough for triage and remediation.

If there is a choice between polishing wording and checking another realistic attack path, check the next attack path.

## Defaults

- `Review Depth`: `standard`.
- `ASVS Level`: `L2`.
- Report language: Polish, unless the user explicitly provides `Report Language: <language>`.
- Output file: `./security-audit-2-<YYYY-MM-DD-HHmm>.md` in the reviewed repository root, unless the user provides another path.
- Normal mode: offline, local repository only, no internet, no GitHub, no SaaS, no runtime access, no external scanners, and no fixes unless the user separately asks.

After writing the report, answer in chat only with the report path and result counts, for example:

`security-audit-2-2026-05-20-1430.md - Findings: 2, Candidate Findings: 3, Observations: 1, Follow-up: 4`

## Internal Recon

Start with a short internal repository profile. Use it to choose relevant review paths and to fill a brief `Repository Context`; do not spend report budget on architecture documentation.

Identify:

- application type and main technologies;
- entry points such as HTTP routes, RPC handlers, message consumers, cron jobs, CLI commands, file watchers, webhooks, admin panels, and generated docs;
- trust boundaries and all places where untrusted input enters the system;
- authentication, authorization, ownership, tenant, organization, and role boundaries;
- public, anonymous, semi-public, invite, tokenized-link, share-link, and lookup flows, especially where they resolve private objects or relationships;
- sensitive data, secrets, tokens, credentials, financial or regulated data, and high-impact operations;
- persistence, caches, queues, object storage, files, and search indexes;
- external integrations, outbound HTTP clients, webhooks, identity providers, brokers, cloud services, and service-to-service authentication;
- deployment, IaC, containers, reverse proxies, CI/CD, environment configuration, and public/internal exposure hints.

Respect local repository instructions such as `AGENTS.md`, `CLAUDE.md`, README files, and project docs. Treat ignored, generated, vendored, or build-output files cautiously unless they are deployment-relevant evidence.

## Hunting Order

Use `references/risk-baseline.md` as the priority model and `references/always-check.md` only as a tiny reminder of obvious high-yield checks. These files are triggers for tracing and correlation, not compliance checklists.

Hunt exploit paths in this order unless the repository context clearly suggests a better route:

1. Access control, tenant or owner checks, workflow authorization, forced browsing, frontend-only controls, state transitions, approvals, quotas, replay, duplicate submission, and business-logic abuse.
2. Authentication, session, token, invite/reset/magic-link, privilege-change, stale-access, cached-authorization, and identity-provider flows.
3. Injection and unsafe sinks: SQL/NoSQL/LDAP, command/process, template/expression, unsafe deserialization, XXE, unsafe redirects, header/log injection, XSS, and parser boundary issues.
4. SSRF, unsafe outbound calls, webhooks, callbacks, imports, URL fetchers, redirect behavior, DNS/IP filtering, and internal or metadata targets.
5. Unsafe file operations: upload, download, export, import, archive extraction, path construction, public storage, object ACLs, and ownership checks.
6. Secrets, credentials, connection strings, private keys, certificates, signing keys, tokens, production-like samples, logs, diagnostics, CI, scripts, and deployment files.
7. Public debug, admin, API docs, health, metrics, diagnostics, verbose errors, development modes, and internal surfaces.
8. Browser controls: CSRF, CORS, cookie flags, cache headers, CSP, HSTS, SameSite, state-changing GET, and unsafe rendering.
9. Dependency and supply-chain risks when local evidence or available lockfiles make the risk concrete.
10. Crypto, randomness, signing, transport, logging, monitoring, auditability, privacy lifecycle, deployment, IaC, containers, reverse proxy, cache, and distributed-state risks.

Use OWASP Web/API Top 10 categories and the older `security-audit` category set only as practical reminders. Do not march through them mechanically, and do not report categories that do not match the application surface.

## Evidence Gate

Report a `Finding` only when local code, configuration, IaC/deployment, routing/exposure evidence, tests, or a traced absence of a required control supports a realistic abuse path.

Use:

- `Finding` for a confirmed vulnerability or material security risk with local evidence and a realistic exploit or risk path.
- `Candidate Finding` for a likely vulnerability with concrete local evidence and plausible abuse, but missing confirmation such as runtime behavior, production configuration, reachability, dependency usage, exploitability in the deployed context, active secret validity, cloud/gateway behavior, or scanner data.
- `Observation` for a short hardening/posture signal, partial evidence, weakened control, or suspicious pattern that does not meet the finding threshold.
- `Follow-up` for a validation task that cannot be resolved from the repository.

Do not report generic best practices, style issues, missing tests alone, or scanner/tool output alone. Promote tool output only when local evidence confirms reachability, version, configuration, dependency use, or exploitability.

For secrets, redact values. Report only location, type, pattern, and evidence of use or deployment relevance. Distinguish real secrets from public identifiers, placeholders, sample values, encrypted values, encoded values, hashes, and non-secret IDs. Do not automatically downgrade realistic secrets just because offline validity cannot be checked.

## ASVS Mapping

Use ASVS only after a concrete result exists. It is a mapping aid, not a checklist and not a coverage or certification claim.

- Local dataset: `references/asvs-5.0.0-local.json`.
- Source notes: `references/asvs-source.md`.
- Helper: `scripts/asvs_lookup.py`.
- Default mapping level: `L2`, unless the user provides another `ASVS Level`.

Add `ASVS Mapping` to confirmed `Findings` when a quick useful match is possible. For `Candidate Findings`, mapping is optional and must not delay hunting. Do not map `Observations` or `Follow-up` by default. If no suitable match appears quickly, write a short rationale rather than forcing a weak mapping.

Example helper commands:

```powershell
python .codex/skills/security-audit-2/scripts/asvs_lookup.py --level L2 --query authorization
python .codex/skills/security-audit-2/scripts/asvs_lookup.py --level L2 --query injection
python .codex/skills/security-audit-2/scripts/asvs_lookup.py --level L2 --query "internal http-based services"
```

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
- `ASVS Mapping`

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

Severity comes from impact, exploitability, and application context, not from ASVS level, OWASP category, or risk-baseline tier.
