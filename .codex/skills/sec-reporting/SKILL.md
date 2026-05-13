---
name: sec-reporting
description: Reporting standard for local AppSec review. Use when you need to distinguish Findings, Observations, and Follow-up entries; prepare an evidence-based report; add Attack Variant, ASVS Mapping, Remediation, and Regression Test sections; and avoid implementing fixes during review.
---

# sec-reporting

Report concisely, but make every claim defensible. Do not label a hypothesis as a `Finding` unless it has code evidence or a traced absence of a required security control.

Tool output from `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, Semgrep, CodeQL, or similar scanners is supporting input only. A tool result becomes a `Finding` only when the report ties it to local code, a manifest, a lockfile, configuration, package source settings, or real dependency usage and explains reachability or impact. Unconfirmed, unreachable, stale, or environment-blocked tool results belong in `Observation` or `Follow-up`.

## Report Language

Write every final review report in Polish. Use clear Polish prose for summaries, evidence explanations, risk paths, impact, remediation, regression-test guidance, observations, and follow-ups.

Keep English only when it is a strong domain term without a reasonable Polish equivalent, an exact report field name, a standard, a vulnerability class, a library/tool name, a header/configuration/API name, or a code identifier. Avoid casual Polish-English mixing inside explanatory sentences. Prefer natural Polish words when they exist, for example evidence -> `dowód`, impact -> `wpływ`, risk path -> `ścieżka ryzyka`, remediation -> `zalecenie`, regression test -> `test regresyjny`, permission -> `uprawnienie`, owner -> `właściciel zasobu`. Keep concise technical terms when they improve precision, for example `XSS`, `SSRF`, `CSRF`, `IDOR/BOLA`, `JWT`, `OAuth/OIDC`, `claim`, `tenant`, `endpoint`, `cookie`, and `lockfile`.

## Result Types

- **Finding**: a confirmed vulnerability or material risk with location, evidence, Risk Path, and Impact.
- **Observation**: a design observation, weakened control, tool signal, or incomplete hypothesis without enough evidence for a finding.
- **Follow-up**: a question, tool validation, separate reference-refresh need, unavailable network/login/database/configuration, or separate check.

## Required Report Sections

Every final report must include `Findings`, `Observations`, and `Follow-up` when those categories occur. If a category has no entries, state that explicitly, for example `Findings: brak potwierdzonych findingow`.

Missing negative tests are supporting evidence, not a standalone finding, unless the implementation path also confirms the missing control.

When the review prompt asks for persisted artifacts, save the exact prompt to `docs/appsec/{data_iso}_{aplikacja}-prompt.md` and the final report to `docs/appsec/{data_iso}_{aplikacja}.md`. Use a short repository, application, scope, or sweep slug for `{aplikacja}`.

## Required Finding Format

Each `Finding` contains:

- title,
- severity and confidence,
- status,
- location: file, line or narrowest practical range, symbol/route/configuration key,
- evidence in code or a traced missing control,
- Attack Variant, for example `authenticated-but-wrong-user`, `wrong-role`, `cross-tenant`, `bulk object access`, `stored XSS`, `reflected XSS`, `SQL injection`, `file-id swap`, or `replay`,
- Risk Path,
- Impact,
- Remediation,
- Regression Test or validation,
- `ASVS Mapping` or a rationale for no suitable mapping,
- optional `OWASP Web/API Top 10 Category`.

The report template is in `references/report-template.md`.
