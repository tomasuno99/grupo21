from django.contrib import admin
from django.urls import path
from apps.residencia import views
urlpatterns = [
    path('residencia/', views.product_detail),
    path('residencia/<id>', views.prueba, name='prue'),
]