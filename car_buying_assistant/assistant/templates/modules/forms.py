from django import forms

from assistant.models import (
    CarEquipment,
    CarGeneration,
    CarMake,
    CarModel,
    CarSerie,
    CarTrim,
)


class ChooseCar(forms.Form):
    brand = forms.ChoiceField(label="Marka", choices=[])
    model = forms.ChoiceField(label="Model", choices=[], required=False)
    generation = forms.ChoiceField(
        label="Generacja",
        choices=[("", "Wybierz generację")],
        required=False,
    )
    series = forms.ChoiceField(
        label="Seria",
        choices=[("", "Wybierz serię")],
        required=False,
    )
    modification = forms.ChoiceField(
        label="Modyfikacja",
        choices=[("", "Wybierz modyfikację")],
        required=False,
    )
    equipment = forms.ChoiceField(
        label="Wyposażenie",
        choices=[("", "Wybierz wyposażenie")],
        required=False,
    )

    advanced = forms.BooleanField(label="Zaawansowane opcje", required=False)
    pref_economy = forms.ChoiceField(
        label="1. Ekonomia i koszty",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )
    pref_family = forms.ChoiceField(
        label="2. Rodzina i praktyczność",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )
    pref_reliability = forms.ChoiceField(
        label="3. Niezawodność i bezpieczeństwo",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )
    pref_performance = forms.ChoiceField(
        label="4. Osiągi i prowadzenie",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )
    pref_usage = forms.ChoiceField(
        label="5. Styl użytkowania",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )
    pref_comfort = forms.ChoiceField(
        label="6. Komfort i wrażenia",
        choices=[],
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].choices = self._brand_choices()
        self.fields["model"].choices = self._model_choices()
        self.fields["generation"].choices = self._generation_choices()
        self.fields["series"].choices = self._series_choices()
        self.fields["modification"].choices = self._modification_choices()
        self.fields["equipment"].choices = self._equipment_choices()
        self.fields["pref_economy"].choices = self._pref_economy_choices()
        self.fields["pref_family"].choices = self._pref_family_choices()
        self.fields["pref_reliability"].choices = self._pref_reliability_choices()
        self.fields["pref_performance"].choices = self._pref_performance_choices()
        self.fields["pref_usage"].choices = self._pref_usage_choices()
        self.fields["pref_comfort"].choices = self._pref_comfort_choices()
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {"class": "form-control form-control-lg"}
            )

    

    def _selected_brand(self):
        return self.data.get("brand") or self.initial.get("brand")

    def _selected_model(self):
        return self.data.get("model") or self.initial.get("model")

    def _selected_generation(self):
        return self.data.get("generation") or self.initial.get("generation")

    def _selected_series(self):
        return self.data.get("series") or self.initial.get("series")

    def _brand_choices(self):
        brands = CarMake.objects.using("car2db").all()
        return [("", "Wybierz markę")] + [
            (brand.id_car_make, brand.name) for brand in brands
        ]

    def _model_choices(self):
        selected_brand = self._selected_brand()
        if not selected_brand:
            return [("", "Wybierz model")]
        models = CarModel.objects.using("car2db").filter(id_car_make=selected_brand)
        return [("", "Wybierz model")] + [
            (model.id_car_model, model.name) for model in models
        ]

    def _generation_choices(self):
        selected_model = self._selected_model()
        if not selected_model:
            return [("", "Wybierz generację")]
        generations = CarGeneration.objects.using("car2db").filter(
            id_car_model=selected_model
        )
        return [("", "Wybierz generację")] + [
            (generation.id_car_generation, generation.name)
            for generation in generations
        ]

    def _series_choices(self):
        selected_model = self._selected_model()
        selected_generation = self._selected_generation()
        if not selected_model:
            return [("", "Wybierz serię")]
        series = CarSerie.objects.using("car2db").filter(id_car_model=selected_model)
        if selected_generation:
            series = series.filter(id_car_generation=selected_generation)
        return [("", "Wybierz serię")] + [
            (serie.id_car_serie, serie.name) for serie in series
        ]

    def _modification_choices(self):
        selected_model = self._selected_model()
        selected_series = self._selected_series()
        if not selected_model:
            return [("", "Wybierz modyfikację")]
        trims = CarTrim.objects.using("car2db").filter(id_car_model=selected_model)
        if selected_series:
            trims = trims.filter(id_car_serie=selected_series)
        return [("", "Wybierz modyfikację")] + [
            (trim.id_car_trim, trim.name) for trim in trims
        ]

    def _equipment_choices(self):
        selected_trim = self.data.get("modification") or self.initial.get(
            "modification"
        )
        if not selected_trim:
            return [("", "Wybierz wyposażenie")]
        equipment = CarEquipment.objects.using("car2db").filter(
            id_car_trim=selected_trim
        )
        return [("", "Wybierz wyposażenie")] + [
            (item.id_car_equipment, item.name) for item in equipment
        ]

    def _preference_choices(self):
        return [
            (
                "Ekonomia i koszty",
                [
                    ("low_fuel", "Niskie zużycie paliwa"),
                    ("low_running_costs", "Niskie koszty eksploatacji"),
                    ("cheap_parts", "Tanie i łatwo dostępne części"),
                    ("low_depreciation", "Niska utrata wartości (dobra odsprzedaż)"),
                ],
            ),
            (
                "Rodzina i praktyczność",
                [
                    ("family_car", "Samochód rodzinny"),
                    ("big_boot", "Duży i praktyczny bagażnik"),
                    ("easy_entry", "Łatwe wsiadanie / dobra widoczność"),
                    ("comfortable_rear", "Wygodne tylne siedzenia"),
                ],
            ),
            (
                "Niezawodność i bezpieczeństwo",
                [
                    ("reliability", "Wysoka bezawaryjność"),
                    ("safety_systems", "Dobre systemy bezpieczeństwa"),
                    ("proven_design", "Sprawdzona konstrukcja (bez eksperymentalnych rozwiązań)"),
                ],
            ),
            (
                "Osiągi i prowadzenie",
                [
                    ("performance", "Dobre osiągi"),
                    ("driving_pleasure", "Przyjemność z jazdy / dobre prowadzenie"),
                    ("high_speed_stability", "Stabilność przy wyższych prędkościach"),
                ],
            ),
            (
                "Styl użytkowania",
                [
                    ("urban", "Głównie jazda miejska"),
                    ("long_distance", "Trasy / autostrady"),
                    ("mixed", "Różne warunki (miasto + trasy)"),
                ],
            ),
            (
                "Komfort i wrażenia",
                [
                    ("ride_comfort", "Wysoki komfort jazdy"),
                    ("noise_isolation", "Dobra izolacja akustyczna"),
                    ("modern_interior", "Nowoczesne wnętrze i technologie"),
                    ("design", "Wygląd / design ma znaczenie"),
                ],
            ),
        ]

    def _pref_economy_choices(self):
        return [
            ("", "Brak wyboru"),
            ("low_fuel", "1.1 Niskie zużycie paliwa"),
            ("low_running_costs", "1.2 Niskie koszty eksploatacji"),
            ("cheap_parts", "1.3 Tanie i łatwo dostępne części"),
            ("low_depreciation", "1.4 Niska utrata wartości (dobra odsprzedaż)"),
        ]

    def _pref_family_choices(self):
        return [
            ("", "Brak wyboru"),
            ("family_car", "2.1 Samochód rodzinny"),
            ("big_boot", "2.2 Duży i praktyczny bagażnik"),
            ("easy_entry", "2.3 Łatwe wsiadanie i dobra widoczność"),
            ("comfortable_rear", "2.4 Wygodne tylne siedzenia"),
        ]

    def _pref_reliability_choices(self):
        return [
            ("", "Brak wyboru"),
            ("reliability", "3.1 Wysoka bezawaryjność"),
            ("safety_systems", "3.2 Dobre systemy bezpieczeństwa"),
            ("proven_design", "3.3 Sprawdzona konstrukcja (bez eksperymentalnych rozwiązań)"),
        ]

    def _pref_performance_choices(self):
        return [
            ("", "Brak wyboru"),
            ("performance", "4.1 Dobre osiągi"),
            ("driving_pleasure", "4.2 Przyjemność z jazdy i dobre prowadzenie"),
            ("high_speed_stability", "4.3 Stabilność przy wyższych prędkościach"),
        ]

    def _pref_usage_choices(self):
        return [
            ("", "Brak wyboru"),
            ("urban", "5.1 Głównie jazda miejska"),
            ("long_distance", "5.2 Trasy i autostrady"),
            ("mixed", "5.3 Różne warunki (miasto i trasy)"),
        ]

    def _pref_comfort_choices(self):
        return [
            ("", "Brak wyboru"),
            ("ride_comfort", "6.1 Wysoki komfort jazdy"),
            ("noise_isolation", "6.2 Dobra izolacja akustyczna"),
            ("modern_interior", "6.3 Nowoczesne wnętrze i technologie"),
            ("design", "6.4 Wygląd i design mają znaczenie"),
        ]
