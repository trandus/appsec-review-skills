---
name: sec-appsec-review
description: Offline-first AppSec code review orchestrator. Use when the user asks for a repository security review, a focused security review, ASVS mapping, or a Polish report with remediation and regression tests.
disable-model-invocation: true
---

# sec-appsec-review

Run a local security code review, not runtime penetration testing. The main goal is to find as many real, exploitable vulnerabilities as practical in one pass for the selected scope and `Review Depth`.

Use the local repository, host-repository instructions such as `AGENTS.md` and `CLAUDE.md` when present, repository-root `SEC-README.md` when present, the `sec-*` skills, and local files under this skill. Do not require internet access, GitHub, SaaS products, Context7, external scanners, or runtime access during normal review work.

## Defaults

- `Review Depth`: `standard`.
- `ASVS Level`: `L2`.
- Default mode: offline, no automatic scanners, no fixes.
- Optional helper: use `repomix` output when available, allowed by repo instructions, and useful for the repository size or scope. Treat packed output as navigation input; verify material evidence against local files before reporting a `Finding`.

## Tiered Review Priority

Always use the tiered baseline in `references/risk-baseline.md` to decide work order, and apply `references/always-check.md` only as a tiny reminder of obvious, high-yield checks that are easy to miss. Select only the always-check areas that match the audited application, technology, exposed surfaces, and selected scope; do not mechanically execute every area for every review. Tiers prioritize review cost and expected exploitability; they are not severity labels and not ASVS levels. Prioritize confirmed, exploitable paths over broad coverage claims.

- `Tier 1`: start with the most exploitable and usually highest-yield paths.
- `Tier 2`: continue into important risks that need more context, cross-file tracing, or representative variants.
- `Tier 3`: cover broader, costlier, architecture-dependent, or uncommon areas when the repository surface justifies them.

Severity comes from impact, exploitability, and application context, not from the tier number. A `Tier 2` issue can be `critical`, and a `Tier 1` signal can remain an `Observation` if local evidence does not support a realistic abuse path. Correlate small weaknesses across authorization, tenancy, async processing, queues/events, logging gaps, stale state, replay, and idempotency before deciding final severity.

## Review Depth

- `quick`: limit sampling and focus mainly on `Tier 1`; state important limitations.
- `standard`: cover `Tier 1`, representative `Tier 2`, and selected `Tier 3` areas based on repository surface.
- `deep`: broaden variants, negative paths, cross-layer checks, and stronger `Tier 3` coverage.

ASVS level controls mapping rigor, not review effort or severity. Use `sec-asvs-review` only after a candidate finding exists.

## Evidence Gate

Report a `Finding` only when local code, configuration, IaC/deployment, routing/exposure evidence, tests, or a traced missing control supports a realistic abuse path. Reference real files, symbols, routes, keys, tests, or narrow code paths.

Do not report generic best practices, style issues, missing tests alone, or scanner output alone. If evidence points to a likely vulnerability but needs validation, use `Candidate Finding`. If it is hardening, posture, partial evidence, or a check that cannot be decided from the repo, use `Observation` or `Follow-up`.

Do not assume cloud, gateway, CDN, WAF, identity-provider, SaaS, framework, SDK, CLI, or production configuration behavior unless it is proven by local repository evidence or user-provided context.

For secrets, redact values. Report the location and pattern, not the secret value. Treat dummy/sample values as `Observation` unless local evidence shows production-like, deployment-active, shared, colliding, or materially risky use.

For Swagger/OpenAPI/ReDoc and diagnostics, confirm a `Finding` only when local code/config/IaC indicates non-development exposure, missing auth, sensitive API disclosure, or risky internal/admin/debug surface. Otherwise use `Observation` or `Follow-up`.

## Output

Write final review reports in Polish. Use `sec-reporting` as the only source of truth for the compact report shape; this skill orchestrates the review and does not define a separate report template:

- `Findings`: confirmed vulnerabilities or material risks.
- `Candidate Findings`: likely vulnerabilities with local evidence but missing confirmation.
- `Observations`: short, lower-detail notes for partial evidence or weakened controls.
- `Follow-up`: short validation tasks for runtime, production config, scanner, cloud/SaaS, documentation, or access-dependent checks.

Each `Finding` includes `Type`, `Title`, `Severity`, `Location`, `Evidence`, `Exploit/Risk Path`, `Impact`, `Fix`, `Regression Test`, and `ASVS Mapping` when a quick suitable mapping exists. Do not keep verification-needed confidence labels on a `Finding`; move that result to `Candidate Findings` or `Follow-up`.

Do not implement fixes unless the user separately asks.
