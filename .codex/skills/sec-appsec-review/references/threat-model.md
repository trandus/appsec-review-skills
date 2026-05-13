# Threat model

## Review Checks

- List assets: accounts, user data, tokens, secrets, money, files, privileged actions, and external integrations.
- List attacker positions: anonymous user, signed-in user, user with another user's identifier, operator, automated client, and compromised dependency.
- Mark trust boundaries: browser/server, public/private endpoint, API/background worker, database/storage, third-party API, package feed, and CI/CD.
- Connect entry points to assets and identify the shortest credible risk paths.
- Prioritize flows with sensitive data, destructive operations, expensive actions, ownership boundaries, or cross-tenant access.

## Evidence Signals

- Routes, controllers, pages, jobs, commands, or handlers that expose the prioritized flows.
- Data models, storage paths, configuration keys, claims, policies, and integration clients showing asset ownership and trust boundaries.
- Tests or documentation that define expected access rules, deletion behavior, retention, or operational limits.
- Missing server-side checks after tracing the flow from entry point to asset.

## Common Findings

- High-value asset reachable through a public or weakly protected path.
- Trust boundary crossed without validation, authorization, integrity check, or logging.
- Destructive or expensive workflow lacks abuse controls or ownership enforcement.
- Security decision depends on client-side state, hidden UI, or untrusted metadata.

## Offline Boundaries

- Do not claim a current framework, SDK, CLI, cloud, or SaaS behavior unless it is documented locally or proven in code.
- If current behavior matters and local references are insufficient, record a `Follow-up` for a separate reference-refresh task.
- Without runtime access, scanners, or environment configuration, keep deployment-specific exposure as `Observation` or `Follow-up` unless repo evidence proves it.
- Threat modeling creates review priorities; it does not create a `Finding` without code evidence or a traced missing control.

## Sources

See repository-root `SEC-README.md` for source links.
