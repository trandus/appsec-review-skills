# Wytyczne Repozytorium

## Struktura Projektu I Organizacja Modułów

To repozytorium zawiera przenośny zestaw skilli Codex do lokalnego AppSec review. Główny plik `SEC-README.md` opisuje zestaw skilli, prompty review, poziomy ASVS i format raportów. Implementacje skilli znajdują się w `.codex/skills/`:

- `.codex/skills/sec-appsec-review/` orkiestruje review i zawiera główne referencje.
- `.codex/skills/sec-repo-recon/` służy do rozpoznania struktury repozytorium.
- `.codex/skills/sec-asvs-review/` zawiera lokalny lookup ASVS, `references/asvs-5.0.0-local.json` i `scripts/asvs_lookup.py`.
- `.codex/skills/sec-reporting/` definiuje format raportu i szablony.

Każdy skill powinien trzymać główne instrukcje w `SKILL.md`, opcjonalną konfigurację agenta w `agents/openai.yaml`, a materiały pomocnicze w `references/` albo `scripts/`.

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
