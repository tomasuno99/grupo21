from django import forms
from .models import Residencia

class ResidenciaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50)
    capacidad = forms.IntegerField()

    class Meta:
        model = Residencia
        fields = ('nombre','capacidad',)