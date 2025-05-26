from django.db import models
from Aplicaciones.Examen.models import Examen


# Pregunta
class Pregunta(models.Model):
    texto = models.TextField()
    examen = models.ForeignKey(Examen, related_name='preguntas', on_delete=models.CASCADE)

    def __str__(self):
        return self.texto
