from django.conf import settings
from openai import OpenAI


def get_openai_api_key():
    return settings.OPENAI_API_KEY


def get_openai_client(marka: str, model: str) -> str:
    client = OpenAI()

    input_text = (
        f"Opisz krótko samochód {marka} {model}.\n"
        "Wypisz plusy, minusy i dla kogo to auto jest dobrym wyborem.\n"
        "Odpowiedź w języku polskim, maksymalnie 200–300 słów."
    )

    response = client.responses.create(model="gpt-5-nano", input=input_text)

    output_text = getattr(response, "output_text", None)
    if output_text is None:
        try:
            output_text = str(response)
        except Exception:
            output_text = "No output_text available from the OpenAI response."

    return output_text
