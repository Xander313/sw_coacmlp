from django.db import models
from Aplicaciones.Capitulo.models import Capitulo


class Examen(models.Model):
    titulo = models.CharField(max_length=200)
    capitulo = models.OneToOneField(Capitulo, related_name='examen', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo
