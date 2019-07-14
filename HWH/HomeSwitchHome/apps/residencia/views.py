from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Residencia, Precio
from .forms import *
from apps.reserva.models import Subasta, Reserva, Hotsale
from apps.reserva.views import chequear_disponibilidad_semana, tiene_algun_hotsale_disponible
from django.views.generic import TemplateView, ListView
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from apps.usuarios.models import CustomUser
from datetime import datetime, timedelta, date
# Create your views here.

def mostrarHome(request):
   residencias = Residencia.objects.filter(is_deleted=False)
   localidades = obtener_localidades(residencias)
   subastas = Subasta.objects.all()
   hotsales = Hotsale.objects.filter(is_active=True)
   hotsales_filtradas = []
   for res in residencias:
      if tiene_algun_hotsale_disponible(res):
         hotsales_filtradas.append(res)
   context = {
      'residencias': residencias,
      'localidades': localidades,
      'premium': Precio.objects.get(nombre="premium"),
      'subastas': subastas,
      'hotsales': hotsales_filtradas,

   }
   return render(request,'home.html',context)

def product_detail(request,id):
   residencia=Residencia.objects.get(auto_id=id)
   if residencia.is_deleted==False:
      related_products= Residencia.objects.exclude(auto_id=id)
      fechas=[]
      for fecha in Reserva.objects.filter(residenciaQuePertence=residencia).values('semana_del_año','auto_id', 'is_active','user','in_hotsale'):
         try:
            subasta= Subasta.objects.get(reserva=fecha['auto_id'])
         except:
            subasta= None
         if subasta:
            if (subasta.is_deleted):
               subasta=None
         print(subasta)
         fechas.append([fecha['auto_id'],((fecha['semana_del_año']).strftime('%d/%m/%Y')), fecha['is_active'],subasta,fecha['user'],fecha['in_hotsale']])
      context= {
         "residencia": residencia,
         "related_products": related_products,
         "fechas": fechas[25:],
         "fechas_hot_sale": fechas[:25]
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
      residencia.nombre = nom
      residencia.capacidad = request.POST['capacidad']
      residencia.direccion = request.POST['direccion']
      residencia.imagen = request.POST['imagen']
      residencia.localidad = request.POST['localidad']
      residencia.descripcion = request.POST['descripcion']
      r = Residencia.objects.filter(nombre=nom).exists()
      if not r: # la residencia no tiene nombre repetido
         residencia.save()
         r= Residencia.objects.get(auto_id=residencia.auto_id)
         creacion_aux=lunes(r.creacion)
         for i in range(1,53):
            crearReservas(r,creacion_aux,i)
            creacion_aux=creacion_aux + timedelta(days=1)
            creacion_aux=lunes(creacion_aux)
      else:
         messages.error(request,'el nombre de la residencia ya existe')
         return render(request,'agregar_residencia.html', context)
      return redirect('/listado_residencias')
   else:
      return render(request,'agregar_residencia.html', context)

def crearReservas(residencia, creacion_r,i):
   reserva= Reserva()
   if i<26:
      reserva.is_active=False
   reserva.semana_del_año=creacion_r
   reserva.residenciaQuePertence=residencia
   reserva.save()

def obtener_localidades(residencias):
   print(residencias)
   localidades = []
   for res in residencias:
      if not res.localidad in localidades and res.localidad != "":
         localidades.append(res.localidad)
   return localidades

def pagina(request):
   return redirect("https://www.lizardsquad.com/")

def listado_residencias(request):
    residencias=Residencia.objects.filter(is_deleted=False)
    localidades = obtener_localidades(residencias)
    context={'residencias': residencias, 'localidades': localidades, 'premium': Precio.objects.get(nombre="premium")}
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
   residencia = Residencia.objects.get(auto_id=id)
   context= {
      'residencia': residencia
   }
   if Residencia.objects.get(auto_id=id).is_deleted==False:
      if request.method == "POST":
         nom = request.POST['nombre']
         residencia.nombre = nom
         residencia.capacidad = request.POST['capacidad']
         residencia.direccion = request.POST['direccion']
         residencia.imagen = request.POST['imagen']
         residencia.localidad = request.POST['localidad']
         residencia.descripcion = request.POST['descripcion']
         r = Residencia.objects.filter(~Q(auto_id=id), nombre=nom).exists()
         if not r: # la residencia no tiene nombre repetido
            residencia.save()
         else:
            messages.error(request,'el nombre de la residencia ya existe')
            return render(request,'modificar_residencia.html', context)
         return redirect('/listado_residencias')
      else:
         return render(request,'modificar_residencia.html', context)
   else: 
      raise Http404  











def eliminar_residencia(request, id):
   if request.method == "GET":
      residencia = Residencia.objects.get(auto_id=id)
      residencia.is_deleted = True
      subastas= Subasta.objects.filter(residencia=residencia)
      for subasta in subastas:
         subasta.is_deleted= True
         subasta.save()
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

def reservar_residencia(request):
   reserva=Reserva.objects.get(auto_id=request.POST.get('id_reserva'))
   if request.user.semanas_disponibles > 0:
      if chequear_disponibilidad_semana(request.user,reserva.semana_del_año):
         print("hola")
         reserva.user= request.user
         reserva.is_active=False
         reserva.save()

         user= CustomUser.objects.get(id=request.user.id)
         user.semanas_disponibles= user.semanas_disponibles - 1
         user.save()
         return JsonResponse({'ok':'ok'},safe=False)
      else:
         return JsonResponse({'ok':'semanaocupada'})
   else:
      return JsonResponse({'ok':'semanas'})
   return JsonResponse({'ok':'notok'},safe=False)

def listado_residencias_filtros(request):
   r = request.POST
   fechaInicio = r['daterange'][:10]
   fechaFin = r['daterange'][17:29]
   residencias= Residencia.objects.filter(is_deleted=False)
   subastas= Subasta.objects.all()
   
   residencias_filtradas= []
   for subasta in subastas:
      if subasta.residencia not in residencias_filtradas:
         if subasta.estaEnElRangoDe(fechaInicio, fechaFin):
            residencias_filtradas.append(subasta.residencia)

   context={'residencias': residencias_filtradas, 'premium': Precio.objects.get(nombre="premium")}
   return render(request,'product.html',context)
def filtrar_residencias(request):
   print(request.GET)
   r = request.POST
   # SE FILTRA POR LOCALIDAD
   residencias_filtradas = []
   print (request.GET.get("localidad"))
   loc = request.GET.get("localidad")
   if loc != "Seleccione una localidad":
      residencias_filtradas=Residencia.objects.filter(is_deleted=False, localidad=loc)
   else:
      residencias_filtradas=Residencia.objects.filter(is_deleted=False)
   if request.GET.get('daterange') != 'Ingrese Fechas Aqui':
      desde= date(int(request.GET.get('daterange')[6:10]),int(request.GET.get('daterange')[3:5]),int(request.GET.get('daterange')[:2]))
      desde=desde+timedelta(days=-desde.weekday())
      hasta = date(int(request.GET.get('daterange')[23:]),int(request.GET.get('daterange')[20:22]),int(request.GET.get('daterange')[17:19]))
      for residencia in residencias_filtradas:
         if not Reserva.objects.filter(residenciaQuePertence=residencia.auto_id,is_active=True,semana_del_año__range=(desde, hasta)):
            residencias_filtradas = residencias_filtradas.exclude(auto_id=residencia.auto_id)
   # guardo todas las localidades disponibles para poder seguir filtrando en el template
   localidades = obtener_localidades(Residencia.objects.filter(is_deleted=False))

   # EN BASE AL FILTRADO ANTERIOR, SE VUELVE A FILTRAR POR FECHAS.
   
   # try:
   #    fechaInicio = r['daterange'][:10]
   #    fechaFin = r['daterange'][17:29]
   # except KeyError:
   #    fechaInicio = str(datetime.now().strftime('%d-%m-%Y'))
   #    fechaFin = str((datetime.now() + timedelta(days=1095)).strftime('%d-%m-%Y'))
   # #residencias= Residencia.objects.filter(is_deleted=False)
   # subastas= Subasta.objects.all()
   # print (fechaFin, fechaInicio)
   # print (residencias_filtradas)
   # for subasta in subastas:
   #    print (subastas)
   #    print (subasta)
   #    if subasta.residencia not in residencias_filtradas:
   #       if subasta.estaEnElRangoDe(fechaInicio, fechaFin):
   #          residencias_filtradas.aadd(subasta.residencia)

   context = {
      "residencias": residencias_filtradas,
      'premium': Precio.objects.get(nombre="premium"),
      "localidades": localidades
   }


   return render(request, "product.html", context)