from django.db import models
from apps.residencia.models import Residencia
from apps.usuarios.models import CustomUser
# Create your models here.




class Reserva(models.Model):
    auto_id= models.AutoField(primary_key=True)
    residencia= models.ForeignKey(Residencia, null=True,blank=True,on_delete=models.CASCADE)
    reservas= models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='historial_reservas') # historial de reservas
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)  # reserva actual
    residenciaQuePertence= models.OneToOneField(Residencia, on_delete=models.CASCADE, null=True, related_name='residencia_actual')



class Subasta(Reserva):
    pass


class Puja(models.Model):
    monto= models.IntegerField()
    subasta= models.ForeignKey(Subasta, null=True, blank=True, on_delete=models.CASCADE)
    user= models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
