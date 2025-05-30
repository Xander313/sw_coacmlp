from django.db import models
from Aplicaciones.Educacion.models import Visitante

# Create your models here.
class Certificacion(models.Model):
    visitante = models.OneToOneField(Visitante, related_name='visitante', on_delete=models.CASCADE, null=True, blank=True)
    certificado = models.BooleanField()
    fechaCertificacion = models.DateTimeField()