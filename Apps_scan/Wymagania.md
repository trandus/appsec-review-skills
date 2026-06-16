## Cel zadania

Przeprowadzenie ustandaryzowanego przeglądu kodu aplikacji z wykorzystaniem modelu GPT-5.5 w celu identyfikacji ryzyk technicznych, problemów jakościowych oraz obszarów do usprawnień, a także przygotowanie rekomendacji wspierających dalszy rozwój i utrzymanie aplikacji.

---

## Zakres prac

- Analiza struktury projektu oraz architektury aplikacji
  -> zad. 2

- Ocena jakości kodu źródłowego
  -> zad. 2

- **Identyfikacja:**
  - potencjalnych błędów (bugów) i antywzorców
    -> zad. 2

  - problemów bezpieczeństwa
    -> zad. 1

  - problemów wydajnościowych
    -> zad. 2

  - duplikacji kodu
    -> SonarQube

  - nadmiernej złożoności
    -> SonarQube

  - martwego lub nieużywanego kodu
    -> IDE + SonarQube

- **Ocena:**
  - czytelności i utrzymywalności (maintainability)
    -> IDE + SonarQube

  - zgodności ze standardami zespołu
    -> do doprecyzowania

  - jakości testów
    -> zad. 2

  - sposobu obsługi błędów i mechanizmów logowania
    -> zad. 2

  - wykorzystywanych zależności i bibliotek
    -> zad. 3 / BlackDuck

- Wskazanie szybkich usprawnień („quick wins”)
  -> raporty zad. 1 i 2

- Przygotowanie podsumowania technicznego aplikacji
  -> raporty zad. 1 i 2

---

## Oczekiwany rezultat

Raport zawierający:

- ogólną ocenę jakości aplikacji
  -> zad. 2

- listę kluczowych problemów i ryzyk
  -> zad. 1 oraz zad. 2

- rekomendacje usprawnień
  -> zad. 1 oraz zad. 2

- propozycję priorytetów technicznych
  -> zad. 2

- listę obszarów wymagających refaktoryzacji
  -> zad. 2

- oszacowanie poziomu długu technologicznego (niski / średni / wysoki)
  -> zad. 2 + SonarQube

- raport podatnych lub nieaktualnych zależności
  -> zad. 3 / BlackDuck

---

## Definition of Done

- Kod aplikacji został przeanalizowany z wykorzystaniem modelu GPT-5.5
  -> zad. 1 oraz zad. 2

- Przygotowano raport podsumowujący analizę
  -> zad. 1, zad. 2, zad. 3

- Zidentyfikowane problemy zostały skategoryzowane według priorytetu
  -> zad. 1 oraz zad. 2

- Raport został zapisany w uzgodnionej lokalizacji – dokumentacja umieszczona w tym zgłoszeniu oraz repozytorium aplikacji
  -> wszystkie zadania