import os
import shutil

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.text import slugify
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
                        obj = (
                            model.objects.using("car2db")
                            .filter(**{pk_field: value})
                            .first()
                        )
                        return obj.name if obj is not None else value
                    except Exception:
                        return value

                brand_label = _label_for(CarMake, "id_car_make", brand)
                model_label = _label_for(CarModel, "id_car_model", model)
                generation_label = _label_for(
                    CarGeneration, "id_car_generation", generation
                )
                series_label = _label_for(CarSerie, "id_car_serie", series)
                modification_label = _label_for(
                    CarTrim, "id_car_trim", modification
                )
                equipment_label = _label_for(
                    CarEquipment, "id_car_equipment", equipment
                )

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
                request.session["report_response"] = (
                    f"Error calling OpenAI: {exc}"
                )
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
    return render(
        request,
        "report.html",
        _build_report_context(request, for_pdf=False),
    )


def report_pdf(request):
    try:
        import pdfkit
    except Exception as exc:
        return HttpResponse(
            "Brak zaleznosci do generowania PDF.\n"
            "Zainstaluj: pip install -r requirements.txt\n\n"
            f"Szczegoly: {exc}\n",
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    context = _build_report_context(request, for_pdf=True)
    html = render_to_string(
        "report_pdf.html",
        context=context,
        request=request,
    )

    wkhtmltopdf_cmd = (
        os.environ.get("WKHTMLTOPDF_CMD")
        or shutil.which("wkhtmltopdf")
    )
    if not wkhtmltopdf_cmd:
        return HttpResponse(
            "wkhtmltopdf nie jest zainstalowany lub nie jest w PATH.\n"
            "Zainstaluj go i sproboj ponownie.\n\n"
            "macOS (Homebrew): brew install wkhtmltopdf\n"
            "Albo ustaw zmienna srodowiskowa WKHTMLTOPDF_CMD "
            "na pelna sciezke do binarki.\n",
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_cmd)
    options = {
        "encoding": "UTF-8",
        "print-media-type": "",
        "margin-top": "12mm",
        "margin-right": "12mm",
        "margin-bottom": "14mm",
        "margin-left": "12mm",
        "disable-smart-shrinking": "",
        "quiet": "",
    }

    pdf_bytes = pdfkit.from_string(
        html,
        False,
        options=options,
        configuration=config,
    )

    title = context.get("report_title") or "raport"
    filename = f"{slugify(title) or 'raport'}.pdf"
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _build_report_context(request, for_pdf: bool):
    report_data = request.session.get("report_data")
    if report_data:
        car = report_data.get("car", {})
        report_obj = report_data.get("report", {})

        def _strip_risk_prefix(text):
            trimmed = text.lstrip()
            lowered = trimmed.lower()
            if lowered.startswith("ryzyko:"):
                return trimmed[7:].lstrip()
            if lowered.startswith("ryzyko "):
                return trimmed[6:].lstrip()
            if lowered == "ryzyko":
                return ""
            return text

        def _strip_leading_dash(text):
            trimmed = text.lstrip()
            if trimmed.startswith("-"):
                return trimmed[1:].lstrip()
            return text

        def _list_html(items, strip_risk=False, strip_dash=True):
            if not items:
                if for_pdf:
                    return '<p class="muted small">Brak danych.</p>'
                return '<p class="text-sm text-slate-500">Brak danych.</p>'
            safe_items = []
            for item in items:
                text = item or ""
                if strip_risk:
                    text = _strip_risk_prefix(text)
                if strip_dash:
                    text = _strip_leading_dash(text)
                safe_items.append(f"<li>{escape(text)}</li>")
            lis = "".join(safe_items)
            if for_pdf:
                return f"<ul class=\"list\">{lis}</ul>"
            return (
                '<ul class="list-disc space-y-1 pl-5 text-sm leading-6 '
                'text-slate-600">'
                f"{lis}</ul>"
            )

        fit = report_obj.get("fit", {})
        pros_cons = report_obj.get("pros_cons", {})
        risks = report_obj.get("risks", {})
        costs = report_obj.get("costs", {})
        audience = report_obj.get("audience", {})

        if for_pdf:
            fit_score = escape(fit.get("score", "brak"))
            fit_lead = (
                "<p class=\"small\"><strong>Dopasowanie:</strong> "
                f"{fit_score}</p>"
            )
            fit_body = (
                f"<p class=\"muted small\">"
                f"{escape(fit.get('summary', ''))}</p>"
                f"{_list_html(fit.get('bullets', []))}"
            )
            audience_body = (
                "<p class=\"small\"><strong>Dla kogo:</strong></p>"
                f"{_list_html(audience.get('for_whom', []))}"
                "<p class=\"small spacer\"><strong>Nie dla:</strong></p>"
                f"{_list_html(audience.get('not_for', []))}"
            )
            recommendation = escape(audience.get("recommendation", ""))
            summary_body = (
                "<p class=\"small\"><strong>Rekomendacja:</strong> "
                f"{recommendation}</p>"
            )
        else:
            fit_lead = (
                "<p class=\"text-sm text-slate-600\">"
                "<strong>Dopasowanie:</strong> "
                f"{escape(fit.get('score', 'brak'))}</p>"
            )
            fit_body = (
                "<p class=\"mt-2 text-sm text-slate-600\">"
                f"{escape(fit.get('summary', ''))}</p>"
                f"{_list_html(fit.get('bullets', []))}"
            )
            audience_body = (
                "<p class=\"text-sm text-slate-700\">"
                "<strong>Dla kogo:</strong></p>"
                f"{_list_html(audience.get('for_whom', []))}"
                "<p class=\"mt-3 text-sm text-slate-700\">"
                "<strong>Nie dla:</strong></p>"
                f"{_list_html(audience.get('not_for', []))}"
            )
            summary_body = (
                "<p class=\"text-sm text-slate-600\">"
                "<strong>Rekomendacja:</strong> "
                f"{escape(audience.get('recommendation', ''))}</p>"
            )

        sections = [
            {
                "id": "fit",
                "title": "Ocena dopasowania do preferencji",
                "icon": "star",
                "lead": fit_lead,
                "body": fit_body,
            },
            {
                "id": "pros",
                "title": "Plusy",
                "icon": "plus",
                "lead": "",
                "body": _list_html(pros_cons.get("pros", []), strip_dash=True),
            },
            {
                "id": "cons",
                "title": "Minusy",
                "icon": "minus",
                "lead": "",
                "body": _list_html(pros_cons.get("cons", []), strip_dash=True),
            },
            {
                "id": "risks",
                "title": "Ryzyka / na co zwrocic uwage przy zakupie",
                "icon": "alert",
                "lead": "",
                "body": _list_html(risks.get("bullets", []), strip_risk=True),
            },
            {
                "id": "audience",
                "title": "Dla kogo to auto / kiedy nie bedzie dobrym wyborem",
                "icon": "users",
                "lead": "",
                "body": audience_body,
            },
            {
                "id": "summary",
                "title": "Podsumowanie i rekomendacja",
                "icon": "flag",
                "lead": "",
                "body": summary_body,
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
        title = " ".join(
            [bit for bit in title_bits if bit and bit != "brak"]
        ).strip()
        if not title:
            title = "Wybrane auto"
        subtitle_parts = [
            f"Wyposazenie: {car.get('equipment', 'brak')}",
            f"Preferencje: {car.get('preferences', 'brak')}",
        ]
        subtitle = " | ".join(subtitle_parts)
        return {
            "response": None,
            "sections": sections,
            "costs_rows": costs_rows,
            "report_title": title,
            "report_subtitle": subtitle,
        }

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
            if for_pdf:
                body = escape(body).replace("\n", "<br>")
                sections.append(
                    {
                        "title": title,
                        "body": f"<p class=\"small muted\">{body}</p>",
                        "icon": "",
                    }
                )
            else:
                sections.append({"title": title, "body": body})

    return {
        "response": response,
        "sections": sections,
        "costs_rows": [],
        "report_title": "",
        "report_subtitle": "",
    }
