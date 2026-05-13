# AppSec Review Report Template

## Review Checks

- Write the final report in Polish. Technical labels may stay in English, but summaries, evidence explanations, risk paths, impact, remediation, regression tests, observations, follow-ups, and fix prompts must be Polish.
- Separate `Findings`, `Observations`, `Follow-up`, and `Out of Scope` instead of mixing confidence levels. If a category has no entries, state that explicitly.
- Report a `Finding` only when local code evidence or a traced missing control supports it.
- Include `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` or a mapping rationale, and `Fix Prompt`.
- Record current-documentation, scanner, runtime, SaaS, cloud, and environment checks as `Follow-up` when they cannot be proven locally.
- Keep source attribution short; source links live in repository-root `SEC-README.md`.

## Evidence Signals

- Findings cite files, symbols, routes, keys, test names, or narrow code paths.
- Evidence connects source, control, sink, and impact rather than listing a general best practice.
- Observations explain why the evidence is incomplete.
- Follow-ups state the validation needed and the expected decision it will unlock.

## Common Findings

- Confirmed vulnerability or material risk with a local proof path.
- Missing required server-side control after tracing an entry point to a protected resource or sensitive sink.
- Risk from configuration, dependency, logging, data handling, or destructive operations that is active under local conditions.
- Repeated instances of the same control gap consolidated into one finding with examples.

## Offline Boundaries

- Do not use a current CVE, advisory, framework behavior, cloud default, or scanner rule as a finding unless the result is locally present or documented in the reviewed repo.
- If local references do not resolve current behavior, write a `Follow-up` to refresh the reference or check official documentation.
- Do not claim penetration testing, runtime exploitation, complete ASVS verification, or legal compliance from offline code review.
- Do not include long source-link lists in each report; use repository-root `SEC-README.md`.

## Metadata

- Scope:
- Review Mode: focused area review / compact full flow
- Review Depth:
- ASVS Level:
- Local Sources:
- Limitations:

## Executive Summary

Briefly describe the most important risks, scope, and limitations. Do not claim certification or complete runtime penetration testing.

## Findings

### Finding: <title>

- Severity:
- Confidence:
- Status: confirmed
- Location:
- Evidence:
- Attack Variant:
- Risk Path:
- Impact:
- Remediation:
- Regression Test:
- ASVS Mapping:
- OWASP Top 10 Category:

#### Fix Prompt

Fix finding `<title>` within `<scope>`. Start from `<files/symbols>`. Risk: `<description>`. Expected behavior after the fix: `<description>`. Apply remediation direction `<approach>`. Add or update regression test `<test>`. Preserve local repository conventions and do not expand scope beyond this finding.

## Observations

- Observation:
  - Partial Evidence:
  - Why this is not a Finding:
  - Suggested Next Step:

## Follow-up

- Follow-up:
  - Question or Validation:
  - Why Needed:
  - Owner / Next Step:

## Sources

See repository-root `SEC-README.md` for source links.
