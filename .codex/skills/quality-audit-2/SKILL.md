---
name: quality-audit-2
description: "Application quality audit for repository review: architecture, source code quality, bug risks, performance, tests, error handling, logging, quick wins, refactoring areas, technical priorities, technical debt, and Jira-import JSON output. Use for local quality/engineering-health audits of any application stack."
disable-model-invocation: true
---

# quality-audit-2

Run a local quality code review focused on identifying real, material, evidence-backed engineering problems within the reviewed scope. The goal is not to maximize the number of findings. A scan with no justified findings is a valid outcome.

Keep the same evidence and practical-impact threshold for findings throughout the audit, even after obvious problems have been found or fixed. Assign severity separately.

The goal is broad evidence-backed discovery, not a fixed checklist. Use the areas below as directions to hunt. Follow the repository shape, architecture, conventions, and domain flows. Explore additional realistic code paths when they can reveal materially different risks, but do not manufacture findings from increasingly speculative, contrived, or extremely unlikely scenarios.

A candidate should become a finding only when there is concrete local evidence of a realistic defect, quality risk, maintainability problem, performance issue, testability problem, or operational failure mode. The mere possibility of constructing a hypothetical failure scenario is not sufficient.

This skill covers repository quality review: architecture, source quality, bug/antipattern risks, performance, test quality, error handling, logging, technical summary, improvement recommendations, technical priorities, refactoring areas, and technical debt estimate.

## Defaults

- Report prose, finding titles, and JSON descriptions: Polish with diacritics, unless the user provides `Report Language: <language>`. Keep required headings, field names, schema keys, and enum values as specified below.
- Markdown output file: `./quality-audits/quality-audit-<YYYY-MM-DD-HHmm>.md` in the reviewed repository root, unless the user provides another path.
- JSON output file: `./quality-audits/quality-audit-<YYYY-MM-DD-HHmm>.json` next to the Markdown report, unless the user disables JSON output or provides another path.
- Normal mode: offline, local repository only, no internet, no GitHub, no SaaS, no runtime access, no external scanners, no fixes, and no package upgrades unless the user separately asks.
- Do not perform a security, dependency-vulnerability, or compliance audit unless the user asks.
- Do not run builds (ie. `dotnet build`, `npm run build`, ...). Do not run commands whose main purpose is to compile, package, publish, container-build, restore remote dependencies, or launch the application.
- Prefer read-only inspection and existing local evidence. Tests, linters, or analyzers may be read from existing output files; run them only if the user explicitly asks.

Chat reply: name only the files actually written, then give the counts in this form:

`<generated file name(s)> - Findings: N (M confirmed, K needs-verification), Dismissed: D, Technical debt: low|medium|high`

## Internal Recon

Start with a short internal repository profile to guide hunting. Summarize relevant facts in `Repository Context`:

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

Continue checking materially different paths in an applicable area even if recent candidates were weak. Stop pursuing a candidate after tracing its relevant path when further inspection adds no evidence or distinct risk mechanism.

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

Swallowed or overbroad exceptions, inconsistent error contracts, missing diagnostics in important flows, noisy or misleading logs, missing correlation/context, weak retry/failure visibility, fragile configuration, environment drift, unclear health/operational behavior, and deployment/runtime assumptions that can break quietly.

### Maintainability and Refactoring

Areas where future changes are expensive or risky: high-complexity modules, repeated concepts, inconsistent conventions, unclear names, domain leakage, poor cohesion, weak seams for tests, and refactoring opportunities that reduce real risk.

### Dependencies

Mention dependencies only when local evidence shows quality impact: unsupported/runtime compatibility risk, upgrade blockage, duplicate stacks, brittle generated clients, build/runtime fragility, or maintainability cost.

## Rules

1. Reference real local evidence: file path and line, symbol, route, config key, test, or documented convention. Do not invent project conventions or assume missing code exists elsewhere.
2. No generic advice. A recommendation must point to a concrete repository problem. Do not recommend rewrites when targeted refactoring is enough.
3. Do not report style preferences, defensive-programming suggestions, or general best-practice deviations without concrete repository-specific correctness, performance, maintainability, testability, operational, or delivery impact.
4. Absence in one file is not proof that a safeguard is absent from the flow. Before reporting a missing control, trace the relevant entry point, local callers, validation, configuration, and affected operation. Its absence from that examined path can support a finding when the trigger and harmful outcome are concrete; do not assume facts about unreviewed or external controls. Use `needs-verification` only when one specific missing fact prevents confirmation.
5. Validate every candidate against the finding threshold before reporting it. A candidate that lacks sufficient evidence, realistic reachability, material impact, or a plausible risk path must be dismissed rather than retained as a weak finding.
6. Consolidate repeated instances or variants of the same problem into one finding with representative examples; dismiss variants without materially distinct risk or remediation.
7. Scanner/analyzer/IDE output is supporting evidence only. Promote it only when local repository evidence confirms a concrete impact.
8. Redact secrets or sensitive values if encountered. Report the location and type, not the value.
9. Do not edit code, configuration, formatting, dependencies, or generated files unless the user separately asks.

## Evidence Gate

Resolve every investigated candidate internally as `confirmed`, `needs-verification`, or `dismissed`.

The burden of proof is on the finding. Do not report a candidate merely because it cannot be disproved.

### Finding (confirmed)

Use `confirmed` only when local repository evidence establishes all of the following:

1. **Concrete condition or trigger**
   There is a specific code path, state, input, configuration, change scenario, or runtime condition that can plausibly occur.
2. **Concrete faulty or harmful behavior**
   The code shows a specific faulty behavior or concrete mechanism that harms correctness, performance, change safety, testability, or operations; a production failure need not already have occurred.
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

State the missing fact and how to check it in `Evidence` or `Recommendation`.

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
|----------|----------|-----------|
| Critical | 0 | 0 |
| High | 0 | 0 |
| Medium | 0 | 0 |
| Low | 0 | 0 |

Overall quality assessment.

## Findings

Confirmed findings first, then needs-verification.

## Dismissed

Include only dismissed candidates useful for triage; D counts only the entries shown here.
```

## JSON Output

If JSON output is enabled, generate one parseable `.json` file for Jira import only after the Markdown report is complete; do not spend hunting time shaping it.

The JSON is an issue import payload, not an audit report. Its shape is closed: use exactly the keys shown below and no extra metadata, summaries, repository context, verification data, `findings`, or `dismissed` sections.

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
5. `description` uses the format required by the target Jira importer (default: readable plain text with field headings) and carries the finding fields from the report: Severity, Confidence, Area, Category, Location, Evidence, Risk/Impact, Recommendation, Effort. Omit missing fields; do not invent details.
6. Before writing the file, check that root keys are exactly `common` and `issues`; `common` has only `labels`; each issue has only `summary`, `description`, and `labels`.
7. Verify that `N = M + K`, the severity table totals `N` findings and `M` confirmed; `D` equals the number of listed dismissals; and, when JSON is enabled, its issue count equals `N`.

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
  2. Faulty behavior or harmful quality mechanism
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
- Why dismissed: specific reason for dismissal; cite local evidence when available, and do not invent evidence when the available evidence is insufficient
```