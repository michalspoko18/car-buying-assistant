# Specyfikacja wymagań (SRS)
## Aplikacja do oceny dopasowania samochodu do potrzeb kupującego

**Wersja:** 0.1.0  
**Data:** 2026-01-22  
**Autorzy:** Andrzej Jur, Michał Walczak  
**Zakres zmian:** Inicjalizacja dokumentu SRS wraz z identyfikacją funkcji systemu na podstawie aktualnej implementacji.

## Spis treści
1. Wprowadzenie
   1.1 Cel
   1.2 Przyjęte konwencje
   1.3 Zakres projektu
   1.4 Odwołania
2. Opis ogólny
   2.1 Perspektywa produktu
   2.2 Klasy i charakterystyki użytkowników
   2.3 Środowisko działania
   2.4 Ograniczenia projektowe i wykonawcze
   2.5 Założenia i zależności
3. Funkcjonalności systemu
4. Wymagania dotyczące danych
   4.1 Logiczny model danych
   4.2 Raporty
   4.3 Pozyskiwanie, integralność przechowywanie i usuwanie danych
5. Wymagania dotyczące interfejsu zewnętrznego
   5.1 Interfejsy użytkownika
   5.2 Interfejsy programowe
   5.3 Interfejsy sprzętowe
   5.4 Interfejsy komunikacyjne
6. Cechy jakości
   6.1 Użyteczność
   6.2 Wydajność
   6.3 Zabezpieczenia
   6.4 Bezpieczeństwo użytkowania
   6.5 Inne
7. Wymagania internacjonalizacji i lokalizacji
8. Inne wymagania
Suplement A: Słownictwo
Suplement B: Modele analityczne

---

## 1. Wprowadzenie
### 1.1 Cel
Celem systemu jest wsparcie osoby planującej zakup samochodu w ocenie, czy dany model odpowiada jej priorytetom. Użytkownik wybiera cechy, które są dla niego najważniejsze, wskazuje konkretny model auta (na podstawie katalogu marek/ modeli/ wersji), a system generuje raport AI z oceną dopasowania, plusami, minusami, ryzykami oraz orientacyjnymi kosztami eksploatacji. System działa jako aplikacja webowa oparta o Django templates i nie wymaga zakładania kont.

Odbiorcy dokumentu: analitycy, projektanci UX/UI, programiści, testerzy, osoby wdrażające, właściciele produktu.

### 1.2 Przyjęte konwencje
- Wymagania funkcjonalne oznaczono jako **FR-XX**.
- Wymagania niefunkcjonalne oznaczono jako **NFR-XX**.
- Kluczowe pojęcia zdefiniowano w suplemencie A.

### 1.3 Zakres projektu
System obejmuje proces: wybór auta + preferencje → generowanie raportu AI → prezentacja raportu → eksport do PDF. Zakres ogranicza się do wersji MVP i nie obejmuje kont użytkowników ani historii raportów. Dokument dotyczy modułów webowych aplikacji, które realizują powyższe funkcje.

### 1.4 Odwołania
- Dokumentacja Django
- Dokumentacja OpenAI API
- Dokumentacja pdfkit / wkhtmltopdf

## 2. Opis ogólny
### 2.1 Perspektywa produktu
Produkt jest niezależną aplikacją webową (SSR) działającą w ramach jednego serwisu Django. System korzysta z lokalnej bazy danych „car2db” zawierającej katalog marek, modeli, generacji, serii, modyfikacji i wyposażenia.

### 2.2 Klasy i charakterystyki użytkowników
- **Użytkownik anonimowy:** osoba rozważająca zakup samochodu, nie wymaga logowania.
- **Administrator systemu:** utrzymanie środowiska, konfiguracja kluczy API, instalacja zależności do PDF.

### 2.3 Środowisko działania
- Backend: Python + Django (renderowanie po stronie serwera).
- Frontend: HTML/CSS generowany przez Django templates.
- Baza danych: SQLite („car2db”) wykorzystywana tylko do odczytu katalogu aut.
- Integracje: OpenAI API (raport AI), pdfkit + wkhtmltopdf (PDF).

### 2.4 Ograniczenia projektowe i wykonawcze
- Brak kont użytkowników i trwałego przechowywania danych osobowych.
- Raport AI generowany jest w stałym schemacie sekcji.
- PDF generowany przy użyciu wkhtmltopdf (wymaga instalacji narzędzia zewnętrznego).

### 2.5 Założenia i zależności
- Klucz API OpenAI jest dostępny w zmiennych środowiskowych.
- Baza „car2db” jest dostępna w konfiguracji Django jako źródło danych katalogowych.
- wkhtmltopdf jest zainstalowany lokalnie lub wskazany w zmiennej `WKHTMLTOPDF_CMD`.

## 3. Funkcjonalności systemu
Poniżej opisano funkcje zidentyfikowane w systemie i możliwe do opisania w SRS.

### 3.1 Wybór danych samochodu
**Opis:** Użytkownik wybiera samochód z katalogu marek i modeli (zależne listy wyboru). Priorytet: wysoki.

**Wymagania funkcjonalne:**
- **FR-01:** System udostępnia listę marek pojazdów na podstawie katalogu danych.
- **FR-02:** Po wyborze marki system udostępnia listę modeli danej marki.
- **FR-03:** Po wyborze modelu system udostępnia listę generacji.
- **FR-04:** Użytkownik może wybrać serię, modyfikację oraz wyposażenie (opcjonalnie).
- **FR-05:** System pozwala kontynuować proces nawet wtedy, gdy użytkownik pominie część wyborów (wartości opcjonalne).

### 3.2 Preferencje kupującego (zaawansowane opcje)
**Opis:** Użytkownik może wskazać priorytety poprzez wybór wartości w grupach preferencji. Priorytet: średni.

**Wymagania funkcjonalne:**
- **FR-06:** System udostępnia opcjonalne, pogrupowane wybory preferencji (ekonomia, praktyczność, niezawodność, osiągi, styl użytkowania, komfort).
- **FR-07:** Użytkownik może nie wybierać żadnej preferencji (brak wymuszenia).
- **FR-08:** System zapisuje zestaw wybranych preferencji i przekazuje je do generowania raportu.

### 3.3 Generowanie raportu AI
**Opis:** System generuje raport dopasowania na podstawie danych auta i preferencji. Priorytet: wysoki.

**Wymagania funkcjonalne:**
- **FR-09:** System buduje prompt zawierający dane auta i preferencje.
- **FR-10:** System wysyła zapytania do API AI i oczekuje zwrotu danych w formacie JSON.
- **FR-11:** Raport zawiera sekcje: dopasowanie (ocena i podsumowanie), plusy, minusy, ryzyka, koszty eksploatacji, profil użytkownika, rekomendacja.
- **FR-12:** System powinien obsłużyć sytuację, gdy AI zwróci niepełne dane (brakujące sekcje prezentowane jako „Brak danych”).
- **FR-13:** System przechowuje wynik raportu w sesji użytkownika do czasu prezentacji i ewentualnego eksportu.

### 3.4 Prezentacja raportu
**Opis:** Raport jest wyświetlany użytkownikowi jako strona HTML. Priorytet: wysoki.

**Wymagania funkcjonalne:**
- **FR-14:** System prezentuje raport w czytelnym układzie sekcji.
- **FR-15:** System wyświetla tytuł i podsumowanie danych auta oraz preferencji.
- **FR-16:** W przypadku błędu generowania raportu system prezentuje komunikat w widoku raportu.

### 3.5 Eksport raportu do PDF
**Opis:** Użytkownik może pobrać raport w formacie PDF. Priorytet: średni.

**Wymagania funkcjonalne:**
- **FR-17:** System generuje PDF na podstawie HTML raportu.
- **FR-18:** PDF zawiera sekcje raportu wraz z tytułem i informacją o wybranym aucie.
- **FR-19:** System zwraca plik PDF jako odpowiedź do pobrania.
- **FR-20:** W przypadku braku zależności (pdfkit/wkhtmltopdf) system wyświetla komunikat błędu.

### 3.6 Obsługa błędów i walidacja
**Opis:** System waliduje formularze i informuje o błędach. Priorytet: średni.

**Wymagania funkcjonalne:**
- **FR-21:** System waliduje poprawność wyborów w formularzu (zgodność z listami wyboru).
- **FR-22:** System zabezpiecza formularze przed błędnymi żądaniami (CSRF).

## 4. Wymagania dotyczące danych
### 4.1 Logiczny model danych
Model logiczny bazuje na katalogu samochodów (marki, modele, generacje, serie, modyfikacje, wyposażenie) oraz na danych sesji zawierających zlecenie raportu.

### 4.2 Raporty
Raport AI zawiera sekcje:
- Ocena dopasowania (ocena liczbowo-opisowa + podsumowanie),
- Plusy,
- Minusy,
- Ryzyka,
- Szacunkowe koszty eksploatacji i serwisu,
- Dla kogo / nie dla kogo,
- Podsumowanie i rekomendacja.

### 4.3 Pozyskiwanie, integralność przechowywanie i usuwanie danych
- Dane katalogowe są tylko odczytywane z lokalnej bazy „car2db”.
- Dane raportu przechowywane są tymczasowo w sesji użytkownika.
- Brak trwałego zapisu danych osobowych.

## 5. Wymagania dotyczące interfejsu zewnętrznego
### 5.1 Interfejsy użytkownika
- Formularz wyboru auta i preferencji.
- Widok raportu (HTML).
- Przycisk/akcja eksportu do PDF.

### 5.2 Interfejsy programowe
- OpenAI API do generowania raportu.
- pdfkit + wkhtmltopdf do generowania pliku PDF.

### 5.3 Interfejsy sprzętowe
Brak specyficznych wymagań sprzętowych.

### 5.4 Interfejsy komunikacyjne
- Protokół HTTPS do komunikacji z API AI.

## 6. Cechy jakości
### 6.1 Użyteczność
- Prosty, liniowy przepływ: wybór auta → preferencje → raport.
- Raport prezentowany w czytelnych sekcjach.

### 6.2 Wydajność
- Raport generowany w akceptowalnym czasie (kilka–kilkanaście sekund).

### 6.3 Zabezpieczenia
- Brak gromadzenia danych osobowych.
- Klucz API przechowywany w zmiennych środowiskowych.
- Ochrona CSRF dla formularzy.

### 6.4 Bezpieczeństwo użytkowania
- Raport ma charakter pomocniczy i nie stanowi gwarancji stanu technicznego pojazdu.

### 6.5 Inne
- Czytelność PDF: marginesy, format A4 i kodowanie UTF-8.

## 7. Wymagania internacjonalizacji i lokalizacji
- Język bazowy: polski.
- Format waluty: PLN.
- Możliwość późniejszej lokalizacji poprzez zasoby tekstowe.

## 8. Inne wymagania
- Aplikacja nie wymaga logowania i nie tworzy profili użytkowników.

## Suplement A: Słownictwo
- **Preferencje** – zestaw priorytetów określonych przez użytkownika.
- **Raport** – wynik analizy dopasowania auta do potrzeb kupującego.
- **Token** – jednostka rozliczeniowa API AI.

## Suplement B: Modele analityczne
- Diagram danych katalogowych (marka → model → generacja → seria → modyfikacja → wyposażenie).
- Diagram przepływu procesu użytkownika (formularz → raport → PDF).
