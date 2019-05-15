from django.contrib import admin
from django.urls import path
from apps.usuarios import views
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registrar/', views.user_register,name='registrar'),
    path('', views.cambiaraNormal,name='cambiaraNormal'),
    path('', views.cambiaraStaff,name='cambiaraStaff')
]