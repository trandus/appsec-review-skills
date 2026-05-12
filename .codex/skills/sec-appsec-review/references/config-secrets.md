# Config/secrets

## Review Checks

- Configuration files, environment files, sample config, deployment manifests, Docker/Kubernetes files, and CI workflows.
- Secrets, connection strings, API keys, tokens, certificates, private keys, passwords, signing keys, and webhook secrets.
- Debug flags, verbose errors, permissive CORS, insecure cookies, missing HTTPS, dev endpoints, and unsafe diagnostics.
- Separation between dev, test, staging, and production configuration.
- Telemetry and logging for sensitive-data leakage.
- Secret-source precedence and whether local sample values can accidentally override safer environment values.

## Evidence Signals

- Hardcoded values in tracked files, generated config, scripts, CI files, IaC, launch settings, or documentation examples.
- Configuration keys that enable insecure behavior outside development-only branches.
- Secret-loading code, configuration providers, environment variable names, and deployment settings.
- Tests or startup validation that reject missing or unsafe production configuration.

## Common Findings

- Real or plausible production secret committed to the repo.
- Debug, verbose error, permissive CORS, insecure cookie, or HTTP-only exception is active outside development.
- Sample config encourages unsafe deployment or uses names that can collide with production keys.
- Secret, token, connection string, or sensitive payload is logged or exposed through diagnostics.

## Offline Boundaries

- A secret-looking value is a finding only when local evidence shows it is live, production-like, or materially risky; otherwise use `Observation` or `Follow-up`.
- Do not assume cloud secret stores, managed identity, CI masking, or platform configuration unless local IaC/config proves it.
- If current SDK, CLI, cloud, or framework configuration precedence is decisive, record a `Follow-up` to check official documentation.
- Without access to deployed environment variables or secret stores, report missing validation and risky defaults, not unproven deployment exposure.

## Sources

See repository-root `SEC-README.md` for source links.
