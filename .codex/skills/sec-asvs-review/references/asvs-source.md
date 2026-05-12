# ASVS Source

Dataset `asvs-5.0.0-local.json` is a focused local list of requirements prepared for offline `sec-*` lookup.

## Review Checks

- Use ASVS as the requirement and finding-mapping standard; use OWASP Top 10 only as an optional risk category.
- Record mappings with the versioned format `v5.0.0-<chapter>.<section>.<requirement>`.
- Select the most specific local requirement that matches the confirmed finding.
- If no good mapping exists in the local dataset, explain the lack of suitable `ASVS Mapping` instead of forcing one.
- Keep the selected ASVS level (`L1`, `L2`, or `L3`) separate from severity and review depth.

## Evidence Signals

- Local lookup results from `references/asvs-5.0.0-local.json` or `scripts/asvs_lookup.py`.
- Finding evidence that matches the mapped requirement's control intent.
- Report metadata showing ASVS version and selected level.
- Mapping rationale when the requirement is broad or no suitable local requirement exists.

## Common Findings

- Finding mapped to a broad or unrelated ASVS item because a closer requirement was not checked.
- OWASP Top 10 category used as a replacement for ASVS mapping.
- ASVS level treated as severity or as proof of complete coverage.
- Report claims complete ASVS conformance from the focused local dataset.

## Offline Boundaries

- This file is not a full copy of ASVS and must not be used to claim complete ASVS conformance.
- The local dataset supports common offline lookup and mapping, not certification.
- If a precise requirement is missing or current ASVS source details matter, record a `Follow-up` to refresh the dataset from official sources.
- Do not copy long ASVS text into review reports or references.

## Source Notes

- Source of truth: OWASP Application Security Verification Standard.
- Stable version used for identifiers: 5.0.0, May 2025.
- OWASP ASVS license: Creative Commons Attribution-ShareAlike 4.0 International.
- Report identifier format: `v5.0.0-<chapter>.<section>.<requirement>`.
- The public `asvs-security-review-skill` repository was not used as a source dataset or copied component. It may be evaluated only as process inspiration or as a helper pattern in separate work.

## Sources

See repository-root `SEC-README.md` for source links.
