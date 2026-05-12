# sec-* AppSec review

`sec-*` to przenośny zestaw czterech skilli do lokalnego AppSec code review. Zwykłe review działa offline po skopiowaniu do repozytorium: bez internetu, Context7, GitHuba, SaaS i zewnętrznych skanerów.

## Skille

- `sec-appsec-review`: orkiestrator review, wybór scope, `Review Depth`, `ASVS Level`, flow i raport końcowy.
- `sec-repo-recon`: rozpoznanie struktury repo, stacku, entry pointów, konfiguracji, zależności i opcjonalnych lokalnych zasad hostującego repo.
- `sec-asvs-review`: lokalny lookup OWASP ASVS, poziomy `L1`, `L2`, `L3`, `ASVS Mapping` i rozróżnienie ASVS od OWASP Top 10.
- `sec-reporting`: format raportu, rozdzielenie `Finding`, `Observation`, `Follow-up` oraz blok `Fix Prompt`.

## Szybki start

1. Skopiuj foldery `.codex/skills/sec-*` oraz `SEC-README.md` do głównego folderu repozytorium.
2. Uruchom review jednym z promptów poniżej.
3. Najpierw rozpoznaj lokalne instrukcje hostującego repo, jeśli istnieją: instrukcje agentów, README, mapy projektu, dokumentację architektury, lokalne skille, zasady wyszukiwania plików i komendy.
4. Wybierz `Review Mode`: focused area review albo compact full flow.
5. Wybierz `Review Depth`: `quick`, `standard`, `deep`.
6. Wybierz `ASVS Level`: `L1`, `L2`, `L3`.

Domyślny wybór dla zwykłego review to `standard + ASVS L2`.

## Praca offline

Focused area review analizuje jeden obszar, np. auth/authz, dependencies albo config/secrets. Compact full flow przechodzi przez recon, threat model, entry points, auth/authz, input/data, backend, frontend, config/secrets, dependencies, sensitive data, privacy/security logging, abuse/rate limiting i destructive operations.

Pakiet nie uruchamia automatycznie `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, CodeQL ani Semgrep. Wyniki takich narzędzi mogą być przekazane ręcznie albo użyte lokalnie na wyraźne żądanie jako materiał pomocniczy, ale `Finding` nadal wymaga dowodu w kodzie albo prześledzonego braku kontroli.

## ASVS lookup offline

`sec-asvs-review` ma lokalny dataset `references/asvs-5.0.0-local.json` i helper:

```powershell
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query authorization
python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --chapter 8
```

ASVS jest głównym standardem wymagań i mapowania. OWASP Top 10 jest tylko pomocniczą kategorią ryzyka, np. `A01 Broken Access Control`.

## Format raportu

Raport po review zawsze ma być napisany po polsku. Techniczne nazwy sekcji i pól mogą pozostać po angielsku, np. `Finding`, `Observation`, `Follow-up`, `Evidence`, `Risk Path`, `ASVS Mapping` i `Fix Prompt`, ale ich treść opisowa ma być po polsku.

- `Finding`: potwierdzony problem z `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnieniem braku mapowania, opcjonalnym `OWASP Top 10 Category` oraz `Fix Prompt`.
- `Observation`: obserwacja projektowa albo hipoteza bez wystarczającego dowodu.
- `Follow-up`: pytanie, walidacja narzędziowa, potrzeba aktualnej dokumentacji albo osobne sprawdzenie.

Review nie implementuje zmian. Dla findingów zwraca `Remediation` i `Fix Prompt` do osobnego zadania naprawczego.

## Prompty

### Pełny mały flow

**Kiedy użyć**

- Gdy potrzebny jest szeroki pierwszy przegląd repo.
- Gdy scope nie jest jeszcze zawężony do jednego modułu albo obszaru security.

**Co uzyskasz**

- Raport z głównych strumieni AppSec.
- Priorytety dalszego review i napraw.

**Zakres**

- Recon, threat model, entry points, auth/authz, input/data, backend, frontend, config/secrets, dependencies.
- Sensitive data, privacy/security logging, abuse/rate limiting i destructive operations.
- Lokalne zasady hostującego repo, jeśli istnieją.

**Wynik**

- `Finding`, `Observation`, `Follow-up`.
- Dla każdego `Finding`: `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping`, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do compact full flow AppSec review tego repo.

Scope: całe repo w zakresie lokalnego code review. Najpierw użyj `sec-repo-recon`, żeby rozpoznać lokalne instrukcje, mapy repo, dokumentację architektury, lokalne skille i zasady wyszukiwania plików, jeśli istnieją.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów.

Wymagania: nie implementuj poprawek. Raportuj `Finding` tylko z dowodem w kodzie albo prześledzonym brakiem wymaganej kontroli. Hipotezy przenieś do `Observation` albo `Follow-up`.

Output: zwróć raport z sekcjami `Finding`, `Observation`, `Follow-up`. Każdy `Finding` ma zawierać `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping`, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.
```

### Review jednego obszaru security

**Kiedy użyć**

- Gdy chcesz sprawdzić jeden obszar security, np. auth/authz, config/secrets albo dependencies.
- Gdy repo jest duże, ale interesuje Cię konkretna klasa ryzyka.

**Co uzyskasz**

- Krótki raport dla wybranego obszaru.
- Findingi oparte na takim samym standardzie dowodu jak w pełnym flow.

**Zakres**

- Tylko wskazany obszar security.
- Minimalny recon potrzebny do znalezienia właściwych plików i entry pointów.

**Wynik**

- `Finding`, `Observation`, `Follow-up` tylko dla wskazanego obszaru.
- `Remediation` i `Fix Prompt`, bez wdrażania zmian.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review obszaru security `<obszar>`.

Scope: ogranicz analizę do `<obszar>`. Najpierw rozpoznaj lokalne zasady hostującego repo, jeśli istnieją, oraz pliki potrzebne do tego obszaru.

Tryb: `<quick|standard|deep> + ASVS <L1|L2|L3>`, offline, bez dostępu do internetu.

Wymagania: raportuj tylko findingi z dowodem w kodzie albo prześledzonym brakiem kontroli. Hipotezy przenieś do `Observation` albo `Follow-up`. Nie naprawiaj kodu.

Output: każdy `Finding` ma zawierać `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnienie braku mapowania oraz `Fix Prompt`.
```

### Review konkretnego obszaru aplikacji

**Kiedy użyć**

- Gdy repo zawiera więcej niż jedną aplikację, API, frontend albo moduł web.
- Gdy chcesz przejrzeć tylko jeden produktowy scope, a nie całe repo.

**Co uzyskasz**

- Raport AppSec ograniczony do wskazanego API, web app, modułu web, route group albo pary backend + frontend.
- Elementy spoza zakresu oznaczone jako `Out of Scope` albo `Follow-up`, a nie jako `Finding`.

**Zakres**

- Przykładowy scope: jedno API, jedna aplikacja web, jeden moduł web, jeden route group, jeden projekt backendowy i odpowiadający mu frontend.
- `sec-repo-recon` najpierw identyfikuje granice wskazanego obszaru i dopiero potem zawęża review.

**Wynik**

- Raport tylko dla wskazanego obszaru aplikacji.
- `Finding`, `Observation`, `Follow-up`, `Out of Scope`.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do review konkretnego obszaru aplikacji w repo: `<opisz scope, np. jedno API, jedna web app, moduł web, route group albo backend project + odpowiadający frontend>`.

Scope: najpierw użyj `sec-repo-recon`, żeby zidentyfikować aplikacje, API, frontendowe moduły, route groups, projekty backendowe i powiązane frontendowe ścieżki. Następnie ogranicz analizę wyłącznie do `<scope>`.

Tryb: `<quick|standard|deep> + ASVS <L1|L2|L3>`, offline, bez dostępu do internetu.

Wymagania: nie rób review całego repo. Nie implementuj poprawek. Raportuj `Finding` tylko dla problemów potwierdzonych w `<scope>`. Elementy spoza zakresu oznacz jako `Out of Scope` albo `Follow-up`, jeśli wymagają osobnego review.

Output: zwróć raport tylko dla `<scope>` z sekcjami `Finding`, `Observation`, `Follow-up` i `Out of Scope`. Każdy `Finding` ma zawierać `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping`, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.
```

### Quick + ASVS L1

**Kiedy użyć**

- Jako szybki sanity check przed głębszym review.
- Przy ograniczonym budżecie czasu.

**Co uzyskasz**

- Krótką listę najpewniejszych findingów i follow-upów.
- Wstępne priorytety do dalszej analizy.

**Zakres**

- Najważniejsze entry points.
- Oczywiste braki auth/authz.
- Podstawowa konfiguracja i wysokopoziomowe zależności.

**Wynik**

- Tylko potwierdzone `Finding` oraz najważniejsze `Observation` i `Follow-up`.

**Prompt**

```text
Cel: użyj `sec-appsec-review` jako szybkiego sanity checku.

Scope: najważniejsze entry points, podstawowa auth/authz, input validation, config/secrets i dependencies.

Tryb: `quick + ASVS L1`, offline, bez dostępu do internetu.

Wymagania: najpierw wykonaj krótkie `sec-repo-recon`. Nie uruchamiaj skanerów i nie implementuj poprawek.

Output: zwróć tylko potwierdzone `Finding` oraz najważniejsze `Observation` i `Follow-up`. Każdy `Finding` musi mieć `Evidence`, `Risk Path`, `Remediation`, `Regression Test`, `ASVS Mapping` i `Fix Prompt`.
```

### Deep + ASVS L2/L3

**Kiedy użyć**

- Dla krytycznego obszaru albo przepływu wysokiego ryzyka.
- Gdy wcześniejsze review wykazało słabe kontrole.

**Co uzyskasz**

- Dokładny raport dla wskazanego obszaru.
- Variant analysis i ścieżki negatywne.

**Zakres**

- Wskazany obszar.
- Ownership boundaries, brakujące kontrole i warianty obejścia.

**Wynik**

- Potwierdzone `Finding` z mocnym `Evidence`.
- Pozostałe elementy jako `Observation` albo `Follow-up`.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do pogłębionego review obszaru `<obszar>`.

Scope: `<obszar>`, jego główne ścieżki, ścieżki negatywne, ownership boundaries i brakujące kontrole.

Tryb: `deep + ASVS <L2|L3>`, offline, bez dostępu do internetu.

Wymagania: rozpoznaj lokalne zasady repo, prześledź przepływy, wykonaj variant analysis i nie implementuj poprawek. Raportuj tylko `Finding` z obronnym `Evidence`.

Output: resztę przenieś do `Observation` albo `Follow-up`. Dla każdego findingu podaj `Location`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping`, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.
```

### Review auth/authz

**Kiedy użyć**

- Gdy ryzyko dotyczy logowania, sesji, claims, policy albo ról.
- Gdy sprawdzasz IDOR/BOLA, tenant isolation albo ownership boundaries.

**Co uzyskasz**

- Raport z potwierdzonymi lukami dostępu.
- Brakujące testy negatywne jako `Regression Test` albo `Follow-up`.

**Zakres**

- Server-side authentication.
- Function-level authorization.
- Object-level authorization.
- Frontend tylko jako element przepływu, nie jako jedyna kontrola.

**Wynik**

- `Finding`, `Observation`, `Follow-up` dla auth/authz.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review auth/authz.

Scope: entry points, middleware auth, policies, role/claims, session/cookie/token handling i ownership boundaries.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu.

Wymagania: sprawdź, czy backend egzekwuje function-level i object-level authorization, a frontend nie jest jedyną kontrolą. Nie naprawiaj kodu.

Output: każdy `Finding` ma mieć `Evidence`, `Risk Path`, `ASVS Mapping`, `Remediation`, `Regression Test` i `Fix Prompt`.
```

### Review dependencies/supply chain bez skanerów

**Kiedy użyć**

- Gdy chcesz ręcznie ocenić zależności bez uruchamiania narzędzi.
- Gdy masz ręcznie dostarczone wyniki narzędzi i chcesz je potraktować jako input.

**Co uzyskasz**

- Findingi oparte na repo i ścieżce ryzyka.
- Follow-upy dla audytów narzędziowych.

**Zakres**

- Manifesty NuGet/npm, lockfile, źródła pakietów.
- Version ranges, transitive dependencies, abandoned packages, package scripts i dependency confusion.

**Wynik**

- `Finding`, `Observation`, `Follow-up` z dowodem albo wskazaniem brakującej walidacji.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review dependencies/supply chain.

Scope: manifesty NuGet/npm, lockfile, feed sources, version ranges, transitive dependency exposure, package scripts i ryzyko dependency confusion.

Tryb: offline, bez dostępu do internetu i bez uruchamiania skanerów.

Wymagania: jeśli są ręcznie dostarczone wyniki `npm audit`, `dotnet package list --vulnerable`, `dotnet list package --vulnerable`, CodeQL albo Semgrep, potraktuj je jako input, nie jako automatyczny finding. Nie naprawiaj kodu.

Output: zwróć `Finding`, `Observation` i `Follow-up` z `Evidence`, `Risk Path`, `Remediation`, `Regression Test`, `ASVS Mapping` i `Fix Prompt`.
```

### Review zależności z użyciem narzędzi

Użyj, gdy chcesz rozszerzyć review o lokalne wyniki narzędzi dependency/security.

Co uzyskasz:
- ocenę ryzyk zależności i supply-chain,
- rozróżnienie `Finding`, `Observation` i `Follow-up`,
- raport z `Evidence`, `Reachability`, `Remediation` i `Fix Prompt`.

**Prompt**

```text
Przeprowadź dependency and supply-chain security review dla wskazanego obszaru repozytorium.

Tryb: offline, bez dostępu do internetu. Użyj lokalnych narzędzi tylko na moje wyraźne żądanie.

Zakres:
- Sprawdź manifesty zależności i lockfile.
- Na moje żądanie użyj dostępnych lokalnie narzędzi:
  - `npm audit`
  - `dotnet package list --vulnerable`
  - `dotnet list package --vulnerable`
  - Semgrep
  - CodeQL

Wynik:
- Zweryfikuj wyniki narzędzi względem kodu i realnego użycia zależności.
- Raportuj jako `Finding`, `Observation` albo `Follow-up`.
- Uwzględnij `Evidence`, `Reachability`, `ASVS Mapping`, `Remediation` i `Fix Prompt`.
- Nie implementuj poprawek i nie aktualizuj zależności.
```

### Review config/secrets

**Kiedy użyć**

- Dla konfiguracji, sekretów, connection strings, CORS, cookies, headers i debug flags.
- Przy porównaniu środowisk dev/test/prod.

**Co uzyskasz**

- Listę ryzyk konfiguracyjnych z konkretnymi kluczami i warunkami.
- Follow-upy dla elementów wymagających potwierdzenia poza kodem.

**Zakres**

- Pliki konfiguracyjne, sample config, CI/deployment manifests.
- Potencjalne przecieki sekretów albo danych wrażliwych do logów.

**Wynik**

- `Finding`, `Observation`, `Follow-up` dla config/secrets.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review config/secrets.

Scope: configuration files, environment files, sample config, CI/deployment manifests, connection strings, API keys, tokens, certificates, CORS, cookies, headers, debug flags i logging/telemetry.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu.

Wymagania: nie uruchamiaj zewnętrznych skanerów i nie naprawiaj kodu.

Output: każdy `Finding` musi wskazywać `Location`, konfigurację lub klucz, warunek ryzyka, `Evidence`, `Risk Path`, `Remediation`, `Regression Test`, `ASVS Mapping` i `Fix Prompt`.
```

### Review sensitive data/privacy logging

**Kiedy użyć**

- Gdy repo przetwarza PII, tokeny, sekrety, dane płatnicze, pliki prywatne albo dane użytkownika.
- Gdy ryzyko dotyczy logowania, telemetry albo error handling.

**Co uzyskasz**

- Raport o wycieku, nadmiarowym dostępie albo braku kontroli nad danymi.
- Wskazania do testów regresyjnych dla ujawnienia danych.

**Zakres**

- Przepływy danych od inputu do storage, logs, telemetry, export i integracji.
- Minimalizacja danych i kontrola miejsc ujawnienia.

**Wynik**

- `Finding`, `Observation`, `Follow-up` dla danych wrażliwych i logowania.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review sensitive data/privacy logging.

Scope: przepływy danych od inputu do storage, logs, telemetry, export i integracji zewnętrznych.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu.

Wymagania: sprawdź, czy logi i błędy nie ujawniają sekretów, tokenów, cookies, payment data, PII ani wrażliwych payloadów. Nie implementuj zmian.

Output: raportuj `Finding`, `Observation`, `Follow-up` z `Evidence`, `Risk Path`, `Remediation`, `Regression Test`, `ASVS Mapping` i `Fix Prompt`.
```

### Review destructive operations

**Kiedy użyć**

- Dla delete, revoke, disable, refund, payout, transfer, export/import, publish/unpublish i zmian uprawnień.
- Gdy operacja jest nieodwracalna, kosztowna albo wpływa na cudze zasoby.

**Co uzyskasz**

- Raport o ryzykach w operacjach wysokiego wpływu.
- Testy negatywne i wymagane kontrole jako `Regression Test` albo `Follow-up`.

**Zakres**

- Auth/authz, ownership boundaries, tenant isolation.
- CSRF/antiforgery tam, gdzie ma zastosowanie.
- Idempotency, audit logging i cleanup zależnych danych.

**Wynik**

- `Finding`, `Observation`, `Follow-up` dla destructive operations.

**Prompt**

```text
Cel: użyj `sec-appsec-review` do focused area review destructive operations.

Scope: delete/revoke/disable/refund/payout/transfer/export/import/publish/unpublish oraz permission-change flows.

Tryb: `standard + ASVS L2`, offline, bez dostępu do internetu.

Wymagania: sprawdź server-side auth/authz, ownership boundaries, tenant isolation, CSRF/antiforgery tam gdzie ma zastosowanie, idempotency, audit logging, negative tests i cleanup zależnych danych. Nie naprawiaj kodu.

Output: każdy `Finding` ma mieć `Evidence`, `Risk Path`, `Remediation`, `Regression Test`, `ASVS Mapping`, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.
```

### ASVS mapping offline

**Kiedy użyć**

- Gdy masz opis findingu albo obszaru i potrzebujesz mapowania do ASVS bez internetu.
- Gdy chcesz odróżnić `ASVS Mapping` od pomocniczej kategorii OWASP Top 10.

**Co uzyskasz**

- Identyfikator ASVS albo uzasadnienie braku dobrego mapowania.
- Opcjonalną kategorię OWASP Top 10, jeśli pasuje.

**Zakres**

- Lokalny dataset ASVS i poziom `L1`, `L2` albo `L3`.

**Wynik**

- `ASVS Mapping` albo uzasadnienie braku mapowania.

**Prompt**

```text
Cel: użyj `sec-asvs-review`, aby offline zmapować opisany finding albo obszar `<opis>` do OWASP ASVS.

Scope: lokalny dataset ASVS i poziom `<L1|L2|L3>`.

Tryb: offline ASVS lookup, bez dostępu do internetu.

Wymagania: jeżeli nie ma dobrego dopasowania, podaj uzasadnienie braku `ASVS Mapping`. `OWASP Top 10 Category` traktuj tylko jako opcjonalną kategorię ryzyka.

Output: zwróć proponowane `ASVS Mapping`, poziom ASVS, krótkie uzasadnienie i opcjonalne `OWASP Top 10 Category`.
```

### Raport końcowy

**Kiedy użyć**

- Po zakończeniu review.
- Po zebraniu wyników kilku strumieni.

**Co uzyskasz**

- Końcowy raport bez implementowania poprawek.
- Ujednolicony format findingów, obserwacji i follow-upów.

**Zakres**

- Normalizacja findingów.
- Deduplikacja.
- Degradacja hipotez bez dowodu.

**Wynik**

- Raport z pełnym formatem `Finding` i blokami `Fix Prompt`.

**Prompt**

```text
Cel: użyj `sec-reporting`, aby z wyników review przygotować końcowy raport.

Scope: wszystkie wyniki z zakończonych strumieni review.

Tryb: raportowanie, offline, bez dostępu do internetu i bez zmian w kodzie.

Wymagania: rozdziel `Finding`, `Observation` i `Follow-up`. Usuń duplikaty i zdegraduj hipotezy bez dowodu do `Observation` albo `Follow-up`.

Output: każdy `Finding` musi mieć `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnienie braku mapowania, opcjonalne `OWASP Top 10 Category` i `Fix Prompt`.
```

### Fix Prompt dla jednego findingu

**Kiedy użyć**

- Gdy chcesz przekazać pojedynczy potwierdzony finding do osobnego zadania naprawczego.
- Gdy potrzebujesz tylko promptu naprawczego, a nie implementacji.

**Co uzyskasz**

- Gotowy `Fix Prompt` z ograniczeniem scope.
- Oczekiwany test regresyjny albo walidację.

**Zakres**

- Jeden potwierdzony finding.
- Bez zmian w kodzie.

**Wynik**

- Samodzielny prompt do osobnego zadania implementacyjnego.

**Prompt**

```text
Cel: użyj `sec-reporting`, aby przekształcić jeden potwierdzony finding `<finding>` w samodzielny `Fix Prompt`.

Scope: tylko ten finding i jego wskazane lokalizacje.

Tryb: przygotowanie promptu naprawczego, offline, bez dostępu do internetu i bez implementacji.

Wymagania: prompt ma być po polsku, ale musi zawierać angielskie pola techniczne: `Title`, `Scope`, `Locations`, `Risk`, `Expected Behavior`, `Remediation`, `Regression Test`, `Scope Limits`.

Output: nie dodawaj implementacji. Zawrzyj ograniczenie: napraw tylko ten finding, zachowaj lokalne konwencje repo i nie ruszaj niepowiązanych plików.
```

## Źródła i odświeżanie

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
