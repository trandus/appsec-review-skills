# Security Review Report Template

## Review Checks

- Write the final report in Polish. Technical labels may stay in English, but summaries, evidence explanations, risk paths, impact, remediation, regression tests, observations, follow-ups, and fix prompts must be Polish.
- Separate confirmed `Finding` entries from `Observation` and `Follow-up`.
- Require local evidence or a traced missing control for every finding.
- Include remediation and a `Fix Prompt` without implementing the fix.
- Use ASVS mapping when a suitable local requirement exists; explain when no good mapping applies.
- Keep source lists short and point to repository-root `SEC-README.md` for refresh links.

## Evidence Signals

- File, route, symbol, configuration key, dependency manifest, or test location is named precisely.
- Evidence shows how the issue is reachable and why the existing control is absent or ineffective.
- Scanner or audit output is tied to the local dependency, code path, commit, or configuration under review.
- Follow-ups explain what current documentation, scanner, runtime, SaaS, cloud, or environment check is still needed.

## Common Findings

- Broken access control, injection, XSS, CSRF, sensitive-data exposure, security misconfiguration, vulnerable local dependency evidence, missing audit logging, or unsafe destructive operation.
- Repeated missing-control pattern across multiple endpoints or modules.
- Confirmed dependency or secret exposure when local tool output or repository evidence proves the affected package/path.
- Local configuration that activates insecure behavior in non-development contexts.

## Offline Boundaries

- Do not convert hypotheses, stale scanner output, or undocumented current framework behavior into findings.
- Current CVEs/advisories, SaaS settings, cloud defaults, identity-provider behavior, and scanner rule semantics need local evidence or `Follow-up`.
- The report is not a penetration test, full ASVS certification, legal assessment, or runtime assurance.
- If local references are insufficient for a framework, SDK, CLI, cloud service, or tool, write a `Follow-up` and continue with locally reviewable evidence.

## Finding

- Title:
- Severity:
- Confidence:
- Status:
- Location:
- Code Evidence:
- Risk Path:
- Impact:
- Remediation:
- Regression Test:
- ASVS Mapping:
- OWASP Top 10 Category:
- Fix Prompt:

## Observation

- Description:
- Partial Evidence:
- Risk:
- Why this is not a Finding:
- Next Step:

## Follow-up

- Question / Validation:
- Context:
- Expected Result:

## Sources

See repository-root `SEC-README.md` for source links.
