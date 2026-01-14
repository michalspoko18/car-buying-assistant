from django import forms


class ChooseCar(forms.Form):
    brand = forms.CharField(label="Brand", max_length=100)
    model = forms.CharField(label="Model", max_length=100)