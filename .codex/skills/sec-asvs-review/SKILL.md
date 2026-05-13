---
name: sec-asvs-review
description: Local OWASP ASVS component for offline requirement lookup, L1/L2/L3 selection, and AppSec finding mapping. Use when a review needs ASVS Mapping, a clear distinction between ASVS and OWASP Web/API Top 10, or requirement lookup without internet access.
---

# sec-asvs-review

Use OWASP ASVS as the requirements and finding-mapping standard. OWASP Web Top 10 and OWASP API Security Top 10 are only supporting risk categories; they do not replace ASVS and they do not have `L1`, `L2`, or `L3` levels.

## Offline Data

- Focused offline dataset: `references/asvs-5.0.0-local.json`.
- Source, version, and license notes: `references/asvs-source.md`.
- Helper lookup: `scripts/asvs_lookup.py`.

The dataset is a focused local reference set for offline lookup and mapping of common findings. Do not claim full ASVS certification or complete ASVS coverage from this local reference set.

## Mapping Workflow

1. Establish the ASVS Level: `L1`, `L2`, or `L3`. Default to the level selected by the orchestrator.
2. Search requirements by chapter, keyword, or risk class. Use the helper or read the JSON directly.
3. Select the most specific applicable requirement. If only broad requirements match, or no good mapping exists, record why there is no suitable `ASVS Mapping`.
4. Record mapped requirements with the versioned format, for example `v5.0.0-2.1.1`.
5. Add `OWASP Web/API Top 10 Category` only as an optional label, for example `A01 Broken Access Control` or `API1:2023 Broken Object Level Authorization`.

## Helper Examples

```powershell
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query authorization
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --chapter 8
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L3 --query secret
```

## Community skill

The public `asvs-security-review-skill` repository may be treated only as evaluated process inspiration or as a helper pattern. Do not copy it as the basis for this component. If a concrete fragment is ever used, document the source, license, and adaptation scope in `asvs-source.md`.
