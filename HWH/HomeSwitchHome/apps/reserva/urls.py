from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pujar/',views.pujar, name='pujar'),
    path('publicar_hotsale/', views.publicarHotsale, name='publicarHotsale'),
    path('listado_hotsales/', views.listadoHotsales, name='listado_hotsales'),
    path('listado_hotsales/filtrar_residencias/',views.filtrar_residencias, name='filtrar_residencias_hotsale')
]
