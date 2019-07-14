from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pujar/',views.pujar, name='pujar'),
    path('publicar_hotsale/', views.publicarHotsale, name='publicarHotsale'),
]
