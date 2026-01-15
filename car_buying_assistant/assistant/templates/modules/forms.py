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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].choices = self._brand_choices()
        self.fields["model"].choices = self._model_choices()
        self.fields["generation"].choices = self._generation_choices()
        self.fields["series"].choices = self._series_choices()
        self.fields["modification"].choices = self._modification_choices()
        self.fields["equipment"].choices = self._equipment_choices()
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
