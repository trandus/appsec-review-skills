---
name: sec-appsec-review
description: Offline-first AppSec code review orchestrator. Use when the user asks for a repository security review, a focused review of one security area, a compact end-to-end AppSec flow, ASVS mapping, or a report with Remediation and Regression Test entries without implementing fixes.
---

# sec-appsec-review

Run the review as local security code review, not as runtime penetration testing. Do not require internet access, GitHub, SaaS products, Context7, or external scanners during normal review work. Use the local repository, host-repository instructions, the repository-root `SEC-README.md` when present, the `sec-*` skills, the files under `references/`, and the ASVS dataset from `sec-asvs-review`.

## Tool-Assisted Inputs

Keep the default review offline-first. Do not run dependency, SAST, or security tools unless the user explicitly asks for them or accepts their use for the current review. Optional local tools may include `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, Semgrep, and CodeQL.

Treat tool output as review input, not as an automatic `Finding`. Before promoting a tool result, connect it to local evidence such as code, a manifest, a lockfile, configuration, package source settings, or real dependency usage. If a result is not confirmed, not reachable, stale, lacks commit/dependency graph context, or depends on unavailable network access, login, databases, or configuration, report it as an `Observation` or `Follow-up` with the limitation.

## Review Modes

- **Focused area review**: use when the user names one area, such as auth/authz, input/data, frontend, config/secrets, or dependencies. Keep recon, reference loading, and reporting within that scope while preserving the evidence standard.
- **Compact full flow**: use when the user asks for local AppSec review of the repository. Move through recon, threat model, entry points, auth/authz, input/data, backend, frontend, config/secrets, dependencies, sensitive data, logging, abuse/rate limiting, and destructive operations.

## High-Priority Baseline Checks

When the user asks for broad web/API review, prioritize exploitable paths in this order:

- **Tier 1**: access control, object-level authorization, function-level authorization, auth/session lifecycle, injection, XSS/template injection, and unsafe file operations.
- **Tier 2**: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/configuration, and sensitive data/security logging.
- **Tier 3**: dependencies/supply-chain, crypto/JWT/key handling, rate limiting, and business logic abuse.

For every endpoint or handler that accepts a resource identifier, trace whether the backend binds the target object to the current owner, tenant, organization, or explicit permission before using it. Include single-object routes, list/search/filter routes, bulk operations, nested resource IDs, file IDs, export/import, and destructive actions. Prioritize authenticated-but-wrong-user, wrong-role, cross-tenant, file-id swap, bulk object access, replay, and destructive-operation variants.

For injection and XSS, trace source to sink rather than checking names only: SQL/NoSQL/LDAP, command execution, template rendering, SSRF, path traversal, unsafe redirects, deserialization, and HTML/Markdown/JavaScript/CSS/URL sinks.

## Review Inputs

- **Review Depth**: `quick`, `standard`, `deep`. The profile controls work budget, path coverage, variant analysis, and validation depth.
- **ASVS Level**: `L1`, `L2`, `L3`. The level controls the rigor of OWASP ASVS requirements used for mapping. It is not severity, an OWASP Top 10 category, or a review-depth profile.
- Use `standard + ASVS L2` by default unless the user asks otherwise or the scope is very small.

Depth details are in `references/review-depth-profiles.md`.

## Workflow

1. Establish scope, Review Depth, ASVS Level, constraints, and whether the review is focused or a compact full flow.
2. Use `sec-repo-recon` or equivalent recon to identify structure, stack, entry points, auth, configuration, dependencies, and local repository rules.
3. Build the review streams. Run them sequentially unless the environment and host-repository rules clearly allow a safe split.
4. Load only the relevant file from `references/` for each stream.
5. Confirm findings only with code evidence or a traced path showing that a required security control is absent.
6. Map findings to ASVS through `sec-asvs-review`. Treat OWASP Top 10 only as a supporting risk category.
7. Use `sec-reporting` and `references/report-template.md` for the final report. Include `Findings`, `Observations`, and `Follow-up` when those categories occur; state that a category has no results when it is empty.
8. Do not implement fixes during review. For each finding, return `Remediation` and `Regression Test`.

## Report Language

The final review report must always be written in Polish. Use clear Polish prose for risk descriptions, evidence explanations, impact, remediation, regression tests, observations, and follow-ups. Keep English only for established domain terms without a reasonable Polish equivalent, exact report field names, standards, vulnerability classes, libraries, tools, headers, configuration keys, APIs, and code identifiers.

Avoid casual Polish-English mixing inside explanatory sentences. Prefer natural Polish words when they exist, for example evidence -> `dowód`, impact -> `wpływ`, risk path -> `ścieżka ryzyka`, remediation -> `zalecenie`, regression test -> `test regresyjny`, permission -> `uprawnienie`, owner -> `właściciel zasobu`. Keep concise technical terms when they improve precision, for example `XSS`, `SSRF`, `CSRF`, `IDOR/BOLA`, `JWT`, `OAuth/OIDC`, `claim`, `tenant`, `endpoint`, `cookie`, and `lockfile`.

When a review is launched from a prompt, preserve the exact prompt and final report as artifacts when requested. Use `docs/appsec/{data_iso}_{aplikacja}-prompt.md` for the prompt and `docs/appsec/{data_iso}_{aplikacja}.md` for the report, where `{aplikacja}` is a short repository, application, scope, or sweep slug.

## Area References

- `threat-model.md`
- `entrypoints.md`
- `auth-authz.md`
- `input-data.md`
- `backend-web.md`
- `frontend-web.md`
- `config-secrets.md`
- `dependencies-supply-chain.md`
- `sensitive-data.md`
- `privacy-security-logging.md`
- `abuse-rate-limiting.md`
- `destructive-operations.md`

Each reference is a short operating guide. Do not treat it as a complete checklist catalog or as a substitute for reasoning over the code under review.

## Boundaries

- The review may accept user-provided tool output as context, or run local tools only when explicitly requested or accepted by the user. The package does not run or require scanners during normal use.
- When current documentation for a library, framework, SDK, CLI, cloud service, or tool is needed beyond the local references, record it as a `Follow-up` or a reference-refresh task.
- Change code only when the user separately asks for a specific finding to be fixed.
