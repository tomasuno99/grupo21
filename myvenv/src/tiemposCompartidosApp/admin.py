from django.contrib import admin

from .models import Registrado
from .forms import RegModelForm

# Register your models here.

class AdminRegistrado(admin.ModelAdmin):
    list_display= ["nombre", "email", "timestamp"]
    list_editable= ["email"]
    search_fields= ["nombre", "email"]
    form= RegModelForm  # sirve para aplicar los filtros desde Admin
        #class Meta:
        #    model = Registrado


admin.site.register(Registrado, AdminRegistrado)
