from django.test import TestCase
from assistant.utils import get_openai_client


class OpenAIClientTestCase(TestCase):
    def test_get_openai_client(self):
        get_openai_client(marka="Honda", model="Civic")
