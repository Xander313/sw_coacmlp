from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Capitulo(models.Model):
    titulo = models.CharField(max_length=500)
    cuerpo = RichTextField() 
    imagenURL = models.TextField()
    videoURL = models.TextField()
    horasProximadas = models.IntegerField()
    activo = models.BooleanField(default=True)
    orden = models.IntegerField()
    fechaCreacion = models.DateTimeField()
    idExamen = models.OneToOneField(
        'Examen.Examen',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='capitulo'
    )


