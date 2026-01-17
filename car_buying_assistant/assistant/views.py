from django.shortcuts import render, redirect
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
                generation = form.cleaned_data["generation"]
                series = form.cleaned_data["series"]
                modification = form.cleaned_data["modification"]
                equipment = form.cleaned_data["equipment"]
                advanced = form.cleaned_data["advanced"]
                car_type = "osobowy"

                def _label_for(model, pk_field, value):
                    if not value:
                        return ""
                    try:
                        obj = model.objects.using("car2db").filter(**{pk_field: value}).first()
                        return obj.name if obj is not None else value
                    except Exception:
                        return value

                brand_label = _label_for(CarMake, "id_car_make", brand)
                model_label = _label_for(CarModel, "id_car_model", model)
                generation_label = _label_for(CarGeneration, "id_car_generation", generation)
                series_label = _label_for(CarSerie, "id_car_serie", series)
                modification_label = _label_for(CarTrim, "id_car_trim", modification)
                equipment_label = _label_for(CarEquipment, "id_car_equipment", equipment)

                # collect grouped preference selections (radio fields)
                pref_fields = [
                    "pref_economy",
                    "pref_family",
                    "pref_reliability",
                    "pref_performance",
                    "pref_usage",
                    "pref_comfort",
                ]
                pref_labels = []
                if advanced:
                    for pf in pref_fields:
                        val = form.cleaned_data.get(pf)
                        # build mapping from that field's choices
                        try:
                            field_choices = form.fields[pf].choices
                            # field_choices is list of (value,label)
                            label_map = {k: v for k, v in field_choices}
                            if val:
                                pref_labels.append(label_map.get(val, val))
                        except Exception:
                            continue

                if wants_report:
                    car_data = {
                        "car_type": car_type,
                        "brand": brand_label or "brak",
                        "model": model_label or "brak",
                        "generation": generation_label or "brak",
                        "series": series_label or "brak",
                        "modification": modification_label or "brak",
                        "equipment": equipment_label or "brak",
                        "preferences": ", ".join(pref_labels) or "brak",
                    }
                    request.session["report_response"] = get_openai_client(car_data)
                    return redirect("report")
        except Exception as exc:
            if "generate_report" in request.POST:
                request.session["report_response"] = f"Error calling OpenAI: {exc}"
                return redirect("report")
            context["response"] = f"Error calling OpenAI: {exc}"

    return render(
        request,
        "home.html",
        {
            "makes": makes,
            "response": context
        },
    )


def report(request):
    response = request.session.get("report_response")
    return render(
        request,
        "report.html",
        {
            "response": response,
        },
    )
