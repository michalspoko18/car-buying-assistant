from django.conf import settings
from openai import OpenAI


def get_openai_api_key():
    return settings.OPENAI_API_KEY


REPORT_EXAMPLE = (
    "Ocena dopasowania do preferencji:\n"
    "- 8/10: bardzo dobre dopasowanie do potrzeb rodzinnych i komfortu, słabsza dynamika.\n"
    "- Kluczowe preferencje spełnione: praktyczność, niezawodność, spokojna jazda.\n"
    "\n"
    "Plusy:\n"
    "- przestronne wnętrze i pojemny bagażnik\n"
    "- stabilne zachowanie na trasie i komfort zawieszenia\n"
    "- szeroka dostępność części i serwisów\n"
    "\n"
    "Minusy:\n"
    "- przeciętne osiągi przy pełnym obciążeniu\n"
    "- wyższe spalanie w mieście\n"
    "- przeciętne wyciszenie przy wyższych prędkościach\n"
    "\n"
    "Ryzyka / na co zwrócić uwagę przy zakupie:\n"
    "- historia serwisowa automatu i interwały wymian oleju\n"
    "- wycieki oleju z uszczelniaczy oraz zużycie tulei zawieszenia\n"
    "- ślady korozji na podwoziu w egzemplarzach z importu\n"
    "\n"
    "Szacunkowe koszty eksploatacji i serwisu:\n"
    "| Pozycja | Szacunek | Uwagi |\n"
    "| --- | --- | --- |\n"
    "| Przegląd okresowy | 900–1400 zł | olej + filtry |\n"
    "| Klocki + tarcze (przód) | 700–1200 zł | zależnie od marki części |\n"
    "| Opony (komplet) | 1600–2400 zł | rozmiar 17–18\" |\n"
    "| Ubezpieczenie | 1800–3200 zł/rok | profil kierowcy |\n"
    "\n"
    "Dla kogo to auto / kiedy nie będzie dobrym wyborem:\n"
    "- dla rodzin i osób jeżdżących w trasy oraz z pełnym bagażem\n"
    "- nie dla osób oczekujących sportowych wrażeń lub niskich kosztów paliwa w mieście\n"
    "\n"
    "Podsumowanie i rekomendacja:\n"
    "Rozsądny wybór do codziennej eksploatacji. Szukaj egzemplarzy z pełną "
    "dokumentacją serwisową, najlepiej po weryfikacji stanu zawieszenia i skrzyni."
)


def get_openai_client(car_data: dict) -> str:
    client = OpenAI()

    input_text = (
        "Przygotuj zaawansowany raport dla auta w języku polskim. Użyj dokładnie "
        "poniższych nagłówków i zachowaj czytelny, powtarzalny format:\n"
        "Ocena dopasowania do preferencji\n"
        "Plusy\n"
        "Minusy\n"
        "Ryzyka / na co zwrócić uwagę przy zakupie\n"
        "Szacunkowe koszty eksploatacji i serwisu\n"
        "Dla kogo to auto / kiedy nie będzie dobrym wyborem\n"
        "Podsumowanie i rekomendacja\n"
        "W sekcji kosztów użyj tabeli Markdown z kolumnami: Pozycja | Szacunek | Uwagi.\n"
        "W każdej sekcji używaj krótkich punktów lub krótkich akapitów.\n"
        "Długość: 350–500 słów.\n"
        "\n"
        "Dane wejściowe:\n"
        f"- marka: {car_data.get('brand')}\n"
        f"- model: {car_data.get('model')}\n"
        f"- generacja: {car_data.get('generation')}\n"
        f"- seria: {car_data.get('series')}\n"
        f"- modyfikacja: {car_data.get('modification')}\n"
        f"- wyposażenie: {car_data.get('equipment')}\n"
        f"- preferencje: {car_data.get('preferences')}\n"
        "\n"
        "Przykład formatu:\n"
        f"{REPORT_EXAMPLE}"
    )

    response = client.responses.create(model="gpt-5-nano", input=input_text)

    output_text = getattr(response, "output_text", None)
    if output_text is None:
        try:
            output_text = str(response)
        except Exception:
            output_text = "No output_text available from the OpenAI response."

    return output_text
