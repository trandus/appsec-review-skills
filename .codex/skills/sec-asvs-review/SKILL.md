---
name: sec-asvs-review
description: Thin local OWASP ASVS mapper for AppSec findings. Use after a concrete Finding or Candidate Finding exists and an ASVS Mapping is needed without internet access.
---

# sec-asvs-review

Use ASVS as a lightweight mapping aid, not as the driver of the review. First identify a concrete `Finding` or `Candidate Finding`; then add the best quick ASVS mapping when useful.

OWASP Web Top 10:2025 and OWASP API Security Top 10:2023 are optional risk labels. They do not replace ASVS and do not have `L1`, `L2`, or `L3` levels.

## Local Data

- Complete local ASVS 5.0.0 dataset: `references/asvs-5.0.0-local.json`.
- Source/version/license notes: `references/asvs-source.md`.
- Optional helper: `scripts/asvs_lookup.py`.

The dataset contains all ASVS 5.0.0 requirements in the local lookup format. Do not claim ASVS certification or use it as a checklist that drives vulnerability hunting.

## Mapping Rules

1. Use the selected `ASVS Level`; default is `L2`.
2. Search by vulnerability class, control, chapter, or keyword.
3. Select the most specific quick match, formatted like `v5.0.0-2.1.1`.
4. If no suitable match is found quickly, write a short mapping rationale instead of spending review time on lookup.
5. Do not let ASVS lookup delay or narrow vulnerability hunting.

## Helper Examples

```powershell
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query authorization
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query injection
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query secret
```
