from django.contrib import admin
from django.urls import path
from apps.usuarios import views
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registrar/', views.user_register,name='registrar'),
    path('cambiaNormal/', views.cambiaraNormal,name='cambiaraNormal'),
    path('cambiaStaff/', views.cambiaraStaff,name='cambiaraStaff'),
    path('logout', views.logout, name='logout')
]