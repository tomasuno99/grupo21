from django.shortcuts import render, render_to_response, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from apps.reserva.models import *
from datetime import datetime, timedelta
from django.contrib import messages
# Create your views here.


def publicarSubasta(request, id):
    reserva= Reserva.objects.get(auto_id=id)
    reserva.is_active=False
    subasta=Subasta()
    subasta.reserva=reserva
    subasta.residencia= reserva.residenciaQuePertence
    subasta.finalizacion= datetime.today() + timedelta(days=3)

    subasta.save()
    reserva.save()
    print(id)

    return redirect('/listado_residencias')

def listado_subastas(request):
    subastas=Subasta.objects.all()
    context={'subastas': subastas}
    return render(request,'subastas.html',context)

def subasta_detail(request,id):
   subasta=Subasta.objects.get(id=id)
   if subasta.is_deleted==False:
      related_products= Subasta.objects.filter(is_deleted=False).exclude(id=id)
      context= {
         "subasta": subasta,
         "related_products": related_products,
      }
      return render(request,'subasta_detail.html', context)
   else:
      raise Http404

def pujar(request):
   montoAux= request.GET['monto']
   print (montoAux)
   p = Puja()
   p.monto = montoAux
   p.save()