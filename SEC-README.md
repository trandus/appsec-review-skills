# sec-* AppSec review

`sec-*` to przenośny zestaw czterech skilli do lokalnego AppSec code review. Zwykłe review działa offline po skopiowaniu do repozytorium: bez internetu, Context7, GitHuba, SaaS i zewnętrznych skanerów.

## Skille

| Skill | Rola |
| --- | --- |
| `sec-appsec-review` | Orkiestrator review: scope, `Review Depth`, `ASVS Level`, flow i raport końcowy. |
| `sec-repo-recon` | Rozpoznanie struktury repo, stacku, entry pointów, konfiguracji, zależności i opcjonalnych lokalnych zasad hostującego repo. |
| `sec-asvs-review` | Lokalny lookup OWASP ASVS, poziomy `L1`, `L2`, `L3`, `ASVS Mapping` i rozróżnienie ASVS od OWASP Web/API Top 10. |
| `sec-reporting` | Format raportu oraz rozdzielenie `Findings`, `Observations` i `Follow-up`. |

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

ASVS 5.0.0 jest głównym standardem wymagań i mapowania. OWASP Web Top 10:2021 oraz OWASP API Security Top 10:2023 są pomocniczymi kategoriami i perspektywami ryzyka, np. `A01 Broken Access Control` albo `API1:2023 Broken Object Level Authorization`. `ASVS Level` nie jest severity, `Review Depth` ani kategorią OWASP Web/API Top 10.

## Format Raportu

Raport po review zawsze ma być napisany po polsku. Używaj normalnego, czytelnego języka polskiego w opisach ryzyka, dowodów, wpływu, rekomendacji i testów. Angielskie określenia zostawiaj tylko wtedy, gdy są utrwalonymi terminami domenowymi bez rozsądnego polskiego odpowiednika albo jednoznacznymi nazwami standardów, klas podatności, pól raportu, bibliotek, narzędzi, nagłówków, konfiguracji lub API.

Unikaj przypadkowego mieszania polskiego i angielskiego w jednym zdaniu. Jeśli polski odpowiednik jest naturalny, użyj polskiego, np. `dowód`, `wpływ`, `ścieżka ryzyka`, `zalecenie`, `test regresyjny`, `uprawnienie`, `właściciel zasobu`. Zachowuj krótkie terminy techniczne tam, gdzie poprawiają precyzję, np. `XSS`, `SSRF`, `CSRF`, `IDOR/BOLA`, `JWT`, `OAuth/OIDC`, `claim`, `tenant`, `endpoint`, `cookie`, `lockfile`.

Każdy raport musi zawierać sekcje `Findings`, `Observations` i `Follow-up`, jeśli te kategorie realnie występują. Jeśli kategoria nie ma wyników, napisz to jawnie, np. `Findings: brak potwierdzonych findingów`.

| Typ wyniku | Kiedy użyć | Wymagane elementy |
| --- | --- | --- |
| `Finding` | Potwierdzony problem z dowodem w kodzie albo prześledzonym brakiem wymaganej kontroli. | `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnienie braku mapowania, opcjonalnie `OWASP Web/API Top 10 Category`. |
| `Observation` | Obserwacja projektowa, osłabiona kontrola, sygnał narzędziowy albo hipoteza bez wystarczającego dowodu. | Częściowy dowód, powód braku kwalifikacji jako `Finding`, sugerowany następny krok. |
| `Follow-up` | Pytanie, walidacja narzędziowa, potrzeba aktualnej dokumentacji, niedostępny runtime/login/baza/konfiguracja albo osobne sprawdzenie. | Co trzeba sprawdzić, dlaczego to potrzebne, jaki wynik odblokuje decyzję. |

Review nie implementuje zmian. Dla findingów zwraca `Remediation` oraz `Regression Test`.

## Poziomy Wyszukiwania / Review Depth

`Review Depth` określa budżet pracy, szerokość pokrycia i głębokość walidacji. W promptach zmieniaj tylko wartość parametru `Review Depth`; nie dopisuj osobnych checklist dla wybranego poziomu. Skill odczytuje znaczenie poziomu z `.codex/skills/sec-appsec-review/references/review-depth-profiles.md`.

Dostępne poziomy:

| `Review Depth` | Kiedy użyć | Co agent ma zrobić | Ograniczenia |
| --- | --- | --- | --- |
| `quick` | Szybkie wyszukiwanie najważniejszych ryzyk albo wstępny sweep dużego repo. | Sprawdzić najważniejsze entry pointy, top web/API risks, reprezentatywne przepływy, bazową konfigurację, oczywiste luki auth/authz, główne wejścia danych i najbardziej ryzykowne zależności. | Raport musi jasno opisać sampling i pominięte obszary. |
| `standard` | Domyślny poziom dla zwykłego review. | Prześledzić główne end-to-end flows, reprezentatywne warianty negatywne, ownership/tenant boundaries, sensitive data, logging, konfigurację, główne ryzyka web/API i mapowanie ASVS. | Nie udaje pełnej certyfikacji ani pełnego pentestu runtime. |
| `deep` | Pogłębione wyszukiwanie dla wysokiego ryzyka, krytycznego scope albo ważnej aplikacji. | Dodać szerszą analizę wariantów, więcej ścieżek negatywnych, missing-control analysis, cross-layer interactions, user-provided tool output i szerszy dependency/supply-chain review. | Jeśli scope jest za szeroki, agent ma go podzielić albo jawnie ograniczyć. |

## Poziomy ASVS / ASVS Level

`ASVS Level` określa rygor wymagań używanych do mapowania findingów. Nie jest severity, `Review Depth` ani kategorią OWASP Top 10. Pełne mapowanie jest obsługiwane przez `sec-asvs-review` i lokalny dataset `asvs-5.0.0-local.json`.

| `ASVS Level` | Kiedy użyć | Znaczenie w review |
| --- | --- | --- |
| `L1` | Małe, niskiego ryzyka albo szybkie review, gdy celem jest podstawowy poziom kontroli. | Mapowanie do podstawowych wymagań bezpieczeństwa aplikacji. |
| `L2` | Domyślny poziom dla typowego web/API review. | Praktyczny balans między kosztem a rygorem dla aplikacji przetwarzających istotne dane lub operacje. |
| `L3` | Krytyczne systemy, wysokie ryzyko, mocne wymagania regulacyjne albo szczególnie wrażliwe dane. | Największy rygor mapowania; zwykle wymaga głębszego review, silniejszych dowodów i jawnego zakresu. |

Jeśli wybrany poziom nie mieści żądanego scope, agent ma zawęzić zakres, podzielić review albo jawnie opisać ograniczenia. Nie wolno sugerować pełnego pokrycia, jeśli faktycznie wykonano tylko sampling.

Przykład użycia w promptcie:

```text
Review Depth: standard (dostępne: quick, standard, deep)
ASVS Level: L2 (dostępne: L1, L2, L3)
```

## Prompty

W promptach ustawiaj tylko parametry, np. `Review Depth: standard` i `ASVS Level: L2`. Znaczenie poziomów jest opisane w skillach, szczególnie w `review-depth-profiles.md` i `sec-asvs-review`, więc użytkownik może zmienić poziom bez przepisywania całego promptu.

### 1. Najważniejszy Prompt: Całe Repo

**Kiedy użyć**

- Gdy chcesz wykonać główny, praktyczny przegląd bezpieczeństwa całego repo.
- Gdy priorytetem są exploitable paths, ASVS, OWASP Web Top 10 i OWASP API Security Top 10.

**Zakres**

| Tier | Priorytet |
| --- | --- |
| `Tier 1` | Access control, API object/property/function authorization, auth/session lifecycle, injection, XSS/template injection, unsafe file operations. |
| `Tier 2` | SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging, API resource consumption. |
| `Tier 3` | Dependencies/supply-chain, crypto/JWT/key handling, rate limiting, business logic abuse, API inventory, unsafe consumption of upstream APIs. |

**Prompt**

```text
Cel: użyj `sec-appsec-review` do szerokiego AppSec review całego repo z priorytetem na najbardziej exploitable ścieżki ataku.

Scope: całe repo.
Review Depth: standard (dostępne: quick, standard, deep)
ASVS Level: L2 (dostępne: L1, L2, L3)
Tryb: offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów podczas zwykłego review.

Najpierw użyj `sec-repo-recon`, żeby rozpoznać lokalne instrukcje hostującego repo, architekturę, aplikacje, entry pointy, modele danych, storage, integracje, konfigurację, zależności i miejsca, gdzie przepływają identyfikatory zasobów.

Użyj ASVS 5.0.0 jako standardu wymagań i mapowania. Użyj OWASP Web Top 10:2021 oraz OWASP API Security Top 10:2023 jako pomocniczych kategorii ryzyka, nie jako zamiennika ASVS.

Priorytety:
- Tier 1: access control, API object/property/function authorization, auth/session lifecycle, injection, XSS/template injection i unsafe file operations.
- Tier 2: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging i API resource consumption.
- Tier 3: dependencies/supply-chain, crypto/JWT/key handling, rate limiting, business logic abuse, API inventory i unsafe consumption of upstream APIs.

Wymagania:
- Najpierw zmapuj powierzchnię ataku i wybierz główne ścieżki do prześledzenia zgodnie z `Review Depth`.
- Dla identyfikatorów zasobów sprawdzaj server-side owner/tenant/organization/permission binding przed użyciem obiektu.
- Dla injection, XSS, SSRF, plików, redirectów i deserializacji wykonuj source-to-sink tracing.
- Dla operacji wysokiego wpływu sprawdzaj authz, replay, race/TOCTOU, idempotency, audit logging i właściwe ograniczenia nadużyć.
- Nie implementuj poprawek. `Finding` raportuj tylko z dowodem w kodzie albo prześledzonym brakiem wymaganej kontroli. Hipotezy przenieś do `Observations` albo `Follow-up`.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations` i `Follow-up`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` i opcjonalne `OWASP Web/API Top 10 Category`.

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
Cel: użyj `sec-appsec-review` do AppSec review wskazanego obszaru aplikacji z takim samym modelem ryzyka jak główny prompt dla całego repo.

Scope: `<opisz scope, np. foldery, jedna aplikacja, jedno API, web app, route group, moduł domenowy albo backend project + odpowiadający frontend>`.
Review Depth: standard (dostępne: quick, standard, deep)
ASVS Level: L2 (dostępne: L1, L2, L3)
Tryb: offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów podczas zwykłego review.

Najpierw użyj `sec-repo-recon`, żeby zidentyfikować granice scope, powiązane entry pointy, modele danych, storage, integracje, konfigurację i frontend/backend paths. Następnie ogranicz analizę do `<scope>`.

Użyj ASVS 5.0.0 jako standardu wymagań i mapowania. Użyj OWASP Web Top 10:2021 oraz OWASP API Security Top 10:2023 jako pomocniczych kategorii ryzyka, nie jako zamiennika ASVS.

Priorytety:
- Tier 1: access control, API object/property/function authorization, auth/session lifecycle, injection, XSS/template injection i unsafe file operations.
- Tier 2: SSRF, CSRF/CORS, destructive operations, race/replay/idempotency, secrets/config, sensitive data/logging i API resource consumption.
- Tier 3: dependencies/supply-chain, crypto/JWT/key handling, rate limiting, business logic abuse, API inventory i unsafe consumption of upstream APIs.

Wymagania:
- Nie rób review całego repo. Elementy spoza `<scope>` oznacz jako `Out of Scope` albo `Follow-up`, jeśli wymagają osobnego review.
- Najpierw zmapuj powierzchnię ataku w `<scope>` i wybierz główne ścieżki do prześledzenia zgodnie z `Review Depth`.
- Dla identyfikatorów zasobów sprawdzaj server-side owner/tenant/organization/permission binding przed użyciem obiektu.
- Dla injection, XSS, SSRF, plików, redirectów i deserializacji wykonuj source-to-sink tracing.
- Dla operacji wysokiego wpływu sprawdzaj authz, replay, race/TOCTOU, idempotency, audit logging i właściwe ograniczenia nadużyć.
- Nie implementuj poprawek. `Finding` raportuj tylko dla problemów potwierdzonych w `<scope>`. Hipotezy przenieś do `Observations` albo `Follow-up`.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations`, `Follow-up` oraz `Out of Scope`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` i opcjonalne `OWASP Web/API Top 10 Category`.

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

Review Depth: standard (dostępne: quick, standard, deep)
ASVS Level: L2 (dostępne: L1, L2, L3)
Tryb: offline, bez dostępu do internetu, GitHuba, SaaS i zewnętrznych skanerów podczas zwykłego review.

Użyj ASVS 5.0.0 jako standardu wymagań i mapowania. OWASP Web/API Top 10 może być użyte tylko jako pomocnicza kategoria ryzyka, jeśli pasuje do potwierdzonego problemu.

Wymagania:
- Najpierw sprawdź, czy dana klasa ryzyka ma realną powierzchnię w repo. Jeśli nie, opisz ją krótko jako `Observation` albo pomiń z jasną notatką zakresową.
- Nie raportuj spekulacyjnych `Finding`. `Finding` wymaga kodu, konfiguracji, IaC albo prześledzonej architektonicznej ścieżki braku kontroli.
- Jeśli decyzja zależy od runtime, reverse proxy, CDN, cloud gateway, WAF, konfiguracji produkcyjnej albo aktualnej dokumentacji, przenieś to do `Follow-up`.
- Nie implementuj poprawek.

Output: zwróć raport po polsku z sekcjami `Findings`, `Observations` i `Follow-up`, jeśli realnie występują. Jeśli sekcja nie ma wyników, napisz to jawnie. Każdy `Finding` musi zawierać `Title`, `Severity`, `Confidence`, `Status`, `Location`, `Evidence`, `Attack Variant`, `Risk Path`, `Impact`, `Remediation`, `Regression Test`, `ASVS Mapping` albo uzasadnienie braku mapowania oraz opcjonalne `OWASP Web/API Top 10 Category`.

Zapisz użyty prompt w `docs/appsec/{data_iso}_{aplikacja}-prompt.md`.
Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

## Źródła I Odświeżanie

Referencje skilli są po angielsku i mają sekcje `Sources`. Powstały jako krótkie lokalne opracowanie na podstawie oficjalnych albo uznanych materiałów: OWASP ASVS 5.0.0, OWASP WSTG stable, OWASP Web Top 10:2021, OWASP API Security Top 10:2023, Microsoft Learn dla ASP.NET Core security i NuGet audit, Angular security docs, npm CLI `npm audit`, CodeQL docs i Semgrep docs.

Linki źródłowe do odświeżania referencji:

| Obszar | Źródło |
| --- | --- |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ |
| OWASP Web Top 10:2021 | https://owasp.org/Top10/2021/ |
| OWASP API Security Top 10:2023 | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ |
| OWASP WSTG stable | https://owasp.org/www-project-web-security-testing-guide/stable/ |
| Microsoft Learn ASP.NET Core security | https://learn.microsoft.com/en-us/aspnet/core/security/ |
| Angular security | https://angular.dev/best-practices/security |
| npm audit | https://docs.npmjs.com/cli/v11/commands/npm-audit/ |
| CodeQL CLI/docs | https://docs.github.com/en/code-security/codeql-cli |
| Semgrep docs | https://semgrep.dev/docs/ |

Internet i Context7 są dopuszczalne przy tworzeniu albo odświeżaniu referencji. Te linki nie są wymaganiem dla zwykłego review: po skopiowaniu pakietu review powinno korzystać z lokalnych plików i działać offline.
