# sec-* AppSec review

`sec-*` to przenośny zestaw skilli Codex do lokalnego AppSec code review. Pakiet pomaga przejść repozytorium offline, uporządkować wynik po polsku i dopasować potwierdzone problemy do OWASP ASVS.

Ten plik jest krótkim przewodnikiem dla osoby, która chce uruchomić review albo zrozumieć wynik. Szczegółowe reguły pracy są w skillach i ich referencjach.

## Jak To Działa

| Element | Rola |
| --- | --- |
| `sec-appsec-review` | Orkiestracja lokalnego review: scope, krótki recon, priorytety i evidence gate. |
| `sec-reporting` | Kanoniczne typy wyników oraz format raportu. |
| `sec-asvs-review` | Lokalny mapper OWASP ASVS używany po znalezieniu konkretnego problemu. |
| `risk-baseline.md` | Główna, tierowana priorytetyzacja obszarów ryzyka. |
| `always-check.md` | Mała przypominajka oczywistych ryzyk dobieranych do technologii i scope'u. |

Zwykły przebieg jest offline: bez internetu, GitHuba, SaaS, runtime access i zewnętrznych skanerów. `repomix` jest opcjonalnym wejściem pomocniczym, gdy istnieje i pasuje do instrukcji repo.

W praktyce użytkownik podaje zakres review, wybiera głębokość i poziom ASVS, a agent szuka realnych ścieżek nadużycia w lokalnym kodzie. Raport rozdziela potwierdzone problemy od sygnałów, które wymagają dodatkowej walidacji poza samym repozytorium.

## Domyślna Konfiguracja

| Ustawienie | Domyślnie | Znaczenie | Przykłady |
| --- | --- | --- | --- |
| `Scope` | całe repo albo wskazany obszar | Część kodu objęta review. Im węższy scope, tym łatwiej o dokładniejsze prześledzenie przepływów. | całe repo, folder, aplikacja, API, moduł domenowy, backend + frontend |
| `Review Depth` | `standard` | Głębokość review i ilość czasu wydana na śledzenie wariantów [`quick`, `standard`, `deep`]. To nie jest severity wyniku. | `standard` dla zwykłego review, `deep` dla ważnego systemu |
| `ASVS Level` | `L2` | Poziom OWASP ASVS używany przy mapowaniu konkretnych znalezionych problemów [`L1`, `L2`, `L3`]. Nie jest checklistą sterującą całym review. | `L2` dla typowej aplikacji, `L3` dla silniejszych wymagań |
| `Tier Scope` | bez jawnego ograniczenia | Opcjonalny limit pracy do wybranych tierów z `risk-baseline.md` [`Tier 1`, `Tier 2`, `Tier 3`]. Używaj tylko wtedy, gdy chcesz świadomie zawęzić review względem `Review Depth`. | `Tier 1 i Tier 2 only` |
| `Report Language` | `Polish` | Opcjonalny parametr do świadomej zmiany języka narracji raportu. Bez tego parametru raport powstaje po polsku; nazwy pól i techniczne terminy pozostają w naturalnej formie. | `Polish`, `English` |
| Tryb | offline | Zakłada pracę na lokalnych plikach i kontekście od użytkownika [`offline`]. Runtime, skanery i chmura zwykle trafiają do osobnego follow-up. | offline review, osobny follow-up dla runtime/skanerów/chmury |
| `repomix` | opcjonalny | Spakowany widok repo jako pomoc w nawigacji po większym kodzie. Nie zastępuje lokalnych plików jako dowodu. | brak, istniejący output repomix |
| Lokalne instrukcje repo | obecne pliki instrukcji | Dodatkowy kontekst projektu, np. lokalne zasady pracy i struktura aplikacji. | `AGENTS.md`, `CLAUDE.md`, README, docs |
| Skille | `sec-appsec-review`, `sec-reporting`, `sec-asvs-review` | Minimalny zestaw aktywny dla typowego review: prowadzenie review, raport i mapowanie ASVS. | zestaw `sec-*` |
| Pliki wyjściowe | `docs/appsec/...` w promptach | Miejsce na zapis promptu i raportu, żeby dało się odtworzyć zakres review. | `{data_iso}_{aplikacja}-prompt.md`, `{data_iso}_{aplikacja}.md` |

`standard` i `L2` są dobrym punktem startowym dla zwykłej aplikacji biznesowej. `quick` pasuje do szybkiego przeglądu albo małego scope'u. `deep` pasuje do ważnego systemu, większego ryzyka albo drugiego przejścia po kodzie. `L3` ma sens przy silniejszych wymaganiach bezpieczeństwa albo sweepie architektonicznym.

## Pojęcia

| Pojęcie | Krótko |
| --- | --- |
| `Review Depth` | Profil kosztu i pokrycia review [`quick`, `standard`, `deep`]. |
| `ASVS Level` | Poziom wymagań używany przy mapowaniu znalezionego problemu [`L1`, `L2`, `L3`]. |
| `Tier Scope` | Ograniczenie pracy do wskazanych tierów z `risk-baseline.md` [`Tier 1`, `Tier 2`, `Tier 3`], np. `Tier 1 i Tier 2`. |
| `Report Language` | Opcjonalna zmiana języka narracji raportu. Domyślnie raport jest po polsku; standardowe pola, klasy podatności, nazwy narzędzi, API, konfiguracje i identyfikatory kodu pozostają stabilne. |
| `Finding` | Potwierdzona podatność lub materialne ryzyko z lokalnym dowodem i realistyczną ścieżką nadużycia. |
| `Candidate Finding` | Prawdopodobna podatność z lokalnym dowodem, ale bez pełnego potwierdzenia. |
| `Observation` | Krótki sygnał o hardeningu, posture, częściowym dowodzie albo osłabionej kontroli. |
| `Follow-up` | Zadanie walidacyjne zależne od runtime, produkcji, skanera, chmury/SaaS, dostępu albo aktualnej dokumentacji. |
| `Evidence Gate` | Próg dowodu wymagany do uznania problemu za `Finding`. Szczegóły są w skillach. |
| `Risk Baseline` | Lokalny model priorytetów opisany w `risk-baseline.md`. Pomaga zacząć od obszarów zwykle najbardziej opłacalnych w review, bez zamiany pracy w checklistę. |
| `Always Check` | Mała przypominajka w `always-check.md` dla oczywistych klas ryzyka, wybieranych tylko wtedy, gdy pasują do technologii, powierzchni i scope'u. |
| `Out of Scope` | Część systemu albo klasa ryzyka poza ustalonym zakresem danego review. |

`Review Depth`, `ASVS Level` i `Tier Scope` opisują różne rzeczy. `Review Depth` mówi o głębokości pracy, `ASVS Level` o poziomie mapowania standardu, a `Tier Scope` jest opcjonalnym limitem obszarów ryzyka. Żadne z tych pól samo nie oznacza severity. Severity wynika z wpływu, exploitability i kontekstu aplikacji.

Najczęściej wystarczy podać `Review Depth`. `Tier Scope` dodawaj tylko jako świadome zawężenie, np. gdy chcesz szybki przebieg ograniczony do `Tier 1` albo focused review bez wychodzenia poza `Tier 1` i `Tier 2`.

Raport ma cztery główne typy wyników. `Finding` to wynik najmocniejszy, bo ma lokalny dowód i realistyczną ścieżkę nadużycia. `Candidate Finding` jest blisko findingu, ale brakuje jednego ważnego potwierdzenia, np. konfiguracji produkcyjnej albo reachability. `Observation` jest lżejszym sygnałem. `Follow-up` opisuje sprawdzenie, którego nie da się rozstrzygnąć z samego repo.

Szczegóły progów, pól raportu i zasad klasyfikacji są w skillach. `SEC-README.md` jest krótką dokumentacją użytkową, a nie źródłem reguł pracy agenta.

## Prompty

W promptach zwykle zmienia się tylko `Scope`, `Review Depth`, `ASVS Level` i nazwę aplikacji/scope.

### 1. Całe Repo

```text
Cel: użyj $sec-appsec-review do szerokiego AppSec review całego repo. Priorytetem jest znalezienie jak najwięcej realnych, exploitable podatności w jednym przebiegu.

Scope: całe repo.
Review Depth: standard
ASVS Level: L2
Tryb: offline, bez internetu, GitHuba, SaaS, runtime access i zewnętrznych skanerów podczas zwykłego review.

Stosuj lokalne instrukcje repo, takie jak `AGENTS.md`, `CLAUDE.md`, README i lokalne wskazówki. Użyj `repomix` jeśli jest dostępny, zgodny z instrukcjami repo i realnie przydatny.

Priorytetyzuj pracę według tierów z baseline $sec-appsec-review.

Nie implementuj poprawek. Raportuj tylko problemy z lokalnym dowodem i realistyczną ścieżką nadużycia jako `Findings`. Prawdopodobne podatności bez pełnego potwierdzenia przenieś do `Candidate Findings`; hardening i częściowe sygnały do `Observations`; walidacje zależne od runtime, środowiska, skanerów, chmury/SaaS albo aktualnej dokumentacji do `Follow-up`.

Zwróć raport po polsku z sekcjami `Findings`, `Candidate Findings`, `Observations` i `Follow-up`.

Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

### 2. Wskazany Scope

```text
Cel: użyj $sec-appsec-review do AppSec review wskazanego obszaru. Priorytetem jest znalezienie jak najwięcej realnych, exploitable podatności w tym zakresie.

Scope: `<opisz scope, np. foldery, jedna aplikacja, jedno API, web app, route group, moduł domenowy albo backend project + odpowiadający frontend>`.
Review Depth: standard
ASVS Level: L2
Report Language: Polish
Tryb: offline, bez internetu, GitHuba, SaaS, runtime access i zewnętrznych skanerów podczas zwykłego review.

Stosuj lokalne instrukcje repo, takie jak `AGENTS.md`, `CLAUDE.md`, README i lokalne wskazówki. Użyj `repomix` jeśli jest dostępny, zgodny z instrukcjami repo i realnie przydatny.

Priorytetyzuj pracę według tierów z baseline $sec-appsec-review, zgodnie z `Review Depth`.

Nie implementuj poprawek. Raportuj tylko problemy z lokalnym dowodem i realistyczną ścieżką nadużycia jako `Findings`. Prawdopodobne podatności bez pełnego potwierdzenia przenieś do `Candidate Findings`; hardening i częściowe sygnały do `Observations`; walidacje zależne od runtime, środowiska, skanerów, chmury/SaaS albo aktualnej dokumentacji do `Follow-up`.

Zwróć raport po polsku z sekcjami `Findings`, `Candidate Findings`, `Observations`, `Follow-up` oraz `Out of Scope`, jeśli występuje.

Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
```

### 3. Dodatkowy Sweep Architektoniczny

Ten prompt pokazuje przykład focused sweepu dla rzadszych klas ryzyka. Lista obszarów jest zakresem tego przebiegu, nie stałym katalogiem do mechanicznego wykonywania w każdym review.

```text
Cel: użyj $sec-appsec-review do dodatkowego sweepu całego repo dla rzadszych albo architektonicznych klas ryzyka. To jest uzupełnienie głównego review, nie zamiennik.

Scope: całe repo, ale tylko pod kątem request smuggling, cache poisoning, unsafe proxy/header trust, host/header confusion, sandbox escapes, unsafe native/process isolation, parser differentials, unusual deserialization/parser behavior, advanced crypto misuse, multi-service trust boundaries, deployment/IaC-only risks i reverse-proxy-only security assumptions.

Review Depth: standard
ASVS Level: L3
Tryb: offline, bez internetu, GitHuba, SaaS, runtime access i zewnętrznych skanerów podczas zwykłego review.

Stosuj lokalne instrukcje repo, takie jak `AGENTS.md`, `CLAUDE.md`, README i lokalne wskazówki. Użyj `repomix` jeśli jest dostępny, zgodny z instrukcjami repo i realnie przydatny.

Najpierw sprawdź, czy dana klasa ryzyka ma realną powierzchnię w repo. Nie raportuj spekulacyjnych `Findings`; użyj `Candidate Findings`, krótkich `Observations` albo `Follow-up`, gdy brakuje pełnego potwierdzenia.

Zwróć raport po polsku z sekcjami `Findings`, `Candidate Findings`, `Observations` i `Follow-up`.

Zapisz raport w `docs/appsec/{data_iso}_{aplikacja}.md`.
Zapisz użyty prompt w `docs/appsec/{data_iso}_{aplikacja}-prompt.md`.
```

## Źródła I Odświeżanie

Internet, Context7 i zewnętrzne źródła są przydatne przy tworzeniu albo odświeżaniu referencji. Normalne review pozostaje offline.

| Obszar | Źródło |
| --- | --- |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ |
| OWASP ASVS releases | https://github.com/OWASP/ASVS/releases |
| OWASP Web Top 10:2025 | https://owasp.org/Top10/2025/ |
| OWASP API Security Top 10:2023 | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ |
| OWASP WSTG stable | https://owasp.org/www-project-web-security-testing-guide/stable/ |
| asvs-security-review-skill inspiration | https://github.com/OdellMoreno/asvs-security-review-skill |
| Microsoft Learn ASP.NET Core security | https://learn.microsoft.com/en-us/aspnet/core/security/ |
| Angular security | https://angular.dev/best-practices/security |
| npm audit | https://docs.npmjs.com/cli/v11/commands/npm-audit/ |
| CodeQL CLI/docs | https://docs.github.com/en/code-security/codeql-cli |
| Semgrep docs | https://semgrep.dev/docs/ |
