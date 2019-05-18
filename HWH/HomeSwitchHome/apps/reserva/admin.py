from django.contrib import admin
from apps.reserva.models import Reserva, Subasta, Puja
# Register your models here.

admin.site.register(Reserva)
admin.site.register(Subasta)
admin.site.register(Puja)
