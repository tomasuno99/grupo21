from django.shortcuts import render
from django.http import HttpResponse
from .models import Residencia
from .forms import ResidenciaForm
# Create your views here.

def product_detail(request,id):
    residencia=Residencia.objects.get(auto_id=id)
    context={'nombre': residencia.nombre
    , 'capacidad': residencia.capacidad}
    return render(request,'product-detail.html',context)

def prueba(request, id):
    return HttpResponse(id)

def agregar_residencia(request):
   form = ResidenciaForm()
   return render(request, 'agregar_residencia.html', {'form': form})

def listado_residencias(request):
    residencia=Residencia.objects.get(auto_id=1)
    context={'id': residencia.auto_id}
    return render(request,'product.html',context)
