---
name: sec-reporting
description: Compact Polish reporting standard for local AppSec review. Use to separate Findings, Observations, and Follow-up without turning partial signals into full findings.
---

# sec-reporting

Write final review reports in Polish by default. The report language can change only when the user prompt explicitly includes `Report Language: <language>`. Keep reports concise so review effort goes into finding vulnerabilities, not producing long process documentation.

## Result Types

- **Finding**: confirmed vulnerability or material security risk with local evidence and a realistic exploit or risk path.
- **Candidate Finding**: likely vulnerability with concrete local evidence and a plausible abuse path, but missing confirmation such as runtime behavior, production configuration, reachability, dependency usage, or exploitability in the deployed context.
- **Observation**: short note for hardening, security posture, partial evidence, weakened control, suspicious pattern, or useful signal that does not meet the finding threshold.
- **Follow-up**: short validation task when the repo does not provide enough evidence to decide the issue, such as runtime behavior, production configuration, scanner/tool execution, cloud/gateway/SaaS behavior, current dependency data, login/database access, or separate documentation refresh.

`Candidate Findings`, `Observations`, and `Follow-up` must be shorter than `Findings`. Do not add full remediation, impact, regression-test, or ASVS sections to `Observations` and `Follow-up` unless the user explicitly asks.

For secrets, credentials, tokens, keys, and connection strings, always make the classification explicit: confirmed `Finding`, `Candidate Finding`, or `Observation`. Do not automatically downgrade realistic secrets to `Observation` only because runtime validity cannot be checked offline. Distinguish real secrets from public identifiers, placeholders, sample values, encrypted values, encoded values, hashes, and non-secret IDs. Redact secret values and report only the location, type, pattern, and evidence of use or deployment relevance.

## Finding Threshold

Do not label a hypothesis as a `Finding` unless it has code evidence, configuration/IaC/deployment evidence, exposure/routing evidence, tests, or a traced absence of a required control.

Tool output from `npm audit`, `dotnet package list --vulnerable`, Semgrep, CodeQL, secret scanners, or similar tools is supporting input only. Promote it to a `Finding` only when local evidence confirms the path, version, reachability, configuration, or real dependency usage.

Missing negative tests are supporting evidence, not a standalone finding.

Do not keep verification-needed confidence labels as normal finding confidence. If a result has local evidence for a likely vulnerability but still needs confirmation, classify it as `Candidate Finding`. If the necessary validation cannot be resolved from the repository, classify it as `Follow-up`.

Use `Observation` for hardening and security posture issues without a realistic exploit path.

Severity comes from impact, exploitability, and confidence in the evidence. Do not raise severity for an issue that lacks a realistic exploit or risk path. Do not count `Observation` or `Follow-up` entries as confirmed findings. Use confidence mainly to decide whether a result is a `Finding` or `Candidate Finding`, not to make an uncertain issue look confirmed.

Separate repository evidence from runtime state. A config file, manifest, IaC snippet, or framework option is evidence that the repository declares something; it is not automatically proof that the deployed environment enforces it. If the decision depends on production state, gateway/cloud/SaaS behavior, live identity-provider settings, active secrets, scanner data, or runtime reachability, record that dependency as `Candidate Finding` or `Follow-up`.

## Report Shape

Every report starts with `Repository Context`, followed by a short `Executive Summary`, `Summary`, one compact `Final Findings Overview` table, and then full report sections. The `Summary` count table must include at least `Findings`, `Candidate Findings`, `Observations`, and `Follow-up`; show `0` for empty sections instead of removing the row.

Start reports with:

- `Repository Context`: 1-2 sentences for the reviewed repo purpose and a compact table `Technology | Role`
- `Executive Summary`: 3-5 short bullets or sentences with the main security conclusion, highest-priority confirmed findings, important candidates, and offline limitations
- `Summary`: count table `Typ | Liczba`
- `Final Findings Overview`: one compact table `Type | ID | Severity / Candidate Severity | Area | Decision` with rows for `Finding`, `Candidate Finding`, `Observation`, and `Follow-up`

Then include these sections:

- `Findings`
- `Candidate Findings`
- `Observations`
- `Follow-up`

If a section has no entries, state that briefly.

Keep `Repository Context` brief. Infer purpose and technologies from local files such as README, manifests, project files, lockfiles, configuration, and directory structure. Do not turn it into architecture documentation.

The `Executive Summary` and `Final Findings Overview` are only a quick index and triage aid. Do not repeat the same evidence there. Use the `Decision` column to make the result backlog-friendly: `fix`, `validate`, `observe`, or `follow-up`. Keep details such as severity, candidate severity, confidence, title, check, evidence, exploit or risk path, remediation, regression or validation test, and ASVS mapping in the full sections.

Each `Finding` should contain:

- `Type`: `Finding`
- `Title`
- `Severity`: `critical`, `high`, `medium`, or `low`
- `Location`: file, line, symbol, route, or configuration key
- `Evidence`: concrete local proof; for high, critical, cross-tenant, async, injection, SSRF, replay, or non-obvious findings, include a minimal request, payload, event/message example, or runtime condition when it can be derived from local evidence
- `Exploit/Risk Path`: short abuse scenario from actor and starting access through entry/control gap/sink to effect; include privilege chaining when a small weakness can combine with auth, tenancy, async processing, queues/events, logging gaps, or stale state
- `Impact`
- `Security Goal`: what security property the fix must restore or enforce
- `Remediation Requirement`: the required outcome, without over-designing the implementation
- optional `Implementation Hint`: a short implementation suggestion only when it is obvious from the codebase
- `Regression Test`: a backlog-ready test or acceptance condition proving the issue stays fixed
- `ASVS Mapping`: best quick match, or a short note if no suitable mapping is found quickly
- optional `OWASP Web/API Top 10 Category`

When `Location` contains multiple files, lines, symbols, routes, or configuration keys, present it as a compact table with columns `File` and `Lines / Symbols / Routes`. A single short location may remain a normal `Location: ...` field.

Each `Candidate Finding` should contain:

- `Type`: `Candidate Finding`
- `Title`
- `Candidate Severity`: `critical`, `high`, `medium`, or `low`
- `Confidence`: `high`, `medium`, or `low`
- `Location`
- `Evidence`
- `Missing Confirmation`: what is missing before this can become a `Finding`
- `Potential Exploit/Risk Path`
- `Validation Test`: a backlog-ready test or check that would confirm or reject the candidate
- optional `Remediation Requirement`

Each `Observation` should explain why it is not a `Finding`. Each `Follow-up` should name the hypothesis or check that needs validation.

Keep `low` and `medium` findings short. Expand mainly for `critical`, `high`, cross-tenant/access-control, business-logic abuse, injection/RCE, serious secret exposure, async/distributed abuse, replay/idempotency, or non-obvious exploit paths. Consolidate repeated instances of the same vulnerability class into one finding with representative examples and avoid repeating the same evidence in multiple places.

## Language

Default report language is `Polish`. If the user prompt does not include `Report Language`, the final report must be written in Polish. Use another narrative language only when the prompt explicitly includes `Report Language: <language>`.

Regardless of narrative language, keep stable domain vocabulary in its natural form. Preserve report section and field names, standards, vulnerability classes, library/tool names, APIs, configuration keys, headers, code identifiers, file paths, symbols, routes, package names, and protocol names as they are normally used, often in English.

Use clear Polish prose for the default report. Keep English for established technical terms, standards, vulnerability classes, report field names, library/tool names, headers, configuration keys, APIs, and code identifiers.

Prefer natural Polish terms in explanations: `dowód`, `wpływ`, `ścieżka ryzyka`, `zalecenie`, `test regresyjny`, `uprawnienie`, `właściciel zasobu`.
