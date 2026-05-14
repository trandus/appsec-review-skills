# ASVS Source Notes

Local ASVS data is a complete offline ASVS 5.0.0 mapping aid for findings. It must not be used to claim ASVS conformance or certification.

## Use

- Map confirmed findings after they are identified.
- Keep `ASVS Level` separate from severity and `Review Depth`.
- Use OWASP Web Top 10:2025 and OWASP API Security Top 10:2023 only as optional risk labels.
- If no suitable mapping is found quickly, write a short rationale instead of forcing a weak match.

## Source

- ASVS version: 5.0.0.
- Dataset refresh input: `OWASP_Application_Security_Verification_Standard_5.0.0_en.flat.json` from `OdellMoreno/asvs-security-review-skill`, based on the official OWASP ASVS 5.0.0 release asset.
- License: Creative Commons Attribution-ShareAlike 4.0 International.
- Local dataset: `asvs-5.0.0-local.json`.

## Scope

The local dataset contains all ASVS 5.0.0 requirements, with `L1`, `L2`, and `L3` applicability represented in each requirement's `levels` field. Keep using it only after a candidate finding exists, in line with `sec-appsec-review`.

Do not copy long ASVS text into review reports or references.
