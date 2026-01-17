from django.shortcuts import render, redirect
from django.utils.html import escape
from .utils import get_openai_report

from .templates.modules.forms import ChooseCar
from .models import (
    CarMake,
    CarModel,
    CarGeneration,
    CarSerie,
    CarTrim,
    CarEquipment,
)


def home(request):
    context = {}
    form = ChooseCar(request.POST or None)
    if request.method == "POST":
        try:
            if form.is_valid():
                wants_report = "generate_report" in request.POST
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
                    request.session["report_data"] = {
                        "car": car_data,
                        "report": get_openai_report(car_data),
                    }
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
            "form": form,
            "response": context.get("response")
        },
    )


def report(request):
    report_data = request.session.get("report_data")
    if report_data:
        car = report_data.get("car", {})
        report = report_data.get("report", {})

        def _list_html(items):
            if not items:
                return '<p class="text-sm text-slate-500">Brak danych.</p>'
            lis = "".join(f"<li>{escape(item)}</li>" for item in items)
            return (
                '<ul class="list-disc space-y-1 pl-5 text-sm leading-6 text-slate-600">'
                f"{lis}</ul>"
            )

        fit = report.get("fit", {})
        pros_cons = report.get("pros_cons", {})
        risks = report.get("risks", {})
        costs = report.get("costs", {})
        audience = report.get("audience", {})

        sections = [
            {
                "id": "fit",
                "title": "Ocena dopasowania do preferencji",
                "icon": "star",
                "lead": (
                    f"<p class=\"text-sm text-slate-600\"><strong>Ocena:</strong> "
                    f"{escape(fit.get('score', 'brak'))}</p>"
                ),
                "body": (
                    f"<p class=\"mt-2 text-sm text-slate-600\">"
                    f"{escape(fit.get('summary', ''))}</p>"
                    f"{_list_html(fit.get('bullets', []))}"
                ),
            },
            {
                "id": "pros",
                "title": "Plusy",
                "icon": "plus",
                "lead": "",
                "body": _list_html(pros_cons.get("pros", [])),
            },
            {
                "id": "cons",
                "title": "Minusy",
                "icon": "minus",
                "lead": "",
                "body": _list_html(pros_cons.get("cons", [])),
            },
            {
                "id": "risks",
                "title": "Ryzyka / na co zwrocic uwage przy zakupie",
                "icon": "alert",
                "lead": "",
                "body": _list_html(risks.get("bullets", [])),
            },
            {
                "id": "audience",
                "title": "Dla kogo to auto / kiedy nie bedzie dobrym wyborem",
                "icon": "users",
                "lead": "",
                "body": (
                    "<p class=\"text-sm text-slate-700\"><strong>Dla kogo:</strong></p>"
                    f"{_list_html(audience.get('for_whom', []))}"
                    "<p class=\"mt-3 text-sm text-slate-700\"><strong>Nie dla:</strong></p>"
                    f"{_list_html(audience.get('not_for', []))}"
                ),
            },
            {
                "id": "summary",
                "title": "Podsumowanie i rekomendacja",
                "icon": "flag",
                "lead": "",
                "body": (
                    f"<p class=\"text-sm text-slate-600\"><strong>Rekomendacja:</strong> "
                    f"{escape(audience.get('recommendation', ''))}</p>"
                ),
            },
        ]

        costs_rows = costs.get("rows", []) or []
        title_bits = [
            car.get("brand", ""),
            car.get("model", ""),
            car.get("generation", ""),
            car.get("series", ""),
            car.get("modification", ""),
        ]
        title = " ".join([bit for bit in title_bits if bit and bit != "brak"]).strip()
        if not title:
            title = "Wybrane auto"
        subtitle_parts = [
            f"Wyposazenie: {car.get('equipment', 'brak')}",
            f"Preferencje: {car.get('preferences', 'brak')}",
        ]
        subtitle = " | ".join(subtitle_parts)
        return render(
            request,
            "report.html",
            {
                "response": None,
                "sections": sections,
                "costs_rows": costs_rows,
                "report_title": title,
                "report_subtitle": subtitle,
            },
        )

    response = request.session.get("report_response")
    sections = []
    if response:
        for block in response.split("\n\n"):
            part = block.strip()
            if not part:
                continue
            lines = part.splitlines()
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()
            sections.append(
                {
                    "title": title,
                    "body": body,
                }
            )
    return render(
        request,
        "report.html",
        {
            "response": response,
            "sections": sections,
            "costs_rows": [],
            "report_title": "",
            "report_subtitle": "",
        },
    )
