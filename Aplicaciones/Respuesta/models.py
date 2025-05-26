from django.db import models
from Aplicaciones.Pregunta.models import Pregunta
# Create your models here.

# Respuesta
class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    correcta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correcta' if self.correcta else 'Incorrecta'})"
