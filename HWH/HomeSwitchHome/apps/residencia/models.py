from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Residencia(models.Model):
    
    
    auto_id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField(null=True, blank=True)
    creacion= models.DateTimeField(('Date created'), auto_now_add=True,null=True)
    direccion = models.CharField(max_length=50, default='')
    #user = models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Residencia"
        verbose_name_plural = "Residencias"


    def getAuto_id(self):
        return self.auto_id