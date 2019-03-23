from django.shortcuts import render
from .forms import RegModelForm,ContactForm
from .models import Registrado
# Create your views here.

def inicio(request):
    titulo= "HOLA"
    form= RegModelForm(request.POST) # or None
    context= {
        "form": form,
        "titulo": titulo,
    }
    if form.is_valid():
        instance= form.save()
        context= {
        "titulo": "Gracias %s!" %instance.nombre
        }
        print (instance)
        print (instance.timestamp)
        #form_data= form.cleaned_data
        #el_email= form_data.get("email")
        #el_nombre=form_data.get("nombre")
        #obj= Registrado.objects.create(email=el_email, nombre=el_nombre)

    return render(request, "inicio.html", context)


def contacto(request):
    form= ContactForm(request.POST or None)
    context= {
        "form": form,
    }
    return render(request, "contacto.html", context)
