# Review Depth Profiles

## Review Checks

- Select `quick`, `standard`, or `deep` before reviewing so the work budget is explicit.
- Select ASVS `L1`, `L2`, or `L3` separately from depth; ASVS level is requirement rigor, not review effort or severity.
- For `quick`, inspect the most important entry points, top web/API risks, representative flows, baseline configuration, obvious auth/authz gaps, major inputs, and riskiest dependencies. State limitations clearly.
- For `standard`, trace main end-to-end flows, representative negative variants, ownership and tenant boundaries, sensitive data, logging, configuration, main web/API risks, and ASVS mapping.
- For `deep`, add broader variant analysis, more negative paths, missing-control analysis, cross-layer interactions, user-provided tool output, and wider dependency/supply-chain review.
- Re-scope, split the review, or report explicit limitations rather than silently downgrading or implying full coverage if the selected depth cannot fit the requested area.

## Evidence Signals

- The report metadata states Review Depth, ASVS Level, scope, local sources, and limitations.
- Reviewed paths match the selected profile and the final report explains skipped areas.
- Scope decisions show what was sampled, what was traced end-to-end, and what was deferred.
- Findings include code evidence or traced missing controls; hypotheses are separated into `Observation` or `Follow-up`.
- Follow-ups capture tool validation, runtime checks, current documentation checks, and out-of-scope areas.

## Common Findings

- Review claims broad coverage while only checking a narrow path.
- ASVS level is confused with severity, OWASP Web/API Top 10 category, or review depth.
- Deep review reports hypotheses as findings without variant analysis or local evidence.
- Quick review omits limitations and reads like a complete certification.

## Offline Boundaries

- Depth does not grant internet, scanner, runtime, SaaS, or cloud access by default.
- If current behavior of a framework, SDK, CLI, cloud, or tool is required and local references are insufficient, record a `Follow-up`.
- Do not claim complete ASVS coverage or certification from this focused offline reference set.
- User-provided scanner output can expand evidence but still needs local triage.

## Sources

See repository-root `SEC-README.md` for source links.
