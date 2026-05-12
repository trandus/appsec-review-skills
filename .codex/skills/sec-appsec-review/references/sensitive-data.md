# Sensitive Data

## Review Checks

- Data classes: PII, payment data, tokens, secrets, health data, user identifiers, private files, moderation data, and support/admin notes.
- Flow: input -> validation -> storage -> logs -> telemetry -> cache -> export -> deletion -> external integrations.
- Retention, account/data deletion, read permissions, download/export, backups, blob prefixes, and caching.
- Whether data is minimized and kept out of locations that are less protected than the source.
- Encryption, signing, hashing, masking, and key-management boundaries where the repo implements or configures them.

## Evidence Signals

- DTOs, database schema, blob/storage paths, logs, telemetry calls, serializers, export/import code, and deletion services.
- Access checks before reading, updating, exporting, or deleting user-owned data.
- Tests for ownership, deletion completeness, redaction, masking, retention, and export scope.
- Configuration showing storage locations, telemetry processors, cache settings, and external processors.

## Common Findings

- Sensitive data is exposed to other users, broader roles, logs, telemetry, errors, exports, or client bundles.
- Data deletion misses dependent tables, blobs, indexes, caches, or integration-side artifacts that local code owns.
- Tokens, secrets, or identifiers are stored or rendered in a form that exceeds the business need.
- Sensitive data is cached or retained without clear scope, expiration, or owner controls.

## Offline Boundaries

- Do not assert external processor, cloud storage, backup, or telemetry retention behavior without local configuration or official refreshed documentation.
- If current SDK, cloud, payment, identity, or telemetry behavior determines the risk, record a `Follow-up`.
- Without runtime data samples, classify data-flow risks from code paths and schemas, not assumptions about live contents.
- Legal/privacy compliance conclusions beyond code evidence should be `Follow-up`, not `Finding`.

## Sources

See repository-root `SEC-README.md` for source links.
