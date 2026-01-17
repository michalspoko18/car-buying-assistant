import json

from django.conf import settings
from openai import OpenAI


def get_openai_api_key():
    return settings.OPENAI_API_KEY


def _parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return {}
    return {}


def _call_openai(client: OpenAI, prompt: str) -> dict:
    response = client.responses.create(model="gpt-5-nano", input=prompt)
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        try:
            output_text = str(response)
        except Exception:
            output_text = ""
    return _parse_json(output_text or "")


def get_openai_report(car_data: dict) -> dict:
    client = OpenAI()

    base = (
        "Dane auta:\n"
        f"- marka: {car_data.get('brand')}\n"
        f"- model: {car_data.get('model')}\n"
        f"- generacja: {car_data.get('generation')}\n"
        f"- seria: {car_data.get('series')}\n"
        f"- modyfikacja: {car_data.get('modification')}\n"
        f"- wyposazenie: {car_data.get('equipment')}\n"
        f"- preferencje: {car_data.get('preferences')}\n"
    )

    fit_prompt = (
        "Napisz sekcje oceny dopasowania. Zwroc tylko JSON.\n"
        'Format: {"score":"8/10","summary":"...","bullets":["...","..."]}\n'
        "Badz bardziej krytyczny: srednie wyniki powinny byc czestsze, a wysokie oceny rzadkie.\n"
        "Uzywaj krotkich zdan, bez markdown. Jezyk polski.\n"
        f"{base}"
    )
    pros_cons_prompt = (
        "Wygeneruj plusy i minusy. Zwroc tylko JSON.\n"
        'Format: {"pros":["..."],"cons":["..."]}\n'
        "Uzywaj krotkich punktow. Jezyk polski.\n"
        f"{base}"
    )
    risks_prompt = (
        "Wygeneruj ryzyka i na co zwrocic uwage przy zakupie. Zwroc tylko JSON.\n"
        'Format: {"bullets":["...","..."]}\n'
        "Uzywaj krotkich punktow. Jezyk polski.\n"
        f"{base}"
    )
    costs_prompt = (
        "Wygeneruj szacunkowe koszty eksploatacji i serwisu. Zwroc tylko JSON.\n"
        'Format: {"rows":[{"item":"...","estimate":"...","notes":"..."}]}\n'
        "Wartosci w PLN, krotkie opisy. Jezyk polski.\n"
        f"{base}"
    )
    audience_prompt = (
        "Wygeneruj dla kogo to auto i kiedy nie bedzie dobrym wyborem, oraz rekomendacje. Zwroc tylko JSON.\n"
        'Format: {"for_whom":["..."],"not_for":["..."],"recommendation":"..."}\n'
        "Uzywaj krotkich punktow i 1-2 zdania rekomendacji. Jezyk polski.\n"
        f"{base}"
    )

    fit = _call_openai(client, fit_prompt)
    pros_cons = _call_openai(client, pros_cons_prompt)
    risks = _call_openai(client, risks_prompt)
    costs = _call_openai(client, costs_prompt)
    audience = _call_openai(client, audience_prompt)

    return {
        "fit": fit,
        "pros_cons": pros_cons,
        "risks": risks,
        "costs": costs,
        "audience": audience,
    }
