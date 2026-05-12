---
name: sec-repo-recon
description: Portable repository reconnaissance for local AppSec review. Use when you need to identify repo structure, stack, entry points, configuration, dependencies, auth, storage, and optional host-repository instructions without assuming a specific project layout.
---

# sec-repo-recon

Map the repository as an optional adaptation layer for review. Missing local instructions, project maps, or skills do not block the work.

## Workflow

1. Identify the repository root and sandbox constraints.
2. Detect local orientation material if it exists: agent instructions, repository-root `SEC-README.md`, README files, architecture docs, project maps, local skills, code review rules, build/test commands, and file-search conventions. Mark them as optional host-repository adaptation.
3. Map the structure: backend, frontend, test, and infrastructure projects; scripts; configuration; and documentation.
4. Identify the stack and manifests: project files, lockfiles, package managers, frameworks, versions, and generated artifacts.
5. Identify optional local security tools only as available inputs, not required steps: `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, Semgrep, CodeQL, and any existing local reports. Do not run them unless the user explicitly requests or accepts their use.
6. Find entry points: routing, controllers, minimal APIs, Razor Pages, middleware, webhooks, uploads, frontend routes, and serverless functions.
7. Find auth and boundaries: auth middleware, policies, roles/claims, guards, sessions, tokens, cookies, tenant ownership, and user ownership.
8. Find storage and integrations: databases, blob/file storage, queues, external services, payments, email, and telemetry.
9. Find configuration and potential secrets: environment files, appsettings, secret placeholders, connection strings, CORS, cookies, headers, and debug flags.
10. Return a short repo model for the review.

## Output Format

Return:

- **Repo model**: application type, main projects, stack, and entry points.
- **Local adaptation**: local instructions found and how they affect the review. If none exist, write `no local orientation material found`.
- **Security surfaces**: auth/authz, input/data, backend, frontend, config/secrets, dependencies, sensitive data, logging, abuse/rate limiting, destructive operations.
- **Optional tool inputs**: available local dependency/security tool reports or commands, whether the user authorized their use, and any limitations such as internet, login, database, SDK, or missing configuration requirements.
- **Review priorities**: 3-7 highest-risk areas with rationale.
- **Unknowns**: items that need manual confirmation.

## Portability

Do not assume specific file names or a specific repository structure. If local instructions exist, respect them as host-project rules. If they do not exist, continue recon from files, manifests, and code.
