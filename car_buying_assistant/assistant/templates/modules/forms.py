from django import forms

from assistant.models import (
    CarEquipment,
    CarGeneration,
    CarMake,
    CarModel,
    CarSerie,
    CarTrim,
    CarType,
)


class ChooseCar(forms.Form):
    car_type = forms.ChoiceField(label="Typ pojazdu", choices=[])
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
        self.fields["car_type"].choices = self._type_choices()
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

    @staticmethod
    def _type_choices():
        types = CarType.objects.using("car2db").all()
        return [("", "Wybierz typ")] + [
            (car_type.id_car_type, car_type.name) for car_type in types
        ]

    def _selected_type(self):
        return self.data.get("car_type") or self.initial.get("car_type")

    def _selected_brand(self):
        return self.data.get("brand") or self.initial.get("brand")

    def _selected_model(self):
        return self.data.get("model") or self.initial.get("model")

    def _selected_generation(self):
        return self.data.get("generation") or self.initial.get("generation")

    def _selected_series(self):
        return self.data.get("series") or self.initial.get("series")

    def _brand_choices(self):
        selected_type = self._selected_type()
        brands = CarMake.objects.using("car2db").all()
        if selected_type:
            brands = brands.filter(id_car_type=selected_type)
        return [("", "Wybierz markę")] + [
            (brand.id_car_make, brand.name) for brand in brands
        ]

    def _model_choices(self):
        selected_brand = self._selected_brand()
        selected_type = self._selected_type()
        if not selected_brand:
            return [("", "Wybierz model")]
        models = CarModel.objects.using("car2db").filter(id_car_make=selected_brand)
        if selected_type:
            models = models.filter(id_car_type=selected_type)
        return [("", "Wybierz model")] + [
            (model.id_car_model, model.name) for model in models
        ]

    def _generation_choices(self):
        selected_model = self._selected_model()
        selected_type = self._selected_type()
        if not selected_model:
            return [("", "Wybierz generację")]
        generations = CarGeneration.objects.using("car2db").filter(
            id_car_model=selected_model
        )
        if selected_type:
            generations = generations.filter(id_car_type=selected_type)
        return [("", "Wybierz generację")] + [
            (generation.id_car_generation, generation.name)
            for generation in generations
        ]

    def _series_choices(self):
        selected_model = self._selected_model()
        selected_generation = self._selected_generation()
        selected_type = self._selected_type()
        if not selected_model:
            return [("", "Wybierz serię")]
        series = CarSerie.objects.using("car2db").filter(id_car_model=selected_model)
        if selected_generation:
            series = series.filter(id_car_generation=selected_generation)
        if selected_type:
            series = series.filter(id_car_type=selected_type)
        return [("", "Wybierz serię")] + [
            (serie.id_car_serie, serie.name) for serie in series
        ]

    def _modification_choices(self):
        selected_model = self._selected_model()
        selected_series = self._selected_series()
        selected_type = self._selected_type()
        if not selected_model:
            return [("", "Wybierz modyfikację")]
        trims = CarTrim.objects.using("car2db").filter(id_car_model=selected_model)
        if selected_series:
            trims = trims.filter(id_car_serie=selected_series)
        if selected_type:
            trims = trims.filter(id_car_type=selected_type)
        return [("", "Wybierz modyfikację")] + [
            (trim.id_car_trim, trim.name) for trim in trims
        ]

    def _equipment_choices(self):
        selected_trim = self.data.get("modification") or self.initial.get(
            "modification"
        )
        selected_type = self._selected_type()
        if not selected_trim:
            return [("", "Wybierz wyposażenie")]
        equipment = CarEquipment.objects.using("car2db").filter(
            id_car_trim=selected_trim
        )
        if selected_type:
            equipment = equipment.filter(id_car_type=selected_type)
        return [("", "Wybierz wyposażenie")] + [
            (item.id_car_equipment, item.name) for item in equipment
        ]
