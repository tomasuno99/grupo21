from django.db import models
from apps.residencia.models import Residencia
# Create your models here.


class Reserva(models.Model):
    auto_id= models.AutoField(primary_key=True)
    residencia= models.ForeignKey(Residencia, null=True,blank=True,on_delete=models.CASCADE)