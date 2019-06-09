from django.shortcuts import render, HttpResponseRedirect, Http404, redirect, HttpResponse
from django.contrib.auth import logout as __logout, login as __login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import time
from apps.residencia.models import Precio
from apps.reserva.models import Reserva
from django.http import JsonResponse
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
        print(r['birthDay'])
        user.email = r['email']
        user.dni = r['dni']
        # esto lo habia puesto para no perder los datos ante un error, pero no funciona
        try:
            if int(r['birthDay'][-4:]) <= 2001:
                if r['password'] == r['confirmPassword']:
                    pass
                else:
                    messages.error(request,'Las contraseñas ingresadas no coinciden')
                    return render(request,'registrar.html', context)    
            else:
                messages.error(request,'Debes ser mayor de edad para registrarte')
                return render(request,'registrar.html', context)
            if (len(r['numero_tarjeta']) == 16):
                if r['fecha_vencimiento'][-2] > time.strftime("%d/%m/%y")[-2]:
                    usuario = CustomUser.objects.create_user(email=r['email'], nombre=r['firstName'], apellido=r['lastName'], dni=r['dni'], fecha_nacimiento=r['birthDay'], password=r['password'], num_tarjeta_credito=r['numero_tarjeta'], nombre_titular_tarjeta=r['nombre_tarjeta'], fecha_vencimiento_tarjeta=r['fecha_vencimiento'], codigo_seguridad_tarjeta=r['securityCode'], marca_tajeta=r['cardBrand'])
                    return HttpResponseRedirect('/listado_residencias')    
                else:    
                    messages.error(request,'La tarjeta ingresada se encuentra Vencida')
                    return render(request,'registrar.html', context)        
            else:    
                messages.error(request,'El numero de tarjeta debe tener 16 digitos')
                return render(request,'registrar.html', context)
            
        except IntegrityError:
            messages.error(request, 'Ese Email ya esta registrado')
            # context['error'] = {'mensaje': 'Ese usuario ya esta registrado'}
            return render(request, 'registrar.html', context)
    else:
        return render(request,'registrar.html', context)
    # return render(request, 'registrar.html')

def mostrar_perfil(request):
    clientes= CustomUser.objects.exclude(is_staff=True)
    context= {'user': request.user, 'premium': Precio.objects.get(nombre="premium"), 'basico': Precio.objects.get(nombre="basico"), 'clientes': clientes
    , 'reservas': Reserva.objects.filter(user=request.user),
    'dia': request.user.fecha_nacimiento[:2],
    'mes': request.user.fecha_nacimiento[3:5],
    'año': request.user.fecha_nacimiento[6:]}
    return render(request,'perfil.html', context)

def modificar_precio_premium(request):
    precio= Precio.objects.get(nombre="premium")
    
    precio.precio= float(request.POST.get('precio'))

    precio.save()

    return JsonResponse({},safe=False)


def modificar_precio_basico(request):
    precio= Precio.objects.get(nombre="basico")
    
    precio.precio= float(request.POST.get('precio'))

    precio.save()

    return JsonResponse({},safe=False)

def cambiar_a_basico(request):
    cliente= CustomUser.objects.get(id= request.POST.get('id_cliente'))

    cliente.is_premium=False

    cliente.save()

    return JsonResponse({},safe=False)

def cambiar_a_premium(request):
    cliente= CustomUser.objects.get(id= request.POST.get('id_cliente'))

    cliente.is_premium=True

    cliente.save()

    return JsonResponse({},safe=False)

def modificar_perfil(request):
    if (request.POST.get('nombre') == "" or request.POST.get('apellido') == "" or request.POST.get('fechanacimiento') == "" or request.POST.get('dni') == "" or request.POST.get('email') == ""):
        return JsonResponse({'ok': 'Debe rellenar todos los campos'},safe=False)
    dia=(request.POST.get('fechanacimiento')[8:]+ '/')
    mes=(request.POST.get('fechanacimiento')[5:7] + '/')
    año=(request.POST.get('fechanacimiento')[:4])
    fecha= dia+mes+año

    usuarios= CustomUser.objects.exclude(id=request.user.id)
    
    for usuario in usuarios:
        if request.POST.get('email') == usuario.email:
            return JsonResponse({'ok':'Ya existe una cuenta con ese Mail'}, safe=False)
    if int(año) >= 2001:
        return JsonResponse({'ok': 'Tiene que ser mayor de 18 años'})
    
    usuario= CustomUser.objects.get(id=request.user.id)

    usuario.nombre= request.POST.get('nombre')
    usuario.apellido= request.POST.get('apellido')
    usuario.dni= request.POST.get('dni')
    usuario.email= request.POST.get('email')
    usuario.fecha_nacimiento= fecha

    usuario.save()
    return JsonResponse({'ok':'ok'},safe=False)

def modificar_tarjeta(request):
    if (request.POST.get('tarjeta') == "" or request.POST.get('titular') == "" or request.POST.get('vencimiento') == "" or request.POST.get('codigo-seguridad') == "" or request.POST.get('marca') == ""):
        return JsonResponse({'ok': 'Debe rellenar todos los campos'},safe=False)
    if len(request.POST.get('tarjeta'))!= 16:
        return JsonResponse({'ok': 'El numero de la tarjeta debe ser de 16 digitos'},safe=False)
    if request.POST.get('vencimiento')[-2] < time.strftime("%d/%m/%y")[-2]:
        return JsonResponse({'ok': 'La Tarjeta esta vencida'})
    
    if len(request.POST.get('vencimiento')) != 5:
        return JsonResponse({'ok':'Ingrese el vencimiento de forma correcta'}, safe=False)

    usuario= CustomUser.objects.get(id=request.user.id)

    usuario.num_tarjeta_credito=request.POST.get('tarjeta')
    usuario.nombre_titular_tarjeta= request.POST.get('titular')
    usuario.fecha_vencimiento_tarjeta= request.POST.get('vencimiento')
    usuario.codigo_seguridad_tarjeta= request.POST.get('codigo-seguridad')
    usuario.marca_tajeta= request.POST.get('marca')

    usuario.save()


    return JsonResponse({'ok':'ok'},safe=False)

def modificar_contraseña(request):
    if request.POST.get('contraseña') == "" or request.POST.get('confirmar')=="":
        return JsonResponse({'ok':'Debe completar todos los campos'},safe=False)
    if request.POST.get('contraseña')!= request.POST.get('confirmar'):
        return JsonResponse({'ok':'Las contraseñas no coinciden'},safe=False)
    usuario= CustomUser.objects.get(id=request.user.id)
    usuario.set_password(request.POST.get('contraseña'))
    usuario.save()

    return JsonResponse({'ok':'ok'},safe=False)