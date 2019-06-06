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

def switchStaff(request):
    user = request.user
    if user.is_staff == False:
        user.is_staff = True
    else:
        user.is_staff = False
    user.save()
    print('cambiado')
    return redirect('/listado_residencias')


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

def user_register(request):
    if request.method == 'POST':
        try:
            r = request.POST
            usuario = CustomUser.objects.create(user=user, nombre=r['firstName'], apellido=r['lastName'], dni=r['dni'],
                                             fechaDeNacimiento=r['birthDay'])

            return render(request, 'listado_residencias.html')
        except IntegrityError:
            context = {'error': 'Ese usuario ya esta registrado'}
            return render(request, 'registrar.html', context)
    
    return HttpResponseRedirect('signin')
