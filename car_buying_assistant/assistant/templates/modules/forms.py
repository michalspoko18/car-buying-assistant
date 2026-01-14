from django import forms

from assistant.models import CarMake, CarModel, CarSpecification


class ChooseCar(forms.Form):
    brand = forms.ChoiceField(label="Brand", choices=[])
    model = forms.ChoiceField(label="Model", choices=[], required=False)
    specification = forms.ModelChoiceField(
        label="Specification",
        queryset=CarSpecification.objects.using("car2db").all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].choices = self._brand_choices()
        self.fields["model"].choices = self._model_choices()

    @staticmethod
    def _brand_choices():
        brands = CarMake.objects.using("car2db").all()
        return [("", "Select brand")] + [
            (brand.id_car_make, brand.name) for brand in brands
        ]

    def _model_choices(self):
        selected_brand = self.data.get("brand") or self.initial.get("brand")
        if not selected_brand:
            return [("", "Select model")]
        models = CarModel.objects.using("car2db").filter(id_car_make=selected_brand)
        return [("", "Select model")] + [
            (model.id_car_model, model.name) for model in models
        ]
