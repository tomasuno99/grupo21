from django import forms
from .models import Residencia

class ModResidenciaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa nombre de la residencia'
        }
    ))
    capacidad = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa capacidad de personas de la residencia'
        }
    ))
    direccion = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa direccion de la residencia'
        }
    ))
    imagen = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa link de la imagen'
        }
    ))


    class Meta:
        model = Residencia
        fields = ('nombre','capacidad','direccion','imagen')
        # widgets = {
        #     'nombre': forms.TextInput(attrs={}),
        #     'capacidad': forms.TextInput(attrs={'style': 'border-color:darkgoldenrod; border-radius: 10px;'})
        # }

class ResidenciaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa nombre de la residencia'
        }
    ))
    capacidad = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa capacidad de personas de la residencia'
        }
    ))
    direccion = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa direccion de la residencia'
        }
    ))
    imagen = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
            'style': 'box-shadow: inset 0 2px 2px rgba(0,0,0,.075); border: 1px solid red',
            'placeholder': 'ingresa link de la imagen'
        }
    ))
    class Meta:
        model = Residencia
        fields = ('nombre','capacidad','direccion','imagen')
        # widgets = {
        #     'nombre': forms.TextInput(attrs={}),
        #     'capacidad': forms.TextInput(attrs={'style': 'border-color:darkgoldenrod; border-radius: 10px;'})
        # }