from django.shortcuts import render
from django.http import HttpResponse
from .models import Residencia
# Create your views here.

def index(request):
    residencia=Residencia.objects.get(auto_id=1)
    context={'nombre': residencia.nombre
            , 'capacidad': residencia.capacidad}
    return render(request,'product-detail.html',context)

def prueba(request, id):
    return HttpResponse(id)