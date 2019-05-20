from django.contrib import admin
from django.urls import path
from apps.residencia import views
from apps.reserva.views import publicarSubasta, listado_subastas, subasta_detail
urlpatterns = [
    path('listado_residencias/residencia/<int:id>/', views.product_detail, name='product'),
    path('listado_subastas/subasta/<int:id>/', subasta_detail, name='subasta'),
    path('listado_residencias/',views.listado_residencias, name= 'listado_residencias'),
    path('agregar_residencia/', views.Agregar_residencia, name='agregar'),
    path('modificar/<int:id>/', views.modificar_residencia, name='modificarResidencia'),
    path('eliminar/<int:id>/', views.eliminar_residencia, name='eliminarResidencia'),
    path('publicar_subasta/<int:id>/', publicarSubasta, name='publicarSubasta' ),
    path('listado_subastas/', listado_subastas, name='listado_subastas'),
    path('index/', views.mostrar_index, name='index')
]