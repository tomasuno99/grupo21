from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from apps.reserva.models import Reserva, Subasta, Puja, Hotsale
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Max
from apps.usuarios.models import CustomUser
from apps.residencia.models import Precio, Residencia
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
   print (hotsales)

   residencias = Residencia.objects.filter(is_deleted=False)
   residencias_filtradas = []
   print (residencias)
   for res in residencias:
      if tiene_algun_hotsale_disponible(res):
         residencias_filtradas.append(res)
   print (residencias_filtradas)
   
   localidades = obtener_localidades(residencias_filtradas)
   print (localidades)
   context={'residencias': residencias_filtradas, 'localidades': localidades, 'premium': Precio.objects.get(nombre="premium")}
   return render(request,'product.html',context)


def obtener_localidades(residencias):
   print(residencias)
   localidades = []
   for res in residencias:
      if not res.localidad in localidades and res.localidad != "":
         localidades.append(res.localidad)
   return localidades

def tiene_algun_hotsale_disponible(residencia):
        reservasDeLaResidencia = Reserva.objects.filter(residenciaQuePertence=residencia, in_hotsale=True)
        print (reservasDeLaResidencia)
        if len(reservasDeLaResidencia) >= 1:
            return True
        else:
            return False