from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Residencia
from .forms import *
from apps.reserva.models import *
from django.views.generic import TemplateView, ListView
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
# Create your views here.

def product_detail(request,id):
   residencia=Residencia.objects.get(auto_id=id)
   related_products= Residencia.objects.filter(capacidad=residencia.capacidad).exclude(auto_id=id)
   fechas=[]
   for fecha in Reserva.objects.filter(residenciaQuePertence=residencia).values('semana_del_año'):
      fechas.append((fecha['semana_del_año']).strftime('%d/%m/%Y'))
   context= {
      "residencia": residencia,
      "related_products": related_products,
      "fechas": fechas[26:]
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
         nom = form.cleaned_data['nombre']
         capacidad = form.cleaned_data['capacidad']
         r = Residencia.objects.filter(nombre=nom).exists()
         if not r:
            r = Residencia()
            r.nombre = nom
            r.capacidad = capacidad
            r.save()
            r= Residencia.objects.get(auto_id=r.auto_id)
            creacion_aux=lunes(r.creacion)
            for i in range(1,53):
               crearReservas(r,creacion_aux)
               creacion_aux=creacion_aux + timedelta(days=1)
               creacion_aux=lunes(creacion_aux)
            form = ResidenciaForm()
         return HttpResponseRedirect('/listado_residencias')

def crearReservas(residencia, creacion_r):
   reserva= Reserva()
   reserva.semana_del_año=creacion_r
   reserva.residenciaQuePertence=residencia
   reserva.save()

def listado_residencias(request):
    residencias=Residencia.objects.all()
    print(residencias)
    context={'residencias': residencias}
    return render(request,'product.html',context)

def modificar_residencia(request, id):
   if request.method == "POST":
      form = ModResidenciaForm(request.POST)
      if form.is_valid():
         nom = form.cleaned_data['nombre']
         capacidad = form.cleaned_data['capacidad']
         r = Residencia.objects.filter(nombre=nom).exists()
         if not r:
            residencia = Residencia.objects.get(auto_id=id)
            residencia.nombre = nom
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
      

def lunes(residencia_fecha):
   dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', 'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}
   while((dicdias[residencia_fecha.strftime('%A').upper()])!= 'Lunes'):
      residencia_fecha=residencia_fecha + timedelta(days=1)
   return residencia_fecha
      