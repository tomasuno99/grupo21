from django.contrib import admin
from django.urls import path
from apps.usuarios import views
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registrar/', views.user_register,name='registrar'),
    path('switchStaff/', views.switchStaff,name='switchStaff'),
    path('logout', views.logout, name='logout'),
    path('mostrar_perfil', views.mostrar_perfil, name='mostrar_perfil'),
    path('modificar_premium', views.modificar_precio_premium, name='modificar_premium'),
    path('modificar_basico', views.modificar_precio_basico, name='modificar_basico'),
    path('cambiar_a_basico', views.cambiar_a_basico, name='cambiar_a_basico'),
    path('cambiar_a_premium', views.cambiar_a_premium, name='cambiar_a_premium'),
    path('modificar_perfil', views.modificar_perfil, name='modificar_perfil'),
    path('modificar_tarjeta', views.modificar_tarjeta, name='modificar_tarjeta'),
    path('modificar_contraseña', views.modificar_contraseña, name='modificar_contraseña'),
    path('get_datos_cliente', views.get_datos_cliente, name='get_datos_cliente'),
    path('get_datos_reserva', views.get_datos_reserva, name='get_datos_reserva'),
    path('cancelar_reserva', views.cancelar_reserva, name='cancelar_reserva'),
    path('baja_admin', views.baja_admin, name='baja_admin'),
    path('alta_admin', views.alta_admin, name='alta_admin')
]