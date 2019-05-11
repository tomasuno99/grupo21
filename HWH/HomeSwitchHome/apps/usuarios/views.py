from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.contrib.auth import logout as __logout, login as __login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone


def baseContext():
    return {
        'footer': {}
    }

def user_login(request):
    context = baseContext()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            ## se autentico bien
            __login(request, user)

            return HttpResponseRedirect('/index')
        else:
            ## algun dato esta mal
            context['error'] = {'message': 'E-mail inexistente, o contraseña invalida'}

    return render(request, 'login.html', context)

