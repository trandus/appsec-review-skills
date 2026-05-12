# Review Depth Profiles

## Review Checks

- Select `quick`, `standard`, or `deep` before reviewing so the work budget is explicit.
- Select ASVS `L1`, `L2`, or `L3` separately from depth; ASVS level is requirement rigor, not review effort or severity.
- For `quick`, inspect the most important entry points, baseline configuration, obvious auth/authz gaps, major inputs, and riskiest dependencies.
- For `standard`, trace main end-to-end flows, negative variants, ownership boundaries, sensitive data, logging, configuration, and ASVS mapping.
- For `deep`, add variant analysis, more negative paths, missing-control analysis, cross-layer interactions, user-provided tool output, and broader dependency review.
- Re-scope rather than silently downgrading if the selected depth cannot fit the requested area.

## Evidence Signals

- The report metadata states Review Depth, ASVS Level, scope, local sources, and limitations.
- Reviewed paths match the selected profile and the final report explains skipped areas.
- Findings include code evidence or traced missing controls; hypotheses are separated into `Observation` or `Follow-up`.
- Follow-ups capture tool validation, runtime checks, current documentation checks, and out-of-scope areas.

## Common Findings

- Review claims broad coverage while only checking a narrow path.
- ASVS level is confused with severity, OWASP Top 10 category, or review depth.
- Deep review reports hypotheses as findings without variant analysis or local evidence.
- Quick review omits limitations and reads like a complete certification.

## Offline Boundaries

- Depth does not grant internet, scanner, runtime, SaaS, or cloud access by default.
- If current behavior of a framework, SDK, CLI, cloud, or tool is required and local references are insufficient, record a `Follow-up`.
- Do not claim complete ASVS coverage or certification from this focused offline reference set.
- User-provided scanner output can expand evidence but still needs local triage.

## Sources

See repository-root `SEC-README.md` for source links.
