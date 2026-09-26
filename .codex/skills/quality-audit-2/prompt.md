```text
Użyj skilla $quality-audit-2 jako jedynego źródła metodyki skanowania, walidacji findingów i formatu raportu.

# Parametry

- MODULE_ROOT: HangFire/
- MAX_AREAS: 6
- LLM_APP: codex
- LLM_MODEL: luna
- LLM_MODEL_EFFORT: max
- OUTPUT_FOLDER: skany/
- OUTPUT_STEM: audit-<LLM_APP>-<LLM_MODEL>-<LLM_MODEL_EFFORT>-after-<RUN_ID>; ustal raz na początku
- RUN_ID: <YYYY-MM-DD-HHmm>; ustal raz na początku według Europe/Warsaw i używaj niezmiennie.

# Zakres

Wyszukuj, weryfikuj i raportuj findingi wyłącznie w `MODULE_ROOT` oraz jego podkatalogach. Kod poza `MODULE_ROOT` wolno czytać tylko jako kontekst konieczny do prześledzenia wywołania; nie wolno w nim szukać ani zgłaszać findingów. Finding należy do `MODULE_ROOT` tylko wtedy, gdy jego przyczyna i lokalizacja znajdują się w `MODULE_ROOT`; w przeciwnym razie go pomiń. Wszystkie obszary poszukiwań muszą być podkatalogami `MODULE_ROOT`, a deduplikacja i weryfikacja odrzucają findingi spoza tej ścieżki.

`MODULE_ROOT` to wyłączna granica audytu.

# Zasady

1. Agent główny koordynuje pracę, ale nie analizuje ponownie kodu, nie ocenia dowodów, nie wykonuje deduplikacji i nie zmienia finalnych statusów nadanych przez subagentów weryfikujących.
2. Subagenci zapisują pełne wyniki swoich analiz do osobnych plików tymczasowych.
3. Agent wiodący dzieli pracę poszukiwań na określoną maksymalną ilość obszarów poszukiwań MAX_AREAS i ich nie zwiększa. Podział opieraj na przewidywanym nakładzie analizy — liczbie i złożoności przepływów, punktów wejścia oraz zależności. Celem jest możliwie równy rozkład pracy między subagentów; szczególnie złożony komponent może stanowić osobny obszar.
4. Faza poszukiwań działa w grupach obszarów. Jednocześnie może pracować maksymalnie 6 subagentów poszukiwawczych (to nie to samo co MAX_AREAS).
5. Faza weryfikacji działa w grupach findingów. Jednocześnie może pracować maksymalnie sześciu subagentów weryfikujących.
6. Jeden subagent weryfikujący otrzymuje maksymalnie 5 findings z tego samego lub powiązanego obszaru.
7. Po zakończeniu poszukiwań agent główny przekazuje subagentowi deduplikującemu informacje o wszystkich plikach z wynikami. Subagent deduplikujący zwraca kompletny, zdeduplikowany zestaw findings:
   - w miejscach wymagających rozstrzygnięcia weryfikuje findings na podstawie kodu źródłowego i bezpośrednich zależności, a nie tylko opisów subagentów, ale tylko w zakresie koniecznym do potwierdzenia lub odrzucenia duplikacji;
   - łączy findings dotyczące tego samego błędu lub przyczyny, także gdy występują w różnych miejscach albo przepływach;
   - zachowuje różne skutki, lokalizacje i dowody;
   - nie łączy findings wymagających różnych poprawek;
   - jeżeli nie może rozstrzygnąć, czy findings dotyczą tego samego problemu, pozostawia je jako oddzielne findings;
   - dla każdego scalenia podaje krótkie uzasadnienie.
8. Pierwszy subagent może nadać wstępny status `confirmed` albo `needs-verification`, ale status ten nie jest finalny.
9. Każdy finding po deduplikacji musi zostać niezależnie sprawdzony przez subagenta weryfikującego. Subagent weryfikujący aktywnie próbuje finding obalić i stosuje Evidence Gate ze skilla $quality-audit-2. Finding pozostaje `confirmed` tylko wtedy, gdy po próbie falsyfikacji nadal spełnia wszystkie wymagania Evidence Gate.
10. Agent główny tworzy wyłącznie raport końcowy. Nie zmienia treści ani finalnych decyzji subagentów weryfikujących.
11. W przypadku błędu `Error - stream disconnected before completion: stream closed before response.completed` nie rozpoczynaj pracy nowego agenta tylko prześlij mu polecenie żeby kontynuował.
12. Podczas tej pracy nie zapisywane są żadne pliki `.json` (mimo, że skill $quality-audit-2 o tym wspomina)
13. Ustaw maksymalny timeout dla subagentów i bezwzględnie czekaj aż agenci zakończą pracę bez wysyłania poleceń nakazujących kończenie pracy.
14. Wszystkie pliki zapisywane są w folderze OUTPUT_FOLDER
15. Agent wiodący wykonuje pracę od początku do końca, nie zatrzymując się.
16. Wszystkie findingi w raporcie końcowym zapisywane są w formacie:

### F-nn - Tytuł

- Severity: low | medium | high | critical
- Confidence: confirmed | needs-verification
- Location: względna ścieżka pliku, klasa/metoda, numer linii
- Evidence: konkretny dowód w kodzie
- Risk/Impact: opis ryzyka lub skutku
- Risk Path:
  punkty opisujące risk path
- Recommendation: konkretna rekomendacja naprawy
- Effort: small | medium | large

---

# Algorytm

1. Agent główny wykonuje preflight i dzieli zakres na maksymalnie MAX_AREAS obszarów poszukiwań.
2. Przed uruchomieniem każdej fali poszukiwań wyświetla listę przydzielanych obszarów.
3. Uruchamia maksymalnie 6 subagentów poszukiwawczych równocześnie.
4. Każdy subagent analizuje swój obszar i zapisuje wynik do pliku:

`OUTPUT_STEM-agent-<PACKAGE_ID>-<AGENT_ID>.tmp.md`

5. Agent główny sprawdza technicznie zapisane pliki, zamyka zakończonych subagentów i uruchamia kolejną falę poszukiwań, jeżeli pozostały niezbadane obszary.
6. Po zakończeniu wszystkich fal poszukiwań agent główny przekazuje subagentowi deduplikującemu informacje o wszystkich plikach z wynikami oraz polecenie zwrócenia kompletnych findings po deduplikacji.
7. Subagent deduplikujący analizuje przekazane wyniki oraz, w razie potrzeby, kod źródłowy i bezpośrednie zależności. Zapisuje kompletny zdeduplikowany wynik do osobnego pliku tymczasowego `.tmp.md` i zwraca agentowi głównemu ścieżkę tego pliku.
8. Agent główny tworzy grupy do weryfikacji obejmujące wszystkie findings po deduplikacji.
9. Dzieli findings do weryfikacji na grupy po maksymalnie 5 elementów z tego samego lub powiązanego obszaru.
10. Przed uruchomieniem każdej fali weryfikacji wyświetla wyłącznie tytuły findings przeznaczonych do sprawdzenia.
11. Uruchamia maksymalnie sześciu subagentów weryfikujących równocześnie wyznaczone obszary weryfikacji.
12. Każdy subagent weryfikujący samodzielnie sprawdza przydzielone findings, aktywnie próbuje je obalić i stosuje Evidence Gate ze skilla $quality-audit-2. Zwraca wynik podając dla każdego findingu status:
   - `confirmed`;
   - `dismissed`;
   - `needs-verification`, jeżeli sprawdzenie nadal nie rozstrzygnęło sprawy,
   poziom błędu z uzasadnieniem,
   effort.
13. Fale weryfikacji są uruchamiane kolejno aż do wyczerpania wszystkich grup.
14. Agent główny przenosi finalne decyzje subagentów weryfikujących do raportu bez ponownej analizy.
15. Tworzy wyłącznie `OUTPUT_STEM.md` bez findingów dismissed, usuwa pliki tymczasowe z bieżącego uruchomienia i podaje końcowe statystyki.
