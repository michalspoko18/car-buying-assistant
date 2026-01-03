from django.shortcuts import render
from .utils import get_openai_client

from .templates.modules.forms import ChooseCar

from .models import CarMake


def home(request):
    makes = CarMake.objects.using("car2db").all()
    context = {}
    if request.method == "POST":
        try:
            form = ChooseCar(request.POST)
            if form.is_valid():
                print(makes)
                brand = form.cleaned_data["brand"]
                model = form.cleaned_data["model"]
                print(f"Brand: {brand}, Model: {model}")
                # context["response"] = get_openai_client(brand=brand, model=model)
                context["response"] = f"Received brand: {brand}, model: {model}"
        except Exception as exc:
            context["response"] = f"Error calling OpenAI: {exc}"

    return render(
        request,
        "home.html",
        {
            "makes": makes,
            "response": context
        },
    )
