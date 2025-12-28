from django.shortcuts import render
from .utils import get_openai_client


def home(request):
    context = {}
    if request.method == "POST":
        try:
            context["response"] = get_openai_client(marka="Honda", model="Civic")
        except Exception as exc:
            context["response"] = f"Error calling OpenAI: {exc}"

    return render(request, "home.html", context)
