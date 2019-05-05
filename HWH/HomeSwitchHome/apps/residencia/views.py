from django.shortcuts import render
from django.http import HttpResponse
from .models import Residencia
# Create your views here.

def product_detail(request):
    residencia=Residencia.objects.get(auto_id=1)
    context={'nombre': residencia.nombre
            , 'capacidad': residencia.capacidad}
    return render(request,'product-detail.html',context)

def prueba(request, id):
    return HttpResponse(id)

def agregar_residencia(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ResidenciaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ResidenciaForm()

    return render(request, 'agregar_residencia.html', {'form': form})