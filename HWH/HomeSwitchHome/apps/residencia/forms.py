from django import forms

class ResidenciaForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    capacidad = forms.IntegerField(null=True, blank=True)