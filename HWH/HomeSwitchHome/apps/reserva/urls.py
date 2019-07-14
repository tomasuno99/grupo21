from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pujar/',views.pujar, name='pujar'),
    path('publicar_hotsale/', views.publicarHotsale, name='publicarHotsale'),
    path('listado_hotsales/', views.listadoHotsales, name='listado_hotsales'),
    path('reservar_hotsale/', views.reservar_hotsale, name='reservar_hotsale'),
    path('listado_hotsales/residencia/<int:id>/', views.hotsale_detail, name='hotsale_detail'),
    path('listado_hotsales/filtrar_residencias/',views.filtrar_residencias, name='filtrar_residencias_hotsale')
]
