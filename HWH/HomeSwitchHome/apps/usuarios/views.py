from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.contrib.auth import logout as __logout, login as __login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm


def baseContext():
    return {
        'footer': {}
    }

def cambiaraNormal(request):
    user = request.user
    user.is_staff = False
    user.save()
    print('cambiado a normal')
    return redirect('/listado_residencias')

def cambiaraStaff(request):
    user = request.user
    user.is_staff = True
    user.save()
    print('cambiado a staff')
    return redirect('/listado_residencias')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/listado_residencias')
    else:
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request,'registrar.html',context)

def user_login(request):
    context = baseContext()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            ## se autentico bien
            __login(request, user)

            return HttpResponseRedirect('/listado_residencias')
        else:
            ## algun dato esta mal
            context['error'] = {'message': 'E-mail inexistente, o contraseña invalida'}

    return render(request, 'login.html', context)

def logout(request):
    __logout(request)
    print('logout')
    return redirect('index')