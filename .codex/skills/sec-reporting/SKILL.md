---
name: sec-reporting
description: Reporting standard for local AppSec review. Use when you need to distinguish Finding, Observation, and Follow-up entries; prepare an evidence-based report; add ASVS Mapping, Remediation, Regression Test, and Fix Prompt sections; and avoid implementing fixes during review.
---

# sec-reporting

Report concisely, but make every claim defensible. Do not label a hypothesis as a `Finding` unless it has code evidence or a traced absence of a required security control.

Tool output from `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, Semgrep, CodeQL, or similar scanners is supporting input only. A tool result becomes a `Finding` only when the report ties it to local code, a manifest, a lockfile, configuration, package source settings, or real dependency usage and explains reachability or impact. Unconfirmed, unreachable, stale, or environment-blocked tool results belong in `Observation` or `Follow-up`.

## Report Language

Write every final review report in Polish. Keep technical labels and field names in English when useful for portability, for example `Finding`, `Observation`, `Follow-up`, `Evidence`, `Risk Path`, `ASVS Mapping`, `OWASP Top 10 Category`, and `Fix Prompt`, but write the report body, risk explanations, remediation text, regression-test guidance, observations, follow-ups, and fix prompts in Polish.

## Result Types

- **Finding**: a confirmed vulnerability or material risk with location, evidence, Risk Path, and Impact.
- **Observation**: a design observation, weakened control, tool signal, or incomplete hypothesis without enough evidence for a finding.
- **Follow-up**: a question, tool validation, need for current documentation, unavailable network/login/database/configuration, or separate check.

## Required Finding Format

Each `Finding` contains:

- title,
- severity and confidence,
- status,
- location: file, line or narrowest practical range, symbol/route/configuration key,
- evidence in code or a traced missing control,
- Risk Path,
- Impact,
- Remediation,
- Regression Test or validation,
- `ASVS Mapping` or a rationale for no suitable mapping,
- optional `OWASP Top 10 Category`,
- `Fix Prompt` for a separate repair task.

## Fix Prompt

`Fix Prompt` must include the finding title, repair scope, locations, risk description, expected behavior after the fix, suggested Remediation, required Regression Test, and scope limits. The prompt must not include an implementation unless the user separately asks for the fix.

The report template is in `references/report-template.md`.
