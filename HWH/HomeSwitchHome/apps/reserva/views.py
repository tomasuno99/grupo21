from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from apps.reserva.models import Reserva, Subasta, Puja, Hotsale
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Max
from apps.usuarios.models import CustomUser
from apps.residencia.models import Precio, Residencia
# from apps.residencia.views import filtrar_residencias NO ME DEJA IMPORTARLO
# from apps.residencia.views import obtener_localidades NO ME DEJA IMPORTARLO
# Create your views here.


def publicarSubasta(request):
   reserva= Reserva.objects.get(auto_id=request.POST.get('auto_id'))
   reserva.is_active=False
   subasta=Subasta()
   subasta.reserva=reserva
   subasta.residencia= reserva.residenciaQuePertence
   subasta.finalizacion= datetime.today() + timedelta(days=3)
 
   
   subasta.save()
   
   reserva.save()

   puja= Puja()
   puja.monto=request.POST.get('monto')
   puja.subasta= subasta
   puja.save()
   
   return JsonResponse({},safe=False)

def listado_subastas(request):
    subastas=Subasta.objects.all()
    context={'subastas': subastas, 'premium':Precio.objects.get(nombre='premium')}
    return render(request,'subastas.html',context)

def hotsale_detail(request,id):
   residencia= Residencia.objects.get(auto_id=id)
   hotsales= Hotsale.objects.all()
   return render(request,'hotsale_detail.html',{'residencia':residencia, 'hotsales':hotsales})

def reservar_hotsale(request):
   reserva=Reserva.objects.get(auto_id=request.POST.get('id_reserva'))
   hotsale=Hotsale.objects.get(id=request.POST.get('id_hotsale'))
   context={}
   if chequear_disponibilidad_semana(request.user,reserva):
      reserva.user=request.user
      reserva.in_hotsale=False
      reserva.reservo_con_hotsale=True
      hotsale.delete()
      reserva.save()
      context['ok']='ok'
      return JsonResponse(context,safe=False)
   else:
      context['ok']='error'
      return JsonResponse(context,safe=False)

def subasta_detail(request,id):
   subasta=Subasta.objects.get(id=id)
   if subasta.is_deleted==False:
      related_products= Subasta.objects.filter(is_deleted=False).exclude(id=id)
      puja = Puja.objects.filter(subasta=subasta).last()
      if puja == None:
         puja=Puja()
         puja.monto=0
      context= {
         "subasta": subasta,
         "related_products": related_products,
         "puja": puja,
         "cantidad_pujas": len(Puja.objects.all())
      }
      return render(request,'subasta_detail.html', context)
   else:
      raise Http404

def modificar_monto(request):
   if request.POST.get('monto'):
      if float(request.POST.get('monto')) < 1:
         return JsonResponse({'ok':'error'},safe=False)
      else:
         puja= Puja.objects.get(id=request.POST.get('id'))
         puja.monto= request.POST['monto']
         puja.save()
         return JsonResponse({'ok':'ok'},safe=False)
   else:
      return JsonResponse({'ok':'error'},safe=False)


def subasta_detail_puja(request,id):
   print("hola")
   subasta= Subasta.objects.get(id=id)

   monto= request.POST['monto']
   user = request.user
   puja = Puja.objects.filter(subasta=subasta).last()
   if puja == None:
      puja=Puja()
      puja.monto=0
   print(puja.monto)

   related_products= Subasta.objects.filter(is_deleted=False).exclude(id=id)
   context= {
      "subasta": subasta,
      "relate_products": related_products,
      "puja": puja
   }

   if int(monto) > int(puja.monto):
      puja= Puja()
      puja.subasta= subasta
      puja.user=user
      puja.monto=monto
      context['puja']=puja
      puja.save()

   else:
      messages.error(request,'El monto ingresado no supera el actual')
      return render(request,'subasta_detail.html',context)
   return render(request,'subasta_detail.html', context)

def pujar(request):
   montoAux= request.GET['monto']
   print (montoAux)
   p = Puja()
   p.monto = montoAux
   p.save()


def devolver_puja_maxima(pujas):
   max=0
   for puja in pujas:
      if puja.monto > max:
         max=puja.monto
         pujamax=puja
   return pujamax

def chequear_disponibilidad_semana(user,semana):
   reservas= Reserva.objects.filter(user=user)
   for reserva in reservas:
      if (reserva.semana_del_año == semana):
         return False
   return True

def actualizar_reserva(id_reserva,user):
   reserva= Reserva.objects.get(auto_id=id_reserva)
   user= CustomUser.objects.get(id=user)

   reserva.user= user
   reserva.save()
   user.save()
   
   

def finalizar_subasta(request):
   subasta= Subasta.objects.get(id=request.POST.get('subasta_id'))
   pujas= list(Puja.objects.filter(subasta=subasta))
   boolean=True
   while boolean:
      pujamax=devolver_puja_maxima(pujas)
      if not pujamax.user:
         subasta.is_deleted=True
         subasta.reserva=None
         subasta.save()
         return JsonResponse({'usuario': 'usuario','msj': 'No pudo asignarse la reserva a ningun Usuario'}, safe=False)
      user= CustomUser.objects.get(id=pujamax.user.id)
      if user.semanas_disponibles > 0:
         if chequear_disponibilidad_semana(user,subasta.reserva.semana_del_año):
            user.semanas_disponibles=user.semanas_disponibles - 1
            subasta.is_deleted=True
            actualizar_reserva(subasta.reserva.auto_id,user.id)
            subasta.save()
            email= user.email
            user.save()
            return JsonResponse({"usuario": email}, safe=False)
         else:
            pujas.remove(pujamax)
      else:
         pujas.remove(pujamax)
   return JsonResponse({},safe=False)


def publicarHotsale(request):
   r = request.POST
   reserva = Reserva.objects.get(auto_id=r["auto_id"])
   reserva.in_hotsale = True
   Hotsale.objects.create(precio=r["monto"], reserva=reserva, is_active=True)
   reserva.save()
   return JsonResponse({},safe=False)

def listadoHotsales(request):
   r = request.POST
   hotsales = Hotsale.objects.filter(is_active=True)

   residencias = Residencia.objects.filter(is_deleted=False)
   residencias_filtradas = []
   for res in residencias:
      if tiene_algun_hotsale_disponible(res):
         residencias_filtradas.append(res)
   
   localidades = obtener_localidades(residencias_filtradas)
   context={'residencias': residencias_filtradas, 'localidades': localidades, 'premium': Precio.objects.get(nombre="premium")}
   return render(request,'listado_hotsales.html',context)


def obtener_localidades(residencias):
   localidades = []
   for res in residencias:
      if not res.localidad in localidades and res.localidad != "":
         localidades.append(res.localidad)
   return localidades

def tiene_algun_hotsale_disponible(residencia):
        reservasDeLaResidencia = Reserva.objects.filter(residenciaQuePertence=residencia, in_hotsale=True)
        if len(reservasDeLaResidencia) >= 1:
            return True
        else:
            return False

def filtrar_residencias(request):
   print(request.GET)
   r = request.POST
   # SE FILTRA POR LOCALIDAD
   residencias_filtradas = []
   print (request.GET.get("localidad"))
   loc = request.GET.get("localidad")
   if loc != "Seleccione una localidad":
      residencias_filtradas=filtrar_las_que_tienen_hotsale(Residencia.objects.filter(is_deleted=False, localidad=loc))
   else:
      residencias_filtradas=filtrar_las_que_tienen_hotsale(Residencia.objects.filter(is_deleted=False))
   # if request.GET.get('daterange') != 'Ingrese Fechas Aqui':
   #    desde= date(int(request.GET.get('daterange')[6:10]),int(request.GET.get('daterange')[3:5]),int(request.GET.get('daterange')[:2]))
   #    desde=desde+timedelta(days=-desde.weekday())
   #    hasta = date(int(request.GET.get('daterange')[23:]),int(request.GET.get('daterange')[20:22]),int(request.GET.get('daterange')[17:19]))
   #    for residencia in residencias_filtradas:
   #       if not Reserva.objects.filter(residenciaQuePertence=residencia.auto_id,is_active=True,semana_del_año__range=(desde, hasta)):
   #          residencias_filtradas = residencias_filtradas.exclude(auto_id=residencia.auto_id)
   # # guardo todas las localidades disponibles para poder seguir filtrando en el template
   localidades = obtener_localidades(filtrar_las_que_tienen_hotsale(Residencia.objects.filter(is_deleted=False)))
   context = {
      "residencias": residencias_filtradas,
      'premium': Precio.objects.get(nombre="premium"),
      "localidades": localidades
   }


   return render(request, 'listado_hotsales.html', context)

def filtrar_las_que_tienen_hotsale(residencias):
   residencias_filtradas = []
   for res in residencias:
      if tiene_algun_hotsale_disponible(res):
         residencias_filtradas.append(res)
   return residencias_filtradas


def cancelarHotsale(request):
   r = request.POST
   reserva = Reserva.objects.get(auto_id=r["auto_id"])
   reserva.in_hotsale = False

   Hotsale.objects.get(reserva=reserva).delete()  
   reserva.save()
   return JsonResponse({},safe=False)