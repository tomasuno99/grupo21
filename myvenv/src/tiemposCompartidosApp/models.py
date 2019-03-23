from django.db import models

# Create your models here.

class Registrado(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


    def __str__(self):
        return self.email
