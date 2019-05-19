from django.db import models
from apps.residencia.models import Residencia
from apps.usuarios.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.




class Reserva(models.Model):
    auto_id= models.AutoField(primary_key=True)
    semana_del_año= models.DateField(null=True)
    reservas= models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='historial_reservas', blank=True) # historial de reservas
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # reserva actual
    residenciaQuePertence= models.ForeignKey(Residencia, on_delete=models.CASCADE, null=True, related_name='residencia_actual')



class Subasta(Reserva):
    finalizacion= models.DateField(null=True)


class Puja(models.Model):
    monto= models.IntegerField()
    subasta= models.ForeignKey(Subasta, null=True, blank=True, on_delete=models.CASCADE)
    user= models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
