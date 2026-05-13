# sec-* AppSec review

`sec-*` to przenośny zestaw czterech skilli do lokalnego AppSec code review. Zwykłe review działa offline po skopiowaniu do repozytorium: bez internetu, Context7, GitHuba, SaaS i zewnętrznych skanerów.

## Skille

- `sec-appsec-review`: orkiestrator review, wybór scope, `Review Depth`, `ASVS Level`, flow i raport końcowy.
- `sec-repo-recon`: rozpoznanie struktury repo, stacku, entry pointów, konfiguracji, zależności i opcjonalnych lokalnych zasad hostującego repo.
- `sec-asvs-review`: lokalny lookup OWASP ASVS, poziomy `L1`, `L2`, `L3`, `ASVS Mapping` i rozróżnienie ASVS od OWASP Top 10.
- `sec-reporting`: format raportu oraz rozdzielenie `Findings`, `Observations` i `Follow-up`.

## Szybki Start

1. Skopiuj foldery `.codex/skills/sec-*` oraz `SEC-README.md` do głównego folderu repozytorium.
2. Uruchom jeden z trzech promptów poniżej.
3. Najpierw rozpoznaj lokalne instrukcje hostującego repo, jeśli istnieją: instrukcje agentów, README, mapy projektu, dokumentację architektury, lokalne skille, zasady wyszukiwania plików i komendy.
4. Domyślny wybór dla zwykłego review to `standard + ASVS L2`.

## Praca Offline

Normalne review korzysta z lokalnego repo, lokalnych instrukcji, `SEC-README.md`, skilli `sec-*`, referencji pod `.codex/skills/sec-appsec-review/references/` i lokalnego datasetu ASVS. Pakiet nie uruchamia automatycznie `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, CodeQL ani Semgrep.

Wyniki narzędzi mogą być przekazane ręcznie albo użyte lokalnie na wyraźne żądanie jako materiał pomocniczy, ale `Finding` nadal wymaga dowodu w kodzie albo prześledzonego braku kontroli.

## ASVS Lookup Offline

`sec-asvs-review` ma lokalny dataset `references/asvs-5.0.0-local.json` i helper:

```powershell
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query authorization
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query injection
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query csrf
```

ASVS jest głównym standardem wymagań i mapowania. OWASP Top 10 jest tylko pomocniczą kategorią ryzyka, np. `A01 Broken Access Control`.

## Format Raportu

Raport po review zawsze ma być napisany po polsku. Używaj normalnego, czytelnego języka polskiego w opisach ryzyka, dowodów, wpływu, rekomendacji i testów. Angielskie określenia zostawiaj tylko wtedy, gdy są utrwalonymi terminami domenowymi bez rozsądnego polskiego odpowiednika albo jednoznacznymi nazwami standardów, klas podatności, pól raportu, bibliotek, narzędzi, nagłówków, konfiguracji lub API.

Unikaj przypadkowego mieszania polskiego i angielskiego w jednym zdaniu. Jeśli polski odpowiednik jest naturalny, użyj polskiego, np. `dowód`, `wpływ`, `ścieżka ryzyka`, `zalecenie`, `test regresyjny`, `uprawnienie`, `właściciel zasobu`. Zachowuj krótkie terminy techniczne tam, gdzie poprawiają precyzję, np. `XSS`, `SSRF`, `CSRF`, `IDOR/BOLA`, `JWT`, `OAuth/OIDC`, `claim`, `tenant`, `endpoint`, `cookie`, `lockfile`.

Każdy raport musi zawierać sekcje `Findings`, `Observations` i `Follow-up`, jeśli te kategorie realnie występują. Jeśli kategoria nie ma wyników, napisz to jawnie, np. `Findings: brak potwierdzonych findingów`.

- `Finding`: potwierdzony problem z `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnieniem braku mapowania oraz opcjonalnym `OWASP Top 10 Category`.
- `Observation`: obserwacja projektowa, osłabiona kontrola, sygnał narzędziowy albo hipoteza bez wystarczającego dowodu.
- `Follow-up`: pytanie, walidacja narzędziowa, potrzeba aktualnej dokumentacji, niedostępny runtime/login/baza/konfiguracja albo osobne sprawdzenie.

Review nie implementuje zmian. Dla findingów zwraca `Remediation` oraz `Regression Test`.

## Prompty

### 1. Najważniejszy Prompt: Całe Repo

**Kiedy użyć**

- Gdy chcesz wykonać główny, praktyczny przegląd bezpieczeństwa całego repo.
- Gdy priorytetem są exploitable paths, OWASP Top 10 i realne luki w web/API.

**Zakres**

- `Tier 1`: access control, object-level i function-level authorization, auth/session lifecycle, injection, XSS/template injection, unsafe file operations.
- `Tier 2`: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging.
- `Tier 3`: dependencies/supply-chain, crypto/JWT/key handling, rate limiting, business logic abuse.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do szerokiego AppSec review całego repo z priorytetem na OWASP Top 10, ASVS i najbardziej exploitable ścieżki ataku.

Scope: całe repo. Najpierw użyj `sec-repo-recon`, żeby rozpoznać lokalne instrukcje hostującego repo, architekturę, aplikacje, entry pointy, route groups, modele danych, storage, integracje, konfigurację, zależności i miejsca, gdzie przepływają identyfikatory zasobów.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów.

Priorytety:
- Tier 1: access control, server-side object-level authorization, function-level authorization, auth/session lifecycle, injection, XSS/template injection i unsafe file operations.
- Tier 2: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging.
- Tier 3: dependencies/supply-chain, crypto/JWT/key handling, rate limiting i business logic abuse.

Wymagania:
- Dla każdego endpointu z identyfikatorem zasobu sprawdź, czy backend przed użyciem identyfikatora wiąże obiekt z ownerem, tenantem, organizacją albo konkretnym uprawnieniem.
- Sprawdź warianty object-level authorization dla single object, list/search/filter, bulk operations, nested resource IDs, file IDs, export/import i destructive actions.
- Priorytetyzuj cross-user, cross-tenant, file-id swap, destructive operations oraz wariant authenticated-but-wrong-user.
- Dla injection i XSS wykonuj source-to-sink tracing: SQL/NoSQL/LDAP, command injection, template injection, SSRF, path traversal, unsafe redirect, deserialization oraz HTML/Markdown/JS/CSS/URL sinks.
- Dla auth/session sprawdź reset hasła, invite/magic link, MFA, logout, token revocation, stale sessions, privilege change/downgrade, admin-only flows i forced browsing.
- Dla operacji wysokiego wpływu sprawdź CSRF/antiforgery tam gdzie ma zastosowanie, replay, TOCTOU, idempotency, audit logging i cleanup zależności.
- Nie implementuj poprawek. `Finding` raportuj tylko z dowodem w kodzie albo prześledzonym brakiem wymaganej kontroli. Hipotezy przenieś do `Observations` albo `Follow-up`.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations` i `Follow-up`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` i opcjonalne `OWASP Top 10 Category`.

Zapisz użyty prompt w `docs/appsec/{data_iso}_{aplikacja}-prompt.md`.
Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

### 2. Ten Sam Zakres Dla Wskazanej Aplikacji Albo Folderów

**Kiedy użyć**

- Gdy repo zawiera kilka aplikacji, API, frontendów albo modułów.
- Gdy chcesz taki sam poziom review jak w promptcie 1, ale tylko dla konkretnego scope.

**Zakres**

Ten prompt ma te same priorytety i wymagania co prompt 1, ale ogranicza review do `<scope>`, np. folderów, jednej aplikacji, API, frontend + backend, route group albo modułu domenowego.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do AppSec review wskazanego obszaru aplikacji z takim samym zakresem kontroli jak główny prompt dla całego repo.

Scope: `<opisz scope, np. foldery, jedna aplikacja, jedno API, web app, route group, moduł domenowy albo backend project + odpowiadający frontend>`. Najpierw użyj `sec-repo-recon`, żeby zidentyfikować granice tego scope, powiązane entry pointy, modele danych, storage, integracje, konfigurację i frontend/backend paths. Następnie ogranicz analizę do `<scope>`.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów.

Priorytety:
- Tier 1: access control, server-side object-level authorization, function-level authorization, auth/session lifecycle, injection, XSS/template injection i unsafe file operations.
- Tier 2: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging.
- Tier 3: dependencies/supply-chain, crypto/JWT/key handling, rate limiting i business logic abuse.

Wymagania:
- Nie rób review całego repo. Elementy spoza `<scope>` oznacz jako `Out of Scope` albo `Follow-up`, jeśli wymagają osobnego review.
- Dla każdego endpointu z identyfikatorem zasobu w `<scope>` sprawdź owner/tenant/organization/permission binding przed użyciem obiektu.
- Sprawdź single object, list/search/filter, bulk operations, nested resource IDs, file IDs, export/import i destructive actions.
- Priorytetyzuj cross-user, cross-tenant, file-id swap, destructive operations oraz wariant authenticated-but-wrong-user.
- Dla injection i XSS wykonuj source-to-sink tracing: SQL/NoSQL/LDAP, command injection, template injection, SSRF, path traversal, unsafe redirect, deserialization oraz HTML/Markdown/JS/CSS/URL sinks.
- Dla auth/session sprawdź reset hasła, invite/magic link, MFA, logout, token revocation, stale sessions, privilege change/downgrade, admin-only flows i forced browsing.
- Nie implementuj poprawek. `Finding` raportuj tylko dla problemów potwierdzonych w `<scope>`. Hipotezy przenieś do `Observations` albo `Follow-up`.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations`, `Follow-up` oraz `Out of Scope`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` i opcjonalne `OWASP Top 10 Category`.

Zapisz użyty prompt w `docs/appsec/{data_iso}_{aplikacja}-prompt.md`.
Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

### 3. Dodatkowy Sweep Dla Podatności Spoza Głównego Zakresu

**Kiedy użyć**

- Po promptcie 1 albo 2, gdy chcesz sprawdzić rzadsze albo bardziej architektoniczne klasy ryzyka.
- Gdy repo ma reverse proxy, cache, nietypowe parsery, sandboxing, native/process isolation, rozproszone serwisy albo istotne IaC/deployment.

**Zakres**

- Request smuggling, cache poisoning, unsafe proxy/header trust, host/header confusion.
- Sandbox escapes, unsafe native/process isolation, parser differentials, unusual deserialization/parser behavior.
- Advanced crypto misuse, trust boundaries między serwisami, deployment/IaC-only risks, reverse-proxy-only security assumptions.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do dodatkowego sweepu całego repo dla podatności spoza głównego web/API zakresu. To jest uzupełnienie promptu głównego, nie jego zamiennik.

Scope: całe repo, ale tylko pod kątem rzadziej występujących albo architektonicznych klas ryzyka: request smuggling, cache poisoning, unsafe proxy/header trust, host/header confusion, sandbox escapes, unsafe native/process isolation, parser differentials, unusual deserialization/parser behavior, advanced crypto misuse, multi-service trust boundaries, deployment/IaC-only risks i reverse-proxy-only security assumptions.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów.

Wymagania:
- Najpierw sprawdź, czy dana klasa ryzyka ma realną powierzchnię w repo. Jeśli nie, opisz ją krótko jako `Observation` albo pomiń z jasną notatką zakresową.
- Nie raportuj spekulacyjnych `Finding`. `Finding` wymaga kodu, konfiguracji, IaC albo prześledzonej architektonicznej ścieżki braku kontroli.
- Jeśli decyzja zależy od runtime, reverse proxy, CDN, cloud gateway, WAF, konfiguracji produkcyjnej albo aktualnej dokumentacji, przenieś to do `Follow-up`.
- Nie implementuj poprawek.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations` i `Follow-up`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnienie braku mapowania oraz opcjonalne `OWASP Top 10 Category`.

Zapisz użyty prompt w `docs/appsec/{data_iso}_{aplikacja}-prompt.md`.
Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

## Źródła I Odświeżanie

Referencje skilli są po angielsku i mają sekcje `Sources`. Powstały jako krótkie lokalne opracowanie na podstawie oficjalnych albo uznanych materiałów: OWASP ASVS 5.0.0, OWASP WSTG latest, OWASP Top 10:2021, Microsoft Learn dla ASP.NET Core security i NuGet audit, Angular security docs, npm CLI `npm audit`, CodeQL docs i Semgrep docs.

Linki źródłowe do odświeżania referencji:

- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10:2021: https://owasp.org/Top10/2021/
- OWASP WSTG latest/stable: https://owasp.org/www-project-web-security-testing-guide/latest/
- Microsoft Learn ASP.NET Core security: https://learn.microsoft.com/en-us/aspnet/core/security/
- Angular security: https://angular.dev/best-practices/security
- npm audit: https://docs.npmjs.com/cli/v11/commands/npm-audit/
- CodeQL CLI/docs: https://docs.github.com/en/code-security/codeql-cli
- Semgrep docs: https://semgrep.dev/docs/

Internet i Context7 są dopuszczalne przy tworzeniu albo odświeżaniu referencji. Zwykłe review po skopiowaniu pakietu powinno korzystać z lokalnych plików i działać offline.
