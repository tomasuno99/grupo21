from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Residencia
from .forms import *
from apps.reserva.models import *
from django.views.generic import TemplateView, ListView
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.contrib import messages
# Create your views here.

def product_detail(request,id):
   residencia=Residencia.objects.get(auto_id=id)
   if residencia.is_deleted==False:
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
   else:
      raise Http404


def prueba(request, id):
    return HttpResponse(id)

def Agregar_residencia(request):
   residencia = Residencia()
   context= {
      'residencia': residencia
   }
   if request.method == "POST":
      nom = request.POST['nombre']
      capacidad = request.POST['capacidad']
      direccion = request.POST['direccion']
      r = Residencia.objects.filter(nombre=nom).exists()
      if not r: # la residencia no tiene nombre repetido
         residencia.nombre = nom
         residencia.capacidad = capacidad
         residencia.direccion = direccion
         residencia.save()
         r= Residencia.objects.get(auto_id=residencia.auto_id)
         creacion_aux=lunes(r.creacion)
         for i in range(1,53):
            crearReservas(r,creacion_aux)
            creacion_aux=creacion_aux + timedelta(days=1)
            creacion_aux=lunes(creacion_aux)
      else:
         messages.error(request,'el nombre de la residencia ya existe')
         return render(request,'agregar_residencia.html', context)
      return redirect('/listado_residencias')
   else:
      return render(request,'agregar_residencia.html', context)

def crearReservas(residencia, creacion_r):
   reserva= Reserva()
   reserva.semana_del_año=creacion_r
   reserva.residenciaQuePertence=residencia
   reserva.save()

def listado_residencias(request):
    residencias=Residencia.objects.filter(is_deleted=False)
    print(residencias)
    context={'residencias': residencias}
    return render(request,'product.html',context)

# def modificar_residencia(request, id):
#    if request.method == "POST":
#       form = ModResidenciaForm(request.POST)
#       if form.is_valid():
#          nom = form.cleaned_data['nombre']
#          capacidad = form.cleaned_data['capacidad']
#          r = Residencia.objects.filter(nombre=nom).exists()
#          if not r:
#             residencia = Residencia.objects.get(auto_id=id)
#             residencia.nombre = nom
#             residencia.capacidad = capacidad
#             residencia.save()
#             form = ModResidenciaForm()
#          return redirect('/listado_residencias')
#    else:
#       form = ModResidenciaForm()
#       return render(request,'modificar_residencia.html', {'id': id, 'form': form})


def modificar_residencia(request, id):
   
   context= {
      'residencia': Residencia.objects.get(auto_id=id)
   }
   if request.method == "POST":
      nom = request.POST['nombre']
      capacidad = request.POST['capacidad']
      direccion = request.POST['direccion']
      r = Residencia.objects.filter(nombre=nom).exists()
      if not r: # la residencia no tiene nombre repetido
         residencia = Residencia.objects.get(auto_id=id)
         residencia.nombre = nom
         residencia.capacidad = capacidad
         residencia.direccion = direccion
         residencia.save()
      else:
         messages.error(request,'el nombre de la residencia ya existe')
         return render(request,'modificar_residencia.html', context)
      return redirect('/listado_residencias')
   else:
      return render(request,'modificar_residencia.html', context)












def eliminar_residencia(request, id):
   if request.method == "GET":
      residencia = Residencia.objects.get(auto_id=id)
      residencia.is_deleted = True
      residencia.save()
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
      