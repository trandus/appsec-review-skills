# Security Review Report Template

## Review Checks

- Write the final report in Polish. Use English only for established domain terms without a reasonable Polish equivalent, exact report field names, standards, vulnerability classes, libraries, tools, headers, configuration keys, APIs, and code identifiers.
- Avoid casual Polish-English mixing. Prefer natural Polish words in explanatory prose, for example `dowód`, `wpływ`, `ścieżka ryzyka`, `zalecenie`, `test regresyjny`, `uprawnienie`, and `właściciel zasobu`.
- Separate confirmed `Findings` entries from `Observations` and `Follow-up`. If a category has no entries, state that explicitly.
- Require local evidence or a traced missing control for every finding.
- Include remediation and regression-test guidance without implementing the fix.
- If the prompt requests persisted artifacts, save the exact prompt to `docs/appsec/{data_iso}_{aplikacja}-prompt.md` and this report to `docs/appsec/{data_iso}_{aplikacja}.md`.
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

## Findings

### Finding: <title>

- Title:
- Severity:
- Confidence:
- Status:
- Location:
- Code Evidence:
- Attack Variant:
- Risk Path:
- Impact:
- Remediation:
- Regression Test:
- ASVS Mapping:
- OWASP Web/API Top 10 Category:

## Observations

### Observation

- Description:
- Partial Evidence:
- Risk:
- Why this is not a Finding:
- Next Step:

## Follow-up

### Follow-up

- Question / Validation:
- Context:
- Expected Result:

## Sources

See repository-root `SEC-README.md` for source links.
