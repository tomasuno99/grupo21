from django.contrib import admin
from django.urls import path
from apps.residencia import views
urlpatterns = [
    path('residencia/<int:id>/', views.product_detail, name='product'),
    path('',views.listado_residencias, name= 'listado_residencias'),
    path('agregar_residencia/', views.Agregar_residencia.as_view(), name='agregar'),
    path('modificar/<int:id>/', views.modificar_residencia, name='modificarResidencia'),
    path('eliminar/<int:id>/', views.eliminar_residencia, name='eliminarResidencia')
]