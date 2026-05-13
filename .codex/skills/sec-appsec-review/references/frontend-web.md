# Frontend web

## Review Checks

- XSS: binding HTML, unsafe DOM APIs, `innerHTML`, template injection, URL/script/style sinks, and raw HTML helpers.
- Framework sanitization and explicit bypass APIs, such as Angular `DomSanitizer.bypassSecurityTrust*`.
- Token storage: localStorage, sessionStorage, cookies, and related XSS/CSRF tradeoffs.
- Client-side authorization: guards and hidden UI must not replace server-side controls.
- Secrets and configuration shipped in the bundle.
- CORS assumptions and frontend dependency usage.
- CSP, Trusted Types, iframe/script/resource URLs, third-party scripts, and generated or user-authored content rendering.

## Evidence Signals

- Templates, components, Razor views, scripts, route guards, state stores, generated bundles, and config files.
- Data flow from user-controlled or server-controlled values to DOM, HTML, JavaScript, CSS, URL, iframe, script, or resource sinks.
- Calls to sanitizer bypass APIs, raw HTML helpers, direct DOM APIs, third-party renderers, Markdown renderers, or template compilers.
- Backend checks showing whether the server trusts frontend decisions.

## Common Findings

- User-controlled content reaches unsafe DOM or template sinks without sanitizer and context-aware encoding.
- Sanitizer bypass APIs are used on data that is not clearly trusted at the source.
- Tokens or secrets are stored where XSS or bundle inspection can expose them without compensating controls.
- Access control exists only in frontend routes, hidden UI, or client-side state.

## Offline Boundaries

- Do not guess current framework sanitizer, CSP, Trusted Types, browser, or bundler behavior when local references are insufficient.
- If Angular, another framework, a SDK, a CLI, or browser behavior is decisive and not proven locally, record a `Follow-up` for a separate reference-refresh task.
- Without built assets or runtime inspection, bundle exposure and CSP effectiveness may need `Follow-up`.
- A frontend issue becomes an access-control finding only when backend trust or missing server-side enforcement is traced.

## Sources

See repository-root `SEC-README.md` for source links.
