---
name: quality-audit
description: "Application quality audit for repository review: architecture, source code quality, bug risks, performance, tests, error handling, logging, quick wins, refactoring areas, technical priorities, technical debt, and Jira-import JSON output. Use for local quality/engineering-health audits of any application stack."
disable-model-invocation: true
---

# quality-audit

Run a local quality code review focused on finding the maximum number of justified engineering findings. Hunt for real technical risks across the repository, then write the shortest report that remains useful for triage and fixing.

The goal is broad evidence-backed discovery, not a fixed checklist. Use the areas below as directions to hunt. Follow the repository shape, architecture, conventions, and domain flows. If there is a choice between polishing wording and checking another realistic code path, check the next code path.

This skill covers repository quality review: architecture, source quality, bug/antipattern risks, performance, test quality, error handling, logging, technical summary, improvement recommendations, technical priorities, refactoring areas, and technical debt estimate.

## Defaults

- Report and JSON file language: Polish with diacritics, unless the user explicitly provides `Report Language: <language>`.
- Markdown output file: `./quality-audits/quality-audit-<YYYY-MM-DD-HHmm>.md` in the reviewed repository root, unless the user provides another path.
- JSON output file: `./quality-audits/quality-audit-<YYYY-MM-DD-HHmm>.json` next to the Markdown report, unless the user disables JSON output or provides another path.
- Normal mode: offline, local repository only, no internet, no GitHub, no SaaS, no runtime access, no external scanners, no fixes, and no package upgrades unless the user separately asks.
- Do not run builds. Do not run commands whose main purpose is to compile, package, publish, container-build, restore remote dependencies, or launch the application.
- Prefer read-only inspection and existing local evidence. Tests, linters, or analyzers may be read from existing output files; run them only if the user explicitly asks.

Chat reply after writing both files:

`quality-audit-2026-05-20-1430.md + quality-audit-2026-05-20-1430.json - Findings: 12 (9 confirmed, 3 needs-verification), Dismissed: 4, Technical debt: medium`

## Internal Recon

Start with a short internal repository profile for hunting only. Use raw notes only to fill `Repository Context`.

- application type, main technologies, repository layout, and local instructions;
- main entry points: UI routes, APIs, jobs, workers, CLIs, message consumers, file processors, integrations, and deployment/runtime configuration;
- important business/runtime flows, state ownership, persistence, external calls, caching, queues, files, and generated artifacts;
- module boundaries, shared abstractions, duplicated responsibilities, and high-change areas;
- test structure, CI hints, diagnostics, logging, and operational assumptions visible in the repo.

Respect repository-specific instructions unless they conflict with the user request. Treat ignored, generated, vendored, minified, migration-generated, or build-output files cautiously unless they are relevant to runtime behavior, deployment, architecture, or local evidence.

## Hunting Directions

Check every applicable area below, but do not stop there. Skip areas with no matching surface. Hunt concrete risk paths, correlate across files, and keep looking after the first finding in a category.

### Architecture

Layering, module boundaries, dependency direction, circular coupling, unclear ownership, god modules, duplicated business rules, leaky abstractions, mixed responsibilities, change hotspots, and architecture that makes common changes risky.

### Code Quality and Bug Risk

Incorrect edge cases, fragile branching, hidden assumptions, null/empty/time/culture/money/state errors, inconsistent validation, unsafe sequencing, resource lifetime mistakes, concurrency/idempotency problems, copy-paste logic drift, and code that is hard to reason about.

### Runtime Flows

Trace representative user, API, job, worker, integration, data-processing, and UI-to-backend flows from entry point to output/persistence. Look for missing validation, inconsistent contracts, weak error paths, poor transaction/state boundaries, and unclear retry or failure behavior.

### Performance

Repeated remote/database calls, unbounded queries or payloads, missing pagination/streaming, inefficient loops over I/O, blocking work in hot paths, uncontrolled concurrency, cache misuse, expensive startup/runtime work, frontend re-render or bundle risks, and scalability assumptions.

### Tests and Testability

Missing tests around critical behavior, tests that assert implementation details, fragile mocks, weak negative/edge coverage, low-value tests, ignored/flaky tests, hidden I/O, static state, time/randomness coupling, and code structure that prevents meaningful testing.

Do not report low coverage alone. Tie test findings to specific unprotected behavior or risky change areas.

### Error Handling, Logging, and Operations

Swallowed or overbroad exceptions, inconsistent error contracts, missing diagnostics in important flows, noisy or misleading logs, missing correlation/context, weak retry/failure visibility, fragile configuration, environment drift, unclear health/operational behavior, and deployment/runtime assumptions that can break quality.

### Maintainability and Refactoring

Areas where future changes are expensive or risky: high-complexity modules, repeated concepts, inconsistent conventions, unclear names, domain leakage, poor cohesion, weak seams for tests, and refactoring opportunities that reduce real risk.

### Dependencies

Do not perform a vulnerability or BlackDuck-style dependency audit. Mention dependencies only when local evidence shows quality impact: unsupported/runtime compatibility risk, upgrade blockage, duplicate stacks, brittle generated clients, build/runtime fragility, or maintainability cost.

## Rules

1. Reference real local evidence: file path and line, symbol, route, config key, test, or documented convention.
2. No generic advice. A recommendation must point to a concrete repository problem.
3. Do not report style preferences unless they create real correctness, performance, maintainability, testability, operational, or delivery risk.
4. If a control, validation, test, transaction, retry, abstraction, or convention is not visible in the repo, treat it as absent or mark confidence as `needs-verification`.
5. Validate every candidate: confirmed, needs-verification, or dismissed. Do not leave ambiguous candidates.
6. Scanner/analyzer output is supporting evidence only. Promote it only when local code evidence confirms relevance.
7. Consolidate repeated instances of the same problem into one finding with representative examples.
8. Redact secrets or sensitive values if encountered. Report the location and type, not the value.
9. Do not edit code, configuration, formatting, dependencies, or generated files unless the user separately asks.

## Evidence Gate

Every candidate issue identified during hunting must be resolved as:

- **Finding (confirmed)** - local evidence proves a realistic quality, correctness, performance, testability, maintainability, or operational problem.
- **Finding (needs-verification)** - local evidence suggests a likely problem, but confirmation requires runtime behavior, production configuration, domain knowledge, traffic, or external context. State what is missing.
- **Dismissed** - investigated as a likely candidate, but local evidence disproves it. Include dismissed items only when useful for triage or when they explain a plausible false positive.

## Severity

- `critical`: likely production outage, data corruption/loss, systemic failure of core flows, or architecture issue blocking safe evolution.
- `high`: serious correctness risk, important performance/scalability risk, fragile critical path, missing tests around high-impact behavior, severe coupling, or realistic operational failure.
- `medium`: meaningful bounded quality, maintainability, testability, performance, or operational problem.
- `low`: isolated issue, quick win, local cleanup, or limited-risk improvement with concrete value.

Severity comes from impact, likelihood, affected flow, blast radius, frequency of change, and cost of delay.

## Area

Area values:

- `backend`
- `frontend`
- `full-stack`
- `data`
- `tests`
- `build-ops`
- `infrastructure`
- `documentation`
- `cross-cutting`

## Report Shape

```md
## Repository Context

Application type, major technologies, repository shape, runtime flows, and scope limits.

## Summary

Findings: N (M confirmed, K needs-verification) · Dismissed: D · Technical debt: low|medium|high

| Severity | Findings | Confirmed |
|-----------|-----------|-----------|
| Critical | 0 | 0 |
| High | 0 | 0 |
| Medium | 0 | 0 |
| Low | 0 | 0 |

Overall quality assessment.

## Findings

Confirmed findings first, then needs-verification.

## Dismissed

Investigated false positives useful for triage.

```

## JSON Output

Generate the JSON only after the Markdown report is complete and all candidates have been resolved through the Evidence Gate. Do not spend hunting time shaping JSON. Treat JSON generation as a final packaging step from the finished report.

Create one parseable `.json` file for Jira import. The JSON is not an audit report; it is only an issue import payload. Its shape is closed: use exactly the keys shown below and no extra metadata, summaries, repository context, verification data, `findings`, or `dismissed` sections.

```json
{
  "common": {
    "labels": [
      "<APPLICATION_NAME>"
    ]
  },
  "issues": [
    {
      "summary": "[<APPLICATION_NAME>] QF-01 - <title>",
      "description": "...",
      "labels": [
        "HIGH"
      ]
    }
  ]
}
```

Rules:

1. Derive `issues` only from the final Markdown `## Findings` section. Include every `confirmed` and `needs-verification` finding; exclude dismissed items and rejected candidates.
2. Use the reviewed application/repository name as `<APPLICATION_NAME>` unless the user provides `Application Name: <name>`.
3. `common.labels` contains only `<APPLICATION_NAME>`. Each issue `labels` contains only the uppercase severity: `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
4. `summary` format is `[<APPLICATION_NAME>] QF-01 - <title>`. Preserve the exact finding ID and title from the Markdown report.
5. `description` uses Jira REST API / Atlassian Markdown formatting and carries the finding fields from the report: Severity, Confidence, Area, Category, Location, Evidence, Risk Path, Risk/Impact, Recommendation, Effort. Omit missing fields; do not invent details.
6. Before writing the file, check that root keys are exactly `common` and `issues`; `common` has only `labels`; each issue has only `summary`, `description`, and `labels`.

### Finding format

```md
### QF-01 - <title>

- Severity: critical | high | medium | low
- Confidence: confirmed | needs-verification
- Area: backend | frontend | full-stack | data | tests | build-ops | infrastructure | documentation | cross-cutting
- Category: architecture | code-quality | bug-risk | performance | tests | logging | maintainability | operations | dependencies | other
- Location: file path and line, symbol, route, or configuration key
- Evidence: concrete local evidence, minimal quote or precise behavior
- Risk/Impact: application-specific impact
- Risk Path:
  1. Trigger, change, or runtime condition
  2. Faulty behavior
  3. Operational, correctness, delivery, or maintenance impact
- Recommendation: concrete direction tied to the evidence
- Effort: small | medium | large
```

### Dismissed format

```md
### D-01 - <title>

- Area: backend | frontend | full-stack | data | tests | build-ops | infrastructure | documentation | cross-cutting
- Category: architecture | code-quality | bug-risk | performance | tests | logging | maintainability | operations | dependencies | other
- Location: file path and line, symbol, route, or configuration key
- Why flagged: what made it look like a finding
- Why dismissed: local evidence that disproves it
```

## Do not

- Do not run builds (ie. `dotnet build`, `npm run build`,...) or launch the application.
- Do not perform a security, dependency-vulnerability, or compliance audit unless the user asks.
- Do not duplicate simple SonarQube/IDE findings unless repository reasoning shows real impact.
- Do not invent project conventions or assume missing code exists elsewhere.
- Do not recommend rewrites when targeted refactoring is enough.
- Do not include vague recommendations like "improve architecture", "add tests", or "use best practices" without evidence and location.
