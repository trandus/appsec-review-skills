# Wytyczne Repozytorium

## Struktura Projektu I Organizacja Modułów

To repozytorium zawiera przenośny zestaw skilli Codex do lokalnego AppSec review. Główny plik `SEC-README.md` jest dokumentacją użytkową dla dewelopera: prostym językiem opisuje zestaw skilli, sposób działania, domyślną konfigurację, tłumaczone pojęcia konfiguracyjne, przykładowe prompty review i źródła do odświeżania referencji. Reguły normatywne pracy skilli mieszkają w `.codex/skills/`. Implementacje skilli znajdują się w `.codex/skills/`:

- `.codex/skills/sec-appsec-review/` orkiestruje review, zawiera wbudowany krótki etap rozpoznania repo i główne referencje.
- `.codex/skills/sec-asvs-review/` zawiera lokalny lookup ASVS, `references/asvs-5.0.0-local.json` i `scripts/asvs_lookup.py`.
- `.codex/skills/sec-reporting/` definiuje format raportu i szablony.

Każdy skill powinien trzymać główne instrukcje w `SKILL.md`, opcjonalną konfigurację agenta w `agents/openai.yaml`, a materiały pomocnicze w `references/` albo `scripts/`.

## Zasady Tworzenia Skilli

W tym repozytorium rozwijane i utrzymywane są skille z prefiksem `sec-*`. Skill `security-audit` jest wyłącznie przykładem referencyjnym i nie powinien być modyfikowany w ramach zwykłego rozwoju tego zestawu.

Skille mają być możliwie proste i przenośne. Nie próbuj przepisywać całej wiedzy AppSec do instrukcji skilla. Skill powinien dawać LLM-owi dobre hasła, tropy, zakresy, priorytety i ogólne nakierowanie na to, czego ma szukać, a nie zamieniać review w sztywną checklistę wykonywaną bez rozumienia kontekstu.

`SEC-README.md` jest plikiem dla użytkowników i deweloperów korzystających z zestawu. Ma być napisany prostym językiem i zawierać sekcje: `Jak To Działa`, `Domyślna Konfiguracja`, `Pojęcia` z tłumaczeniem pojęć konfiguracyjnych oraz `Prompty` z przykładami do wklejenia. Ma dawać dość informacji, żeby użytkownik rozumiał parametry takie jak `Scope`, `Review Depth`, `ASVS Level`, `Tier Scope`, tryb offline, `repomix` i pliki wyjściowe. Szczegółowe progi findingów, evidence gate, format raportu i zasady prowadzenia review należą do odpowiednich skilli oraz ich referencji. Tam, gdzie poprawia to czytelność porównań albo konfiguracji, używaj tabel zamiast długich list opisowych.

Skille mają działać tak, żeby użytkownik nie musiał ręcznie wybierać konkretnych podatności do sprawdzenia. Zakres review powinien wynikać z konfiguracji, np. tieru, poziomu intensywności, poziomu ASVS L1/L2/L3, technologii, typu aplikacji albo innych jawnie zdefiniowanych ustawień. Prompt użytkownika może zawężać lub rozszerzać kontekst, ale podstawowy dobór obszarów bezpieczeństwa powinien wynikać z konfiguracji skilla.

W review istnieje wbudowany, bardzo krótki zestaw obszarów przypominających dla oczywistych, wysokozwrotnych podatności, które łatwo pominąć przy szukaniu bardziej złożonych problemów. Utrzymuj go jako jawny element referencji i dokumentuj jego położenie w `SEC-README.md` w krótkiej, użytkowej formie. Obecnym miejscem jest `.codex/skills/sec-appsec-review/references/always-check.md`. Nie rozszerzaj tego pliku do katalogu podatności; pełniejsza priorytetyzacja należy do `risk-baseline.md`. Obszary mają być dobierane do audytowanej aplikacji, technologii, wystawionych powierzchni i scope'u, a nie wykonywane mechanicznie w każdym review. Jeśli plik zostanie przeniesiony, zaktualizuj jednocześnie dokumentację i instrukcje skilla.

Na końcu `SEC-README.md` znajduje się lista linków z referencjami. Traktuj ją jako utrzymywaną część dokumentacji: dodawaj użyteczne źródła przy większych zmianach merytorycznych, usuwaj martwe albo przestarzałe odnośniki i pilnuj, żeby lista nadal wspierała offline-first AppSec review zamiast rozpraszać użytkownika.

## Komendy Budowania, Testów I Rozwoju

Repozytorium nie ma osobnego systemu budowania. Używaj ukierunkowanych sprawdzeń:

Każdą komendę PowerShell uruchamiaj bez profilu użytkownika, zawsze przez `pwsh -NoLogo -NoProfile -NonInteractive -Command "..."`. W narzędziu `shell_command` każda komenda PowerShell musi mieć `login: false`, bo inaczej zewnętrzna powłoka może załadować profil użytkownika przed uruchomieniem wewnętrznego `pwsh -NoProfile`. Dzięki temu `oh-my-posh`, PSReadLine, moduły terminalowe i lokalne aliasy nie zanieczyszczają wyników komend ostrzeżeniami ani błędami niezwiązanymi z repozytorium.

```powershell
pwsh -NoLogo -NoProfile -NonInteractive -Command "python .codex/skills/sec-asvs-review/scripts/asvs_lookup.py --level L2 --query authorization"
pwsh -NoLogo -NoProfile -NonInteractive -Command "git diff --check"
pwsh -NoLogo -NoProfile -NonInteractive -Command "rg 'TODO|FIXME' .codex SEC-README.md AGENTS.md"
```

Lookup ASVS sprawdza skrypt i lokalny dataset. `git diff --check` wykrywa problemy z białymi znakami. `rg` pomaga znaleźć niedokończone notatki w treści skilli.

## Styl Kodowania I Nazewnictwo

Pisz dokumentację w Markdownie, krótkimi sekcjami i konkretnymi punktami działania. Zachowuj nazwy folderów w stylu lowercase kebab-case oraz istniejący prefiks `sec-*`. Używaj poprawnych polskich znaków w polskiej dokumentacji. Skrypty Pythona powinny być małe, oparte głównie na bibliotece standardowej i mieć czytelne flagi `argparse`, np. `--level` oraz `--query`.

## Zasady Testowania

Po zmianach w danych ASVS albo logice lookupu uruchom reprezentatywne zapytania dla autoryzacji, injection, CSRF, logowania i zależności. Po edycji promptów lub szablonów ręcznie sprawdź, czy nadal występują wymagane pola: `Findings`, `Observations`, `Follow-up`, `Remediation`, `Regression Test` i `ASVS Mapping`. Pakiet ma działać offline po skopiowaniu do docelowego repozytorium, więc nie dodawaj obowiązkowych testów zależnych od sieci.

## Commity I Pull Requesty

Historia używa krótkich tematów commitów, np. `Fix prompts` oraz `Add security review references and reporting templates for AppSec assessments`. Temat commita powinien być zwięzły i wskazywać zmieniony skill albo obszar referencji. Pull request powinien opisywać zmienione skille, ewentualne aktualizacje datasetu ASVS, uruchomione komendy oraz wpływ na offline review.

## Bezpieczeństwo I Konfiguracja

Nie dodawaj sekretów, wyników review klientów ani prywatnych szczegółów repozytoriów do referencji i szablonów. Źródeł zewnętrznych można używać przy odświeżaniu referencji, ale zwykłe review powinno opierać się na lokalnych plikach i domyślnie działać offline.
