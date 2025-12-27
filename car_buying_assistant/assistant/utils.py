from django.conf import settings
from openai import OpenAI


def get_openai_api_key():
    return settings.OPENAI_API_KEY


def get_openai_client(marka="Toyota", model="Corolla"):
    client = OpenAI()

    input_text = f"""Opisz krótko samochód {marka} {model}. \n
    Wypisz plusy, minusy i dla kogo to auto jest dobrym wyborem. \n
    Odpowiedź w języku polskim, maksymalnie 200–300 słów.
    """

    response = client.responses.create(
        model="gpt-5-nano",
        input=input_text
    )

    print(response.output_text)
