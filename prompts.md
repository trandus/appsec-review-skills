## Prompt porównania roportów

```
Porównaj dwa załączone raporty bezpieczeństwa IT / AppSec dotyczące tej samej aplikacji.

Cel:
Chcę ocenić nie tylko liczbę znalezionych problemów, ale też jakość raportu, kompletność analizy, wartość dowodową i przydatność do dalszych działań developerskich/security.

Raporty oznacz jako:
- Raport A
- Raport B
- Raport n (dla kolejnych, jeżeli występują)
Wstaw tablelce przypisanie nazwa raportu -> oznaczenie raportu

Nie zakładaj, że dłuższy raport jest lepszy. Oceń merytorycznie.

## 1. Krótki werdykt

Napisz krótko:
- który raport jest ogólnie lepszy,
- który raport ma lepsze findingi,
- który raport ma lepsze dowody,
- który raport jest bardziej przydatny do backlogu naprawczego,
- czy najlepszym rozwiązaniem jest wybór jednego raportu, czy połączenie obu.

## 2. Porównanie ogólne w tabeli

Porównaj raporty w tabeli według kategorii:

| Kategoria | Raport A | Raport B | Lepszy | Komentarz |
|---|---|---|---|---|

Kategorie do oceny:
- Zakres analizy
- Liczba findingów
- Jakość findingów
- Istotność znalezionych problemów
- Konkretność dowodów
- Lokalizacje w kodzie / plikach
- Ścieżki ataku / exploit path
- Ocena impactu biznesowego
- Remediacje
- Testy regresji
- Uwzględnienie IaC / deployment / konfiguracji środowiska
- Wykrywanie secrets / konfiguracji wrażliwej
- Rozróżnienie finding vs observation
- Mapowanie do OWASP / ASVS / kategorii ryzyka
- Czytelność raportu
- Przydatność dla zespołu developerskiego
- Przydatność dla security / audit

## 3. Porównanie findingów

Przygotuj tabelę:

| Problem / Finding | Raport A | Raport B | Severity wg raportów | Który opis lepszy | Komentarz |
|---|---|---|---|---|---|

Uwzględnij:
- findingi wspólne,
- findingi tylko z Raportu 1,
- findingi tylko z Raportu 2,
- findingi podobne, ale opisane innymi słowami.

Dla każdego findingu oceń:
- czy jest dobrze udowodniony,
- czy ma sensowną severity,
- czy ma realny exploit path,
- czy remediation jest konkretna,
- czy powinien trafić do finalnego raportu.

## 4. Ocena jakości findingów

Dla każdego raportu oceń jakość wykrytych problemów:

| Kryterium | Raport A | Raport B | Komentarz |
|---|---:|---:|---|

Skala: 1-5.

Kryteria:
- Trafność techniczna
- Istotność bezpieczeństwa
- Dowody w kodzie
- Dowody w konfiguracji / IaC
- Realistyczny attack path
- Realistyczny impact
- Konkretność remediation
- Możliwość przepisania na zadania developerskie
- Brak fałszywych alarmów
- Kompletność względem analizowanego scope

## 5. Ocena pokrycia obszarów bezpieczeństwa

Porównaj, które obszary zostały dobrze lub słabo pokryte:

| Obszar | Raport A | Raport B | Luka / komentarz |
|---|---|---|---|

Obszary:
- Authentication
- Authorization / access control
- Tenant isolation
- CSRF
- SSRF
- Input validation
- XML / deserialization
- Request size limits / DoS
- Secrets management
- Logging / privacy
- Swagger / debug endpoints
- CORS / headers / HTTPS
- Rate limiting
- Error handling
- Dependency / supply chain
- Cloud / IaC / deployment config
- Business logic abuse
- Test coverage / regression tests

## 6. Co każdy raport znalazł lepiej

Podaj dwie krótkie sekcje:

### Co Raport A zrobił lepiej
Wypunktuj najważniejsze przewagi Raportu 1.

### Co Raport B zrobił lepiej
Wypunktuj najważniejsze przewagi Raportu 2.

## 7. Czego brakuje w słabszym raporcie

Wskaż, co trzeba poprawić w każdym raporcie, żeby dorównał drugiemu.

Forma:

| Raport | Brak / słabość | Jak poprawić |
|---|---|---|

Nie opisuj zbyt długo. Skup się na praktycznych usprawnieniach skillu / procesu review.

## 8. Skonsolidowana lista finalnych findingów

Na końcu przygotuj rekomendowaną listę findingów do finalnego raportu:

| Priorytet | Finding | Severity | Źródło | Decyzja |
|---|---|---|---|---|

Priorytety:
- P1 — najpilniejsze
- P2 — ważne
- P3 — średnie / hardening
- Follow-up — wymaga dalszej walidacji

W kolumnie „Źródło” wpisz:
- Raport A
- Raport B
- Oba

W kolumnie „Decyzja” wpisz:
- zostawić,
- połączyć,
- doprecyzować,
- zdegradować do observation,
- odrzucić jako słabo udowodnione.

## 9. Ocena końcowa

Podaj krótką ocenę końcową:

- Lepszy raport ogólnie:
- Lepszy raport pod względem liczby findingów:
- Lepszy raport pod względem jakości findingów:
- Lepszy raport pod względem dowodów:
- Lepszy raport pod względem użyteczności dla developerów:
- Lepszy raport pod względem security/audit:
- Najlepsza strategia: wybrać jeden / połączyć oba / uruchomić kolejny review

## Zasady odpowiedzi

- Pisz po polsku.
- Używaj tabel tam, gdzie to ma sens.
- Nie streszczaj całych raportów.
- Nie rozwlekaj się.
- Skup się na porównaniu jakości i przydatności.
- Jeżeli coś nie wynika z raportów, napisz, że nie da się tego ocenić.
- Nie wymyślaj findingów, których nie ma w raportach.
- Jeżeli jeden raport ma lepszy finding, ale drugi ma lepsze dowody, zaznacz to wyraźnie.
- Jeżeli raport zawiera observation/follow-up, nie traktuj tego automatycznie jako confirmed finding.
```

## Review spójności i jakości skillów AppSec

```
# Review spójności i jakości skillów AppSec sec-* i SEC-README.md (jako instrukcji i dokumentacji dla użytkownika)

Jesteś doświadczonym specjalistą IT Security / AppSec.

Tworzę skille do przeglądów repozytoriów aplikacji. Chcę, abyś przeprowadził review aktualnej wersji skillów `sec-*`.

Na razie niczego nie zmieniaj. Najpierw wykonaj dogłębną analizę i przedstaw wnioski.

Podczas analizy trzymaj się zasad opisanych w plikach typu `AGENTS.md`, `CLAUDE.md` lub podobnych instrukcjach repozytorium. Jeżeli zasady repozytorium są sprzeczne ze skillem, wskaż to jako problem.

Sprawdź szczególnie:

- czy treść jest konsekwentna i zrozumiała,
- czy nie ma sprzeczności, powtórzeń lub duplikatów,
- czy opisy nie są zbyt długie, szczegółowe albo skomplikowane,
- czy skille `sec-*` nie wymuszają zbyt sztywnej procedury działania,
- czy zachowują charakter ogólnych zasad, kierunków i obszarów analizy,
- czy pozostawiają LLM swobodę decyzji, co dokładnie sprawdzić i jak przeprowadzić review,
- czy nie zawierają zbyt domenowych lub przypadkowych założeń.

Celem skillów `sec-*` nie jest stworzenie checklisty krok po kroku, ale nadanie LLM dobrego kierunku pracy: wskazanie obszarów, sposobu myślenia, oczekiwanej jakości analizy i formy raportowania.

W odpowiedzi podaj krótko:

1. Najważniejsze problemy.
2. Miejsca niespójne lub niejasne.
3. Elementy zbyt szczegółowe lub zbyt proceduralne.
4. Niezgodności z zasadami repozytorium, w szczególności z `AGENTS.md`, `CLAUDE.md` lub podobnymi instrukcjami.
5. Sugestie kierunków poprawy, bez przepisywania treści skillów.
```