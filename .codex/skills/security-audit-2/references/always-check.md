# Always-Check Areas

Use this file only as a tiny reminder of obvious, high-yield checks that are easy to miss while looking for deeper issues. It is not a vulnerability catalog and must not replace `risk-baseline.md`. Pick only areas that match the audited technology, scope, and exposed surface; report only evidence-backed issues.

## Access Control And Workflows

- Missing auth on public routes, APIs, files, admin/debug panels.
- Missing owner, tenant, organization, role, approval, state-transition checks, IDOR/BOLA

## Unsafe Input To Sinks

- SQL/NoSQL/LDAP/query, command, template/expression, path traversal, unsafe redirect.
- SSRF, unsafe file import/export/archive handling, attacker-controlled outbound URLs.

## Browser And Rendering

- Reflected, stored, or DOM XSS through raw HTML, Markdown/rich text, or missing encoding/sanitization.
- CSRF, unsafe CORS, and weak sensitive-cookie flags on browser-auth flows.

## Secrets And Sensitive Data

- Credentials, API keys, tokens, connection strings, private keys, weak defaults, or production-like sample values.
- Secrets, PII, auth headers, request bodies, stack traces in logs/errors/responses.
- Production-like `http://` endpoints used with credentials, tokens, cookies, sensitive data, or Windows/NTLM auth.

## Public Debug Surfaces

- Swagger/OpenAPI/ReDoc exposed outside development.
- Debug, diagnostics, health, metrics, logs, admin/dev endpoints without clear protection.

## Proof Rule

- Do not report a finding from this file without a concrete local evidence path and realistic abuse scenario.
