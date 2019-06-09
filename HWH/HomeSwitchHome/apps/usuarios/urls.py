from django.contrib import admin
from django.urls import path
from apps.usuarios import views
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registrar/', views.user_register,name='registrar'),
    path('switchStaff/', views.switchStaff,name='switchStaff'),
    path('logout', views.logout, name='logout'),
    path('mostrar_perfil', views.mostrar_perfil, name='mostrar_perfil')
]