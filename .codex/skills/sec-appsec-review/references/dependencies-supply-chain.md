# Dependencies/supply chain

## Review Checks

- Inventory manifests and lockfiles: NuGet, npm, pnpm/yarn, Docker images, GitHub Actions, build tools, and language-specific package files.
- Check for missing lockfiles where the ecosystem and project workflow expect deterministic restore.
- Look for broad or floating version ranges, unpinned tool versions, manually downloaded binaries, vendored code, and abandoned packages.
- Review package scripts, build hooks, postinstall steps, generators, and CI commands that execute dependency-provided code.
- Inspect package feed sources, private package names, registry precedence, source mapping, and dependency confusion risk.
- Use user-provided or explicitly authorized local outputs from `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, NuGet audit, CodeQL, Semgrep, or secret scans as review input.
- Check whether vulnerability, SAST, SCA, and secret-scan outputs are current enough and tied to the same commit or dependency graph.
- If the user asks to run a tool, report prerequisites and limitations before relying on it: internet or registry access, vulnerability database availability, login, CodeQL database creation, build requirements, SDK availability, Semgrep rules, or missing configuration.

## Evidence Signals

- `package.json`, lockfiles, `.npmrc`, NuGet config, `Directory.Packages.props`, project files, workflow files, Dockerfiles, tool manifests, and package source mapping.
- Version ranges such as floating, wildcard, prerelease, or broad semver constraints on runtime or build-time dependencies.
- Lifecycle scripts, build scripts, external install commands, curl/download steps, unsigned binaries, custom registries, and private package names.
- Locally supplied audit/SAST/SCA/secret-scan reports that include package name, version, advisory or rule id, path, timestamp, and commit or dependency graph context.
- Explicit user authorization to run local tooling, the exact command used, whether it required network access, and any failure or partial-result conditions.

## Common Findings

- Missing lockfile or deterministic restore control for an application that relies on package restore during build/deploy.
- Broad version ranges or unpinned tools allow unreviewed dependency changes in sensitive build/runtime paths.
- Package scripts or build hooks execute untrusted dependency code without a clear need or review gate.
- Private package names can be resolved from a public feed before the intended private feed.
- Tool output identifies a vulnerable package, SAST issue, or secret exposure and local code, manifests, lockfiles, configuration, or real dependency usage confirm the affected package/path is relevant.

## Offline Boundaries

- Offline review does not confirm current CVEs, advisories, exploitability, package reputation, or latest safe versions without local tool output or access to a current vulnerability database.
- Current dependency vulnerabilities without local evidence belong in `Follow-up`, not `Finding`.
- Treat `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, NuGet audit, CodeQL, Semgrep, and secret-scan reports as input that still needs local confirmation of path, version, reachability, and relevance.
- If npm, NuGet, CodeQL, Semgrep, registry, SDK, CLI, or cloud behavior is decisive and local references are insufficient, record a `Follow-up` for a separate reference-refresh task.
- Do not run scanners automatically during normal review unless the user explicitly requests or accepts it and host-repository rules allow it.
- If a tool needs internet access, authentication, a vulnerability database, a CodeQL database, a successful build, or unavailable configuration, state the limitation and report unresolved items as `Observation` or `Follow-up`.

## Sources

See repository-root `SEC-README.md` for source links.
