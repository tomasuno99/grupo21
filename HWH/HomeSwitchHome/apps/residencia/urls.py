from django.contrib import admin
from django.urls import path
from apps.residencia import views
urlpatterns = [
    path('residencia/<id>', views.product_detail, name='product'),
    path('',views.listado_residencias, name= 'listado_residencias'),
    path('agregar_residencia/', views.agregar_residencia, name='agregar')]

