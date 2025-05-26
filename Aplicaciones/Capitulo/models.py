from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

# Capitulo
class Capitulo(models.Model):
    titulo = models.CharField(max_length=500)
    cuerpo = RichTextField() 
    imagenURL = models.TextField()
    videoURL = models.TextField()
    horasProximadas = models.IntegerField()
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(unique=True)
    activacion = models.IntegerField(default=10)
    fechaCreacion = models.DateTimeField()

    def __str__(self):
        return self.titulo

