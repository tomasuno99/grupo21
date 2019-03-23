from django import forms
from .models import Registrado



class ContactForm(forms.Form):
    nombre= forms.CharField(max_length=50)
    email= forms.EmailField()
    texto= forms.CharField(widget=forms.Textarea)

class RegModelForm(forms.ModelForm):
    class Meta:
            model= Registrado
            fields= ["nombre", "email"]
