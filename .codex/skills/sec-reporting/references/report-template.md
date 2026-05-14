# Compact AppSec Report Template

Use this compact shape for AppSec review reports. The template is for Polish reports by default. The report language can change only when the user prompt explicitly includes `Report Language: <language>`.

Keep canonical report fields, section names, standards, vulnerability classes, library/tool names, APIs, configuration keys, code identifiers, file paths, symbols, routes, package names, and protocol names stable in their natural form, even when the narrative language changes.

## Repository Context

- Purpose: <very short description of what the reviewed repo/application does>

| Technology | Role | Evidence |
| --- | --- | --- |
| <technology> | <short role, e.g. backend, frontend, database, auth, tests> | <README/manifest/project/config path> |

## Executive Summary

- <short security conclusion>
- <highest-priority confirmed finding or "no confirmed findings">
- <important candidate/follow-up or offline limitation>

## Summary

| Typ | Liczba |
| --- | ---: |
| Findings | 0 |
| Candidate Findings | 0 |
| Observations | 0 |
| Follow-up | 0 |

## Final Findings Overview

| Type | ID | Severity / Candidate Severity | Area | Decision |
| --- | --- | --- | --- | --- |
| Finding | F-01 | <severity> | <area> | fix |
| Candidate Finding | CF-01 | <candidate severity> | <area> | validate |
| Observation | O-01 | n/a | <area> | observe |
| Follow-up | FU-01 | n/a | <area> | follow-up |

## Findings

### F-01: <title>

- Type: Finding
- Severity:
- Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `<path/to/file>` | `:<line>`, `<symbol>`, `<route>` |
| `<path/to/other-file>` | `:<line>` |

- Evidence:
- Exploit/Risk Path:
- Impact:
- Security Goal:
- Remediation Requirement:
- Implementation Hint:
- Regression Test:
- ASVS Mapping:

## Candidate Findings

### CF-01: <title>

- Type: Candidate Finding
- Candidate Severity:
- Confidence:
- Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `<path/to/file>` | `:<line>`, `<symbol>`, `<route>` |

- Evidence:
- Missing Confirmation:
- Potential Exploit/Risk Path:
- Validation Test:
- Remediation Requirement:

## Observations

- O-01: <title>
  - Type: Observation
  - Evidence:
  - Why not a Finding:
  - Suggested Action:

## Follow-up

- FU-01: <check>
  - Type: Follow-up
  - Hypothesis:
  - Why cannot be decided from repo:
  - Validation needed:
  - Evidence that would change the decision:
