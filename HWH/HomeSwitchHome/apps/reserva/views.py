from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from apps.reserva.models import Reserva,Subasta,Puja
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Max
from apps.usuarios.models import CustomUser
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
    context={'subastas': subastas}
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
         "puja": puja
      }
      return render(request,'subasta_detail.html', context)
   else:
      raise Http404
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

def finalizar_subasta(request):
   subasta= Subasta.objects.get(id=request.POST.get('subasta_id'))
   pujas= Puja.objects.filter(subasta=subasta)
   boolean=True
   while boolean:
      pujamax=devolver_puja_maxima(pujas)
      user= CustomUser.objects.get(id=pujamax.user.id)
      if user.semanas_disponibles > 0:
         if chequear_disponibilidad_semana(user,subasta.reserva.semana_del_año):
            user.semanas_disponibles=user.semanas_disponibles - 1
            subasta.reserva.user= user
            subasta.is_deleted=True
            subasta.save()
            user.save()
            print("hola entre jejejeje")
            return JsonResponse({"usuario": subasta.reserva.user.email}, safe=False)
      else:
         pujas.remove(pujamax)
   return JsonResponse({},safe=False)