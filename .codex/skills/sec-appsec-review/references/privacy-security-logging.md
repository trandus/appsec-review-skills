# Privacy/security logging

## Review Checks

- Security events are logged: sign-in, sign-out, access denials, permission changes, destructive operations, abuse/rate-limiting events, and sensitive export/import.
- Logs do not contain secrets, tokens, cookies, full payment data, sensitive payloads, or excessive PII.
- Errors do not disclose stack traces, configuration, connection strings, secrets, or user data outside development-only contexts.
- Telemetry, traces, metrics, and audit logs have a clear purpose and limited data scope.
- Log integrity, correlation identifiers, retention knobs, and alert-worthy events are present where the repo controls them.

## Evidence Signals

- Logging calls, exception handlers, telemetry initializers/processors, audit-event tables, filters, middleware, and operational dashboards/config.
- Structured log properties that include request bodies, claims, headers, cookies, tokens, identifiers, or exception details.
- Tests or snapshots asserting redaction, audit-event creation, and development-only error details.
- Configuration that differs by environment for logging level, telemetry sinks, sampling, and diagnostics.

## Common Findings

- Secrets, tokens, cookies, payment data, or sensitive payloads are written to logs or telemetry.
- Important security events are not logged where local requirements or code paths require auditability.
- Production error handling reveals stack traces, configuration, or sensitive user data.
- Audit logs can be modified or deleted through ordinary user-controlled flows.

## Offline Boundaries

- Without access to deployed log sinks, retention policies, alert rules, or telemetry backend, report only local logging behavior and missing local controls.
- If logging framework, SDK, cloud telemetry, or hosting behavior is decisive and not proven locally, record a `Follow-up` for a separate reference-refresh task or environment validation.
- Lack of monitoring alerts is usually a `Follow-up` unless the repo explicitly defines required alerts and omits them.
- Do not infer privacy-law compliance from code review alone.

## Sources

See repository-root `SEC-README.md` for source links.
