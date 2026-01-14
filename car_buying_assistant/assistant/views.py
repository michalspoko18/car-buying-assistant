from django.shortcuts import render
from .utils import get_openai_client

from .templates.modules.forms import ChooseCar


def home(request):
    context = {}
    form = ChooseCar(request.POST or None)
    if request.method == "POST":
        try:
            if form.is_valid():
                brand = form.cleaned_data["brand"]
                model = form.cleaned_data["model"]
                specification = form.cleaned_data["specification"]
                context["response"] = (
                    f"Received brand: {brand}, model: {model}, "
                    f"specification: {specification}"
                )
        except Exception as exc:
            context["response"] = f"Error calling OpenAI: {exc}"

    return render(
        request,
        "home.html",
        {
            "form": form,
            "response": context
        },
    )
