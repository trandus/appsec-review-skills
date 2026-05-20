# security-audit-3 - Opis

`security-audit-3` służy do lokalnego, exploit-path-first review kodu. Domyślnie działa offline, bez internetu, bez GitHuba, bez zewnętrznych skanerów i bez wprowadzania poprawek w kodzie, chyba że użytkownik jawnie poprosi inaczej.

## Parametry domyślne

| Parametr | Domyślnie | Znaczenie |
| --- | --- | --- |
| `Review Depth` | `standard` | Standardowy poziom pokrycia review. |
| Język raportu | polski | Chyba że podasz `Report Language: <language>`. |
| Plik raportu | `./security-audit-3-<YYYY-MM-DD-HHmm>.md` | Tworzony w katalogu głównego repozytorium. |
| Tryb pracy | offline/local only | Bez internetu, SaaS, GitHuba, runtime access i zewnętrznych skanerów. |

## Tiery

Tiery są warstwami priorytetu, nie przełącznikami wyłączającymi niższe poziomy.

| Tier | Kiedy jest używany | Skrót |
| --- | --- | --- |
| Tier 1 | Zawsze jako punkt startowy. | Najbardziej zwrotne ścieżki: auth/authz, IDOR/BOLA, tenant escape, tokeny, injection, XSS, SSRF, pliki, sekrety, debug/admin surfaces. |
| Tier 2 | Po Tier 1 albo gdy powierzchnia jest widoczna w scope. | Szersze standardowe pokrycie: operacje destrukcyjne, workflow bypass, ekspozycja danych, CSRF/CORS/cookies, zależności, abuse/rate limits, crypto i transport. |
| Tier 3 | Gdy `Review Depth` to `deep`, architektura to uzasadnia albo wcześniejsze tiery wskazują głębszy problem. | Bardziej systemowe ryzyka: proxy/cache/header trust, parsery, service-to-service, kolejki/eventy, izolacja workerów, distributed state, replay i stale auth. |

## Review Depth

| Wartość | Co oznacza |
| --- | --- |
| `quick` | Głównie Tier 1 oraz mała próbka oczywistych Tier 2. |
| `standard` | Odpowiedni Tier 1, reprezentatywny Tier 2 i wybrane Tier 3 pasujące do repo. To domyślny tryb. |
| `deep` | Szerzej Tier 1 i Tier 2, mocniejsze Tier 3 oraz więcej korelacji między warstwami, workflow, konfiguracją i deploymentem. |

`deep` ma sens dla aplikacji produkcyjnych, multi-tenant, płatności, danych wrażliwych, integracji, kolejek, webhooków, SSO/OIDC/OAuth, uploadów/importów, parserów, IaC albo przed ważnym releasem/audytem.

## Przykładowe prompty

### Standard, bez parametru

```text
Użyj $security-audit-3 i wykonaj lokalny review tego repozytorium. Raport do pliku.
```

### Deep

```text
Użyj $security-audit-3.
Review Depth: deep
Scope: <folder>
Wykonaj lokalny review wskazanego scope, możesz wychodzić poza scope tylko w uzasadnionych sytuacjach, gdy wymaga tego analiza wybranego obszaru. Zapisz raport do pliku.
```
