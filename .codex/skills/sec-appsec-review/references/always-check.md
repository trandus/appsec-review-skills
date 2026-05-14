# Always-Check Areas

Use this file only as a tiny reminder of obvious, high-yield checks that are easy to miss while looking for deeper issues. It is not a vulnerability catalog and must not replace `risk-baseline.md`. Pick only areas that exist in the audited scope and report only evidence-backed issues.

## Access Control

- Missing auth on public routes, APIs, files, admin/debug panels.
- Missing owner, tenant, organization, or role check on object access.

## Injections

- SQL/NoSQL/LDAP/query injection.
- Command, template/expression, path traversal, unsafe redirect.

## XSS

- Reflected, stored, DOM XSS.
- Raw HTML, unsafe Markdown/rich text, missing output encoding/sanitization.

## Secrets And Passwords

- Passwords, API keys, tokens, connection strings, private keys in repo/config/docs/tests/logs.
- Weak default secrets or sample values that could work in real deployments.

## Public Debug Surfaces

- Swagger/OpenAPI/ReDoc exposed outside development.
- Debug, diagnostics, health, metrics, logs, admin/dev endpoints without clear protection.

## Browser Basics

- CSRF on state-changing browser-auth flows.
- Unsafe CORS and missing Secure/HttpOnly/SameSite on sensitive cookies.

## Files

- Upload/download without authz.
- Path traversal, public storage, unsafe archive extraction.

## Sensitive Data Leakage

- Secrets, tokens, PII, auth headers, request bodies, stack traces in logs/errors/responses.

## Proof Rule

- Do not report a finding from this file without a concrete local evidence path and realistic abuse scenario.
