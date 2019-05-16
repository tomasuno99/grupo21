from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Residencia
from .forms import *
from django.views.generic import TemplateView, ListView
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def product_detail(request,id):
   residencia=Residencia.objects.get(auto_id=id)
   related_products= Residencia.objects.filter(capacidad=residencia.capacidad).exclude(auto_id=id)
   context= {
      "residencia": residencia,
      "related_products": related_products
   }
   return render(request,'product-detail.html', context)

def prueba(request, id):
    return HttpResponse(id)

class Agregar_residencia(TemplateView):
   template_name = 'agregar_residencia.html'
   def get(self, request):
      form = ResidenciaForm()
      return render(request, self.template_name, {'form': form})

   def post(self,request):
      form = ResidenciaForm(request.POST)
      if form.is_valid():
         #form.save()
         nombre = form.cleaned_data['nombre']
         capacidad = form.cleaned_data['capacidad']
         r = Residencia()
         r.nombre = nombre
         r.capacidad = capacidad
         r.save()
         form = ResidenciaForm()
         return HttpResponseRedirect('/listado_residencias')

def listado_residencias(request):
    residencias=Residencia.objects.all()
    print(residencias)
    context={'residencias': residencias}
    return render(request,'product.html',context)

def modificar_residencia(request, id):
   if request.method == "POST":
      form = ModResidenciaForm(request.POST)
      if form.is_valid():
         nombre = form.cleaned_data['nombre']
         capacidad = form.cleaned_data['capacidad']
         residencia = Residencia.objects.get(auto_id=id)
         residencia.nombre = nombre
         residencia.capacidad = capacidad
         residencia.save()
         form = ModResidenciaForm()
         return redirect('/listado_residencias')
   else:
      form = ModResidenciaForm()
      return render(request,'modificar_residencia.html', {'id': id, 'form': form})

def eliminar_residencia(request, id):
   if request.method == "GET":
      residencia = Residencia.objects.get (auto_id=id)
      residencia.delete()
      return redirect('/listado_residencias')

def mostrar_index(request):
   residencias=Residencia.objects.all()
   context = {
      'residencias': residencias
   }
   return render(request, "index.html", context)
      