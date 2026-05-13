# ASVS Source

Dataset `asvs-5.0.0-local.json` is a curated local list of requirements prepared for offline `sec-*` lookup.

## Review Checks

- Use ASVS as the requirement and finding-mapping standard; use OWASP Web Top 10 and OWASP API Security Top 10 only as optional risk categories.
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
- OWASP Web/API Top 10 category used as a replacement for ASVS mapping.
- ASVS level treated as severity or as proof of complete coverage.
- Report claims complete ASVS conformance from the focused local dataset.

## Offline Boundaries

- This file is not a full copy of ASVS and must not be used to claim complete ASVS conformance.
- The local dataset includes only ASVS 5.0.0 mappings currently used by the `sec-*` review flow. It is a compact lookup library for common web/API findings, not a broad ASVS subset and not certification material.
- If a precise requirement is missing or current ASVS source details matter, record a `Follow-up` to refresh the dataset from official sources before adding that mapping locally.
- Do not copy long ASVS text into review reports or references.

## Source Notes

- Source of truth: OWASP Application Security Verification Standard.
- Stable version used for identifiers: 5.0.0, May 2025.
- OWASP ASVS license: Creative Commons Attribution-ShareAlike 4.0 International.
- Report identifier format: `v5.0.0-<chapter>.<section>.<requirement>`.
- Dataset refresh input: official OWASP ASVS 5.0.0 release asset `OWASP_Application_Security_Verification_Standard_5.0.0_en.flat.json`.
- Selection scope: compact mappings used by current prompts and references for exploitable web/API paths, authentication/session/token handling, authorization, input/data, files, configuration, data protection, logging, supply chain, SSRF, mass assignment, resource consumption, and abuse resistance.
- Exclusions: ASVS requirements not used by current review prompts or local references. Do not keep unused ASVS requirements locally as a future stash.
- The public `asvs-security-review-skill` repository was reviewed as process inspiration for bundled ASVS lookup patterns. It was not used as the copied source dataset or as a copied component.

## Sources

See repository-root `SEC-README.md` for source links.
