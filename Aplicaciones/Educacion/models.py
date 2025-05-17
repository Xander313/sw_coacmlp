from django.db import models

# Create your models here.
class Visitante(models.Model):
    email = models.CharField(primary_key=True, unique=True, max_length=256)
    nombreCompleto = models.CharField(max_length=1000)
    ultimoAcceso = models.DateTimeField()

    def __str__(self):
        return self.email
