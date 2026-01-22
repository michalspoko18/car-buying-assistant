# Instrukcja wdrożeniowa (Anaconda)

Poniższa instrukcja zakłada uruchomienie aplikacji na maszynie z zainstalowaną Anacondą/Minicondą. Projekt jest aplikacją Django i korzysta z klucza API OpenAI oraz opcjonalnego generowania PDF przez `wkhtmltopdf`.

## Wymagania wstępne

- Anaconda lub Miniconda (polecane).
- Python 3.11 (instalowany w środowisku conda).
- `wkhtmltopdf` (tylko jeśli potrzebujesz eksportu do PDF).
- Dostęp do internetu (instalacja zależności).

## Szybki start (skrypt)

1. Przejdź do katalogu repozytorium.
2. Uruchom skrypt bootstrapujący środowisko:

```bash
./scripts/conda_bootstrap.sh
```

Skrypt:
- utworzy środowisko conda `car-buying-assistant`,
- zainstaluje zależności z `requirements.txt`,
- skopiuje `env.example` do `car_buying_assistant/.env` (jeśli plik nie istnieje),
- uruchomi migracje bazy danych.

Następnie uzupełnij `car_buying_assistant/.env` o właściwy klucz `OPENAI_API_KEY`.

## Ręczna konfiguracja krok po kroku

1. **Utwórz środowisko conda**:

```bash
conda create -y -n car-buying-assistant python=3.11
```

2. **Aktywuj środowisko**:

```bash
conda activate car-buying-assistant
```

3. **Zainstaluj zależności**:

```bash
pip install -r requirements.txt
```

4. **Przygotuj plik `.env`**:

```bash
cp env.example car_buying_assistant/.env
```

Edytuj `car_buying_assistant/.env` i ustaw zmienną:

```
OPENAI_API_KEY=twoj_klucz_api
```

5. **Migracje bazy danych**:

```bash
cd car_buying_assistant
python manage.py migrate
```

6. **Uruchom aplikację**:

```bash
python manage.py runserver 0.0.0.0:8000
```

Aplikacja będzie dostępna pod adresem: `http://localhost:8000`.

## Eksport PDF

Aby generować raporty PDF, zainstaluj `wkhtmltopdf` i upewnij się, że binarka jest dostępna w `PATH`. Jeśli nie, ustaw zmienną środowiskową `WKHTMLTOPDF_CMD` na pełną ścieżkę do binarki.

## Utrzymanie środowiska

- Aktualizacja zależności:

```bash
pip install -r requirements.txt --upgrade
```

- Dezaktywacja środowiska:

```bash
conda deactivate
```
