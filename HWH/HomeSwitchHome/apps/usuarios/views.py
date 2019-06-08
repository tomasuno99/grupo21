from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.contrib.auth import logout as __logout, login as __login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.contrib import messages
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
    user = CustomUser()
    context = baseContext()
    context['user']: { 'usuario': user }
    if request.method == 'POST':
        r = request.POST
        user.nombre = r['firstName'] 
        user.apellido = r['lastName']
        user.fecha_nacimiento = r['birthDay']
        user.email = r['email']
        user.dni = r['dni']
        # esto lo habia puesto para no perder los datos ante un error, pero no funciona
        try:
            
            if int(r['birthDay'][-4:]) <= 2001:
                if r['password'] == r['confirmPassword']:
                    usuario = CustomUser.objects.create_user(email=r['email'], nombre=r['firstName'], apellido=r['lastName'], dni=r['dni'], fecha_nacimiento=r['birthDay'], password=r['password'])
                    return HttpResponseRedirect('/listado_residencias')
                else:
                    messages.error(request,'Las contraseñas ingresadas no coinciden')
                    return render(request,'registrar.html', context)    
            else:
                messages.error(request,'Debes ser mayor de edad para registrarte')
                return render(request,'registrar.html', context)
        except IntegrityError:
            messages.error(request, 'Ese Email ya esta registrado')
            # context['error'] = {'mensaje': 'Ese usuario ya esta registrado'}
            return render(request, 'registrar.html', context)
    else:
        return render(request,'registrar.html', context)
    # return render(request, 'registrar.html')
