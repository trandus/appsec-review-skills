---
name: quality-audit-2
description: "Application quality audit for repository review: architecture, source code quality, bug risks, performance, tests, error handling, logging, quick wins, refactoring areas, technical priorities, technical debt, and Jira-import JSON output. Use for local quality/engineering-health audits of any application stack."
disable-model-invocation: true
---

# quality-audit

Run a local quality code review focused on identifying real, material, evidence-backed engineering problems within the reviewed scope. The goal is not to maximize the number of findings. A scan with no findings is a valid and desirable outcome when the available evidence does not justify reporting a problem.

Maintain a consistent threshold for what qualifies as a finding throughout the audit. Do not lower the threshold of severity, likelihood, evidence, or practical impact merely because more obvious problems have already been found or fixed.

The goal is broad evidence-backed discovery, not a fixed checklist. Use the areas below as directions to hunt. Follow the repository shape, architecture, conventions, and domain flows. Explore additional realistic code paths when they can reveal materially different risks, but do not manufacture findings from increasingly speculative, contrived, or extremely unlikely scenarios.

A candidate should become a finding only when there is concrete local evidence of a realistic defect, quality risk, maintainability problem, performance issue, testability problem, or operational failure mode. The mere possibility of constructing a hypothetical failure scenario is not sufficient.

If continued exploration produces only weaker, more speculative, or materially less relevant candidates than those already investigated, it is acceptable to conclude that no additional justified findings remain in that area.

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

Check every applicable area below. Skip areas with no matching surface.

Investigate representative and materially different risk paths. Correlate evidence across files where necessary.

Do not stop after the first finding when additional realistic and materially distinct risks remain, but do not continue exploring solely to produce additional findings.

Stop exploring an area when additional investigation yields only candidates that are substantially weaker, more speculative, less likely, or less impactful than the established finding threshold.

Repeatedly analyzing equivalent variants of the same risk is not additional coverage.

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
4. Absence of visible evidence is not by itself evidence of a defect. If a control, validation, transaction, retry, configuration, runtime guarantee, or external behavior is not visible in the reviewed code, do not assume either its presence or absence. Report a finding only when the reviewed code itself creates a realistic risk. Use `needs-verification` only when there is concrete local evidence of a likely problem and one specific missing fact prevents confirmation.
5. Validate every candidate against the finding threshold before reporting it. A candidate that lacks sufficient evidence, realistic reachability, material impact, or a plausible risk path must be dismissed rather than retained as a weak finding.
6. Do not report multiple increasingly hypothetical variants of the same underlying concern. Consolidate them or dismiss variants that do not materially change the risk.
7. Do not treat theoretical possibility, defensive-programming opportunities, stylistic improvements, or general best-practice deviations as findings unless the repository evidence shows a concrete engineering impact.
8. Scanner/analyzer output is supporting evidence only. Promote it only when local code evidence confirms relevance.
9. Consolidate repeated instances of the same problem into one finding with representative examples.
10. Redact secrets or sensitive values if encountered. Report the location and type, not the value.
11. Do not edit code, configuration, formatting, dependencies, or generated files unless the user separately asks.

## Evidence Gate

Every candidate identified during hunting must be resolved as `confirmed`, `needs-verification`, or `dismissed`.

The burden of proof is on the finding. Do not report a candidate merely because it cannot be disproved.

### Finding (confirmed)

Use `confirmed` only when local repository evidence establishes all of the following:

1. **Concrete condition or trigger**
   There is a specific code path, state, input, configuration, change scenario, or runtime condition that can plausibly occur.
2. **Concrete faulty or harmful behavior**
   The code shows what goes wrong, not merely what might theoretically go wrong.
3. **Material engineering impact**
   The behavior has a meaningful correctness, reliability, performance, maintainability, testability, operational, or delivery impact.
4. **Causal connection**
   The reported location is materially responsible for the problem.
5. **Realistic risk path**
   The finding does not depend on a contrived chain of independently unlikely assumptions.

If any of these elements is missing, do not mark the finding as `confirmed`.

### Finding (needs-verification)

Use `needs-verification` only when all of the following are true:

- local evidence strongly suggests a realistic problem;
- a specific missing fact prevents confirmation;
- that missing fact can be stated explicitly;
- obtaining that fact could realistically change the result to either `confirmed` or `dismissed`.

Do not use `needs-verification` as a holding category for speculative ideas.

### Dismissed

Dismiss a candidate when any of the following applies:

- the code disproves it;
- the required trigger is not realistically reachable;
- the impact is negligible or purely stylistic;
- the scenario depends on excessive speculation;
- the candidate is only a generic best-practice recommendation;
- the concern duplicates an existing finding without materially different impact or remediation;
- evidence is insufficient to cross the finding threshold.

A dismissed candidate is a successful validation outcome and is preferable to a weak finding.

## Severity

- `critical`: likely production outage, data corruption/loss, systemic failure of core flows, or architecture issue blocking safe evolution.
- `high`: serious correctness risk, important performance/scalability risk, fragile critical path, missing tests around high-impact behavior, severe coupling, or realistic operational failure.
- `medium`: meaningful bounded quality, maintainability, testability, performance, or operational problem.
- `low`: a concrete, evidence-backed engineering problem with limited blast radius or impact, but with a realistic negative consequence if left unchanged. Do not use `low` for stylistic cleanup, optional refactoring, defensive-programming suggestions, general best practices, or improvements without a demonstrated repository-specific risk.

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
