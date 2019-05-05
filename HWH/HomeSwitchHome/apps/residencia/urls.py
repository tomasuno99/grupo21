from django.contrib import admin
from django.urls import path
from apps.residencia.views import index, prueba
urlpatterns = [
    path('residencias', index),
    path('residencias/<id>', prueba, name='prue'),
]