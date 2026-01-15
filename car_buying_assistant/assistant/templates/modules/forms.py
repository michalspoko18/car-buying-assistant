from django import forms

from assistant.models import CarMake, CarModel, CarSpecification


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
    specification = forms.ModelChoiceField(
        label="Wyposażenie",
        queryset=CarSpecification.objects.using("car2db").all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].choices = self._brand_choices()
        self.fields["model"].choices = self._model_choices()
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {"class": "form-control form-control-lg"}
            )

    @staticmethod
    def _brand_choices():
        brands = CarMake.objects.using("car2db").all()
        return [("", "Wybierz markę")] + [
            (brand.id_car_make, brand.name) for brand in brands
        ]

    def _model_choices(self):
        selected_brand = self.data.get("brand") or self.initial.get("brand")
        if not selected_brand:
            return [("", "Wybierz model")]
        models = CarModel.objects.using("car2db").filter(id_car_make=selected_brand)
        return [("", "Wybierz model")] + [
            (model.id_car_model, model.name) for model in models
        ]
