---
name: sec-reporting
description: Compact Polish reporting standard for local AppSec review. Use to separate Findings, Observations, and Follow-up without turning partial signals into full findings.
---

# sec-reporting

Write final review reports in Polish. Keep reports concise so review effort goes into finding vulnerabilities, not producing long process documentation.

## Result Types

- **Finding**: confirmed vulnerability or material security risk with local evidence and a realistic exploit or risk path.
- **Candidate Finding**: likely vulnerability with concrete local evidence and a plausible abuse path, but missing confirmation such as runtime behavior, production configuration, reachability, dependency usage, or exploitability in the deployed context.
- **Observation**: short note for hardening, security posture, partial evidence, weakened control, suspicious pattern, or useful signal that does not meet the finding threshold.
- **Follow-up**: short validation task when the repo does not provide enough evidence to decide the issue, such as runtime behavior, production configuration, scanner/tool execution, cloud/gateway/SaaS behavior, current dependency data, login/database access, or separate documentation refresh.

`Candidate Findings`, `Observations`, and `Follow-up` must be shorter than `Findings`. Do not add full remediation, impact, regression-test, or ASVS sections to `Observations` and `Follow-up` unless the user explicitly asks.

## Finding Threshold

Do not label a hypothesis as a `Finding` unless it has code evidence, configuration/IaC/deployment evidence, exposure/routing evidence, tests, or a traced absence of a required control.

Tool output from `npm audit`, `dotnet package list --vulnerable`, Semgrep, CodeQL, secret scanners, or similar tools is supporting input only. Promote it to a `Finding` only when local evidence confirms the path, version, reachability, configuration, or real dependency usage.

Missing negative tests are supporting evidence, not a standalone finding.

Do not keep verification-needed confidence labels as normal finding confidence. If a result has local evidence for a likely vulnerability but still needs confirmation, classify it as `Candidate Finding`. If the necessary validation cannot be resolved from the repository, classify it as `Follow-up`.

Use `Observation` for hardening and security posture issues without a realistic exploit path.

## Report Shape

Every report starts with `Repository Context`, followed by `Summary`, one compact `Overview` table, and then full report sections. The `Summary` count table must include at least `Findings`, `Candidate Findings`, `Observations`, and `Follow-up`; show `0` for empty sections instead of removing the row.

Start reports with:

- `Repository Context`: 1-2 sentences for the reviewed repo purpose and a compact table `Technology | Role`
- `Summary`: count table `Typ | Liczba`
- `Overview`: one compact table `Type | ID | Severity / Candidate Severity | Area` with rows for `Finding`, `Candidate Finding`, `Observation`, and `Follow-up`

Then include these sections:

- `Findings`
- `Candidate Findings`
- `Observations`
- `Follow-up`

If a section has no entries, state that briefly.

Keep `Repository Context` brief. Infer purpose and technologies from local files such as README, manifests, project files, lockfiles, configuration, and directory structure. Do not turn it into architecture documentation.

The `Overview` table is only a quick index. Keep details such as severity, candidate severity, confidence, title, check, evidence, exploit or risk path, fix, regression test, and ASVS mapping in the full sections.

Each `Finding` should contain:

- `Type`: `Finding`
- `Title`
- `Severity`: `critical`, `high`, `medium`, or `low`
- `Location`: file, line, symbol, route, or configuration key
- `Evidence`: concrete local proof; for high, critical, cross-tenant, async, injection, SSRF, replay, or non-obvious findings, include a minimal request, payload, event/message example, or runtime condition when it can be derived from local evidence
- `Exploit/Risk Path`: short abuse scenario from actor and starting access through entry/control gap/sink to effect; include privilege chaining when a small weakness can combine with auth, tenancy, async processing, queues/events, logging gaps, or stale state
- `Impact`
- `Fix`
- `Regression Test`
- `ASVS Mapping`: best quick match, or a short note if no suitable mapping is found quickly
- optional `OWASP Web/API Top 10 Category`

Each `Candidate Finding` should contain:

- `Type`: `Candidate Finding`
- `Title`
- `Candidate Severity`: `critical`, `high`, `medium`, or `low`
- `Confidence`: `high`, `medium`, or `low`
- `Location`
- `Evidence`
- `Missing Confirmation`: what is missing before this can become a `Finding`
- `Potential Exploit/Risk Path`
- `Validation Needed`
- optional `Suggested Fix`

Each `Observation` should explain why it is not a `Finding`. Each `Follow-up` should name the hypothesis or check that needs validation.

Keep `low` and `medium` findings short. Expand mainly for `critical`, `high`, cross-tenant/access-control, injection/RCE, serious secret exposure, async/distributed abuse, replay/idempotency, or non-obvious exploit paths. Consolidate repeated instances of the same vulnerability class into one finding with representative examples.

## Language

Use clear Polish prose. Keep English for established technical terms, standards, vulnerability classes, report field names, library/tool names, headers, configuration keys, APIs, and code identifiers.

Prefer natural Polish terms in explanations: `dowód`, `wpływ`, `ścieżka ryzyka`, `zalecenie`, `test regresyjny`, `uprawnienie`, `właściciel zasobu`.
