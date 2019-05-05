from django.db import models

# Create your models here.


class Residencia(models.Model):
    auto_id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField(null=True, blank=True)


