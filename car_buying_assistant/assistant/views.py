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
                generation = form.cleaned_data["generation"]
                series = form.cleaned_data["series"]
                modification = form.cleaned_data["modification"]
                equipment = form.cleaned_data["equipment"]
                car_type = "osobowy"
                context["response"] = (
                    "Received type: "
                    f"{car_type}, brand: {brand}, model: {model}, "
                    f"generation: {generation}, series: {series}, "
                    f"modification: {modification}, equipment: {equipment}"
                )
        except Exception as exc:
            context["response"] = f"Error calling OpenAI: {exc}"

    return render(
        request,
        "home.html",
        {
            "form": form,
            "response": context.get("response")
        },
    )
