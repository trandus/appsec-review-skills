# Input/data

## Review Checks

- Model binding, validation, normalization, and length limits.
- Trace untrusted input from source to sink for SQL/NoSQL/LDAP injection, command injection, template injection, SSRF, path traversal, unsafe redirects, and deserialization.
- File upload/download/export/import/archive extraction: type, size, storage path, scanning, public access, object authorization, archive paths, and attacker-controlled names.
- XSS/template injection, especially when input returns to HTML, Markdown, JavaScript, CSS, URL, rich-text, or server/client template contexts.
- Business logic abuse: quantities, prices, workflow states, retries, and automation.
- Encoding at the output context, not only validation at the input edge.
- Server-side validation for values also constrained by frontend controls.

## Evidence Signals

- Binding models, validators, parsing/normalization code, route constraints, upload handlers, and request DTOs.
- Data flow from input source to database query, shell/process call, file path, URL fetch, redirect, HTML/JS/CSS/URL sink, or deserializer.
- Template renderers, Markdown/rich-text renderers, raw HTML helpers, DOM sinks, URL builders, archive extraction code, and file response/download handlers.
- Use of parameterized queries, safe framework APIs, allowlists, canonicalization, and context-aware encoding.
- Tests for malformed, boundary, encoded, duplicate, and cross-field inputs.

## Common Findings

- User-controlled input reaches SQL, command, path, URL, redirect, deserialization, or DOM/template sink without an appropriate control.
- Stored or reflected XSS through HTML, Markdown, rich text, JavaScript, CSS, URL, or template contexts.
- Validation exists only in the browser or only checks presence while dangerous syntax remains accepted.
- File upload/download/export/import/archive flow accepts dangerous content, public paths, path traversal, oversized files, attacker-controlled names, or missing object authorization.
- Business constraints can be bypassed by changing hidden fields, repeated requests, or inconsistent state transitions.

## Offline Boundaries

- If a framework parser, sanitizer, serializer, or validation library's current behavior is decisive and not locally documented, record a `Follow-up` for official documentation.
- Do not classify a sink as vulnerable if local code shows a safe API and no bypass path.
- Without runtime payload testing, report only flows proven by code or missing-control tracing.
- Scanner findings supplied by the user need local confirmation before becoming a `Finding`.

## Sources

See repository-root `SEC-README.md` for source links.
