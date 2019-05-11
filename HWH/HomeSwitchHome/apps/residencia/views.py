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
    context={'nombre': residencia.nombre
    , 'capacidad': residencia.capacidad}
    return render(request,'product-detail.html',context)

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
   #instance = Residencia.objects.get(auto_id=id)
   instance = get_object_or_404(Residencia, auto_id=id)
   form = ModResidenciaForm(request.POST or None, instance=instance)
   context={
      'form': form,
      'instance': instance
   }
   
   if form.is_valid():
       form.save()
       return redirect('/listado_residencias')
   return render(request, 'modificar_residencia.html', context) 



def eliminar_residencia(request, id):
    instance = get_object_or_404(Residencia, auto_id=id)
    if request.method == "POST":
        instance.delete()
        return redirect('/listado_residencias')
    context = {
        "instance": instance
    }
    return render(request, "product_delete.html", context)