from django.db import models
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Educacion.models import Visitante

# Create your models here.
class Progreso(models.Model):
    capitulo = models.ForeignKey(Capitulo, related_name='capitulo', on_delete=models.CASCADE, null=True, blank=True)
    visitante = models.ForeignKey(Visitante, related_name='visitante', on_delete=models.CASCADE, null=True, blank=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    aprobado = models.BooleanField(default=True)
    fechaProgreso = models.DateTimeField()

