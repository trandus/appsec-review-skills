# Auth/authz

## Review Checks

- Verify that every protected entry point enforces authentication server-side.
- Check object-level and function-level authorization, not only role checks or hidden UI.
- Tie resource identifiers to an owner, tenant, or explicit permission before use.
- Check object-level authorization for single-object routes, list/search/filter routes, bulk operations, nested resource IDs, file IDs, export/import, and destructive actions.
- Review sessions, cookies, tokens, claims, policies, route guards, logout, password reset, invite/magic link, MFA, credential reset flows, and privilege changes.
- Check token revocation, stale sessions, privilege downgrade, admin-only flows, forced browsing, and identity-provider callback handling when locally visible.
- Prioritize administrative, destructive, expensive, and cross-user operations.
- Check negative tests for anonymous, authenticated-but-wrong-user, wrong-role, cross-tenant, stale-session, file-id swap, bulk object access, and replay cases.

## Evidence Signals

- Authentication/authorization middleware, endpoint attributes, policy registration, scheme configuration, and claims mapping.
- Resource loading code that constrains by current user, tenant, organization, role, or explicit permission.
- Query filters, repository/service methods, and policy checks that constrain both list results and individual object reads/writes.
- Tests or fixtures demonstrating denied access for other users and roles.
- Frontend guards paired with backend enforcement rather than replacing it.

## Common Findings

- BOLA/IDOR: a user can read or modify another user's resource by changing an identifier.
- Bulk, list, search, filter, nested-resource, file, export, or import endpoint returns or changes objects outside the caller's tenant/owner boundary.
- Missing server-side policy on an endpoint or operation.
- Authorization relies only on a frontend guard, route check, or hidden button.
- Claims, roles, or tenant identifiers are trusted without server-side validation against the target resource.
- Logout, reset, or privilege-change flows leave active sessions or tokens usable when the application expects revocation.

## Offline Boundaries

- Do not claim identity-provider, token lifetime, claim issuance, or cookie behavior unless local configuration or official refreshed documentation supports it.
- If the behavior of an auth library, SDK, cloud identity provider, or framework policy system is decisive and not proven locally, create a `Follow-up` for a separate reference-refresh task.
- Without runtime session traces, keep cookie/token transport assumptions as `Observation` unless code/config proves the issue.
- Missing negative tests are supporting evidence, not a finding by themselves, unless the implementation path confirms the missing control.

## Sources

See repository-root `SEC-README.md` for source links.
