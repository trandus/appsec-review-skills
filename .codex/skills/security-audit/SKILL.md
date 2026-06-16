---
name: security-audit
description: Application audit for OWASP vulnerabilities
disable-model-invocation: true
---

# security-audit

Run a local security code review focused on finding the maximum number of real, exploitable vulnerabilities. Check every applicable OWASP category against the repository surface. Spend thinking budget on attack-path hunting, cross-file correlation, and defensible evidence, then write the shortest report that remains useful for triage and fixing.

If there is a choice between polishing wording and checking another realistic attack path, check the next attack path.

This skill is intentionally self-contained. Do not load additional skill reference files for its normal workflow. Do not add ASVS, compliance, certification, or standards-mapping work unless the user separately asks for it.

## Defaults

- Report language: Polish, unless the user explicitly provides `Report Language: <language>`.
- Output file: `./security-audits/security-audit-<YYYY-MM-DD-HHmm>.md` in the reviewed repository root, unless the user provides another path.
- Normal mode: offline, local repository only, no internet, no GitHub, no SaaS, no runtime access, no external scanners, and no fixes unless the user separately asks.

After writing the report, answer in chat only with the report path and result counts, for example:

`security-audit-2026-05-20-1430.md — Findings: 3 (2 confirmed, 1 needs-verification), Dismissed: 4`

## Internal Recon (do not include in report)

Start with a short internal repository profile. Use it to direct hunting across all categories below. Do not output the profile in the report; use it only to fill a brief `Repository Context` section.

Identify:

- application type and main technologies;
- entry points such as HTTP routes, RPC handlers, message consumers, cron jobs, CLI commands, file watchers, webhooks, admin panels, API docs, and diagnostics;
- trust boundaries and all places where untrusted input enters the system;
- authentication, authorization, ownership, tenant, organization, role, approval, and workflow boundaries;
- public, anonymous, semi-public, invite, tokenized-link, share-link, and lookup flows, especially where they resolve private objects or relationships;
- sensitive data, secrets, tokens, credentials, financial or regulated data, and high-impact operations;
- persistence, caches, queues, object storage, files, search indexes, and generated artifacts;
- external integrations, outbound HTTP clients, webhooks, identity providers, brokers, cloud services, and service-to-service authentication;
- deployment, IaC, containers, reverse proxies, CI/CD, environment configuration, public exposure, and internal-only assumptions.

Respect local repository instructions such as `AGENTS.md`, `CLAUDE.md`, README files, and project docs. Treat ignored, generated, vendored, or build-output files cautiously unless they are deployment-relevant evidence. Ignore ALL files from `.gitignore` and in `secret_files` directories in k8s (`k8s/**/secret_files/**`).

## Hunting Checklist

Check at minimum the categories below against the repository surface. Investigate additional attack paths specific to this application's domain and technology stack. Skip categories that have no matching surface. Hunt exploit paths within each category: start where exploitability is highest, correlate across files and categories, and do not stop at the first finding in a category. The .NET examples below are primary triggers for tracing and correlation, not limits on review scope.

### A01 - Broken Access Control

IDOR/BOLA, missing `[Authorize]`, role/policy checks bypassed, tenant isolation failures, audit-log enumeration, file download/delete endpoints without ownership checks, impersonation/SwitchContext target validation, path traversal in file ops, mass assignment, public/anonymous/invite/share-link flows exposing private objects or relationships.

### A02 - Cryptographic Failures

Plaintext secrets in code/config/manifests, MD5/SHA1 for security purposes, hardcoded keys/IVs, ECB mode, custom crypto, weak random (`Random` for tokens), missing TLS validation, PBKDF2/bcrypt with low iteration counts, disabled certificate validation, internal integrations over HTTP, missing HTTPS enforcement, secrets in logs/diagnostics/build artifacts/CI scripts. Distinguish real secrets from placeholders, sample values, encrypted values, hashes, and non-secret IDs.

### A03 - Injection

SQL (string concat, `FromSqlRaw`, dynamic Dapper), command injection (`Process.Start` with user input), LDAP, XPath, XXE (`XmlReader` without `DtdProcessing.Prohibit`), NoSQL injection, header injection, log injection, expression injection, frontend XSS sinks.

### A04 - Insecure Design

Business logic flaws, TOCTOU races, negative number bypass, integer overflow, missing rate limits on sensitive ops, predictable identifiers, race conditions in critical sections, missing CSRF defenses for browser-auth flows (cookies/session/Windows auth), rights caching without invalidation on role changes (stale access window).

### A05 - Security Misconfiguration

Debug/dev mode in prod, permissive CORS (`*` with credentials), `UseDeveloperExceptionPage` in prod, missing security headers (incl. missing CSP / misconfigured HSTS), default credentials, verbose errors leaking stack traces or echoing user input, exposed `/swagger`, `/healthz`, `/metrics` without auth, prod allowlist containing `http://` origins, container/manifest misconfigs (running as root, privileged containers, overly broad RBAC, missing NetworkPolicy).

### A06 - Vulnerable Components

NuGet packages with known CVEs, outdated runtime, deprecated libraries (e.g., `Newtonsoft.Json` with `TypeNameHandling.All`), unmaintained dependencies, vulnerable container base images, `:latest` tags hiding unpatched versions.

### A07 - Auth Failures

Weak JWT validation (`ValidateIssuer=false`, `ValidateAudience=false`, no expiry check, `none` algorithm accepted), missing token rotation, session fixation, credential stuffing exposure, weak password policy, cookie/session misconfiguration, missing CSRF/XSRF integration for SPA+cookie auth, Windows auth negotiation/downgrade risks (NTLM vs Kerberos) in browser flows.

### A08 - Data Integrity Failures

Unsafe deserialization (`BinaryFormatter`, `Newtonsoft.Json` with `TypeNameHandling`, `XmlSerializer` with type confusion), unsigned updates, CI/CD without integrity checks.

### A09 - Logging & Monitoring

Sensitive data in logs (passwords, tokens, PII), missing audit trail for security events, log injection enabling forgery.

### A10 - SSRF

`HttpClient` calls with user-controlled URLs, missing URL allowlist, IMDS metadata access (169.254.169.254), DNS rebinding, response fed to parser (SSRF response chain).

### A11 - Other

Other vulnerabilities specific to this application's domain, business logic, or technology stack not covered above.

### .NET-Specific

- Reflection with user input (`Type.GetType(userInput)`)
- `Process.Start` argument concatenation
- `SqlConnection` without parameterization
- Unprotected `[HttpGet]` for state-changing operations
- `IFormFile` upload without size/type/path validation
- Missing antiforgery tokens on cookie-auth endpoints
- `JsonSerializerOptions` with overly permissive settings

## Tiny Always-Check Reminder

After completing the category hunt above, scan once for these high-yield patterns if not already covered. Do not report without concrete local evidence and a realistic abuse scenario.

- Auth/authz gaps: unauthenticated routes, missing ownership/tenant checks, anonymous flows resolving private objects.
- Dangerous sinks: SQL/command/template injection, path traversal, unsafe redirect, SSRF to internal targets.
- Secrets and debug surfaces: real credentials in code/config/logs/CI, exposed Swagger/metrics/admin without auth.
- Browser controls: XSS through raw HTML/Markdown, CSRF on cookie-auth flows, unsafe CORS.

## Rules

1. Reference real code. Every finding cites a file path and line/symbol. No "the application might..."
2. No generic advice. "Use HTTPS" or "validate input" without pointing to specific code is not a finding.
3. Don't assume controls exist. If a control (auth, validation, sanitization) is not visible in the repo, treat it as absent. If the finding depends on a control you cannot see, mark confidence as `needs-verification`.
4. Redact secrets. Report location and pattern (e.g., "32-char hex string assigned to `ApiKey`") — do not reproduce actual values.
5. Distinguish hypotheses from finding. If you cannot trace a concrete exploitability path, either downgrade confidence to `needs-verification` or dismiss with evidence.
6. Stay in scope. Don't report style issues, missing tests, or non-security code smells.
7. Validate every candidate. Every potential vulnerability must be traced to its conclusion — confirmed with evidence, marked needs-verification with stated gaps, or dismissed with evidence. Do not leave findings in an ambiguous state.

## Evidence Gate

Every potential vulnerability identified during hunting must be explicitly resolved as one of:

- **Finding (confirmed)** — vulnerability with local evidence and a realistic exploit path. Confidence is high enough to recommend a fix.
- **Finding (needs-verification)** — concrete local evidence of a likely vulnerability, but confirmation requires runtime behavior, production configuration, or external context not available in the repository. State what is missing.
- **Dismissed** — investigated as a potential finding, but proven false positive through local evidence. Requires two-part justification: (1) why it was flagged, (2) why it was rejected.

Do not report generic best practices, style issues, missing tests alone, or scanner/tool output alone. Promote tool output only when local evidence confirms reachability, version, configuration, dependency use, or exploitability.

Do not assume cloud, gateway, CDN, WAF, identity-provider, SaaS, framework, SDK, CLI, or production configuration behavior unless proven by local repository evidence or user-provided context.

For secrets, redact values. Report only location, type, pattern, and evidence of use or deployment relevance. Do not automatically downgrade realistic secrets just because offline validity cannot be checked.

## Severity

- `critical`: unauthenticated RCE, full system compromise, mass data breach, broad tenant escape, or equivalent business-critical compromise.
- `high`: auth bypass, serious privilege escalation, arbitrary file read/write, SSRF to sensitive internal/cloud targets, exploitable injection with sensitive data access or command execution, serious secret exposure, or cross-tenant access.
- `medium`: constrained exploitability, limited sensitive data exposure, authenticated abuse with meaningful impact, or misconfiguration with realistic but bounded risk.
- `low`: plausible but limited impact, unusual preconditions, or defense-in-depth weakness with a credible abuse scenario.

Severity comes from impact, exploitability, and application context, not from category number. Correlate small weaknesses before deciding final severity.

## Exploitability

- `trivial`: no authentication required, publicly reachable, standard tools
- `requires-auth`: attacker needs valid credentials or session
- `requires-specific-conditions`: specific configuration, timing, or multi-step chain needed
- `theoretical`: plausible but no concrete path demonstrated

## Explicit Exclusions (do not report)

- `Encrypt=False` in DB connection strings
- Missing auth on healthcheck endpoints

## Report Shape

Write reports in this order:

1. **Repository Context** — brief, 3–5 lines from recon.

2. **Summary** — first line with totals, then severity breakdown table:

`Findings: N (M confirmed, K needs-verification) · Dismissed: D`

| Severity | Findings | Confirmed |
|-----------|-----------|-----------|
| Critical | 0 | 0 |
| High | 0 | 0 |
| Medium | 0 | 0 |
| Low | 0 | 0 |

3. **Findings** — detailed entries, confirmed first, then needs-verification.

4. **Dismissed** — brief entries with two-part justification.

### Finding format

Each **Finding** must include:

- `ID` (sequential, e.g. F-01)
- `Title`
- `Severity`: critical | high | medium | low
- `Exploitability`: trivial | requires-auth | requires-specific-conditions | theoretical
- `Confidence`: confirmed | needs-verification (if needs-verification, state what is missing)
- `Category`: OWASP category (A01-A11, .NET)
- `Location`: file, line, symbol, route, or configuration key
- `Evidence`
- `Exploit/Risk Path` (required for high/critical): numbered steps showing how an attacker triggers this
- `Impact`
- `Mitigating Factors` (if any)

### Dismissed format

Each **Dismissed** entry must include:

- `ID` (sequential, e.g. D-01)
- `Title`
- `Category`: OWASP category
- `Location`: file, line
- `Why flagged`: what made it look like a finding (1–2 sentences)
- `Why dismissed`: evidence that disproves the finding (1–3 sentences)

Expand mainly for `critical`, `high`, access control, tenant escape, injection/RCE, SSRF, and serious secret exposure. Keep `medium`, `low`, and `Dismissed` entries brief. Consolidate repeated instances of the same vulnerability class into one result with representative examples.

## Do not

- Include Non-Findings Sections like `Checked Areas Without Findings`