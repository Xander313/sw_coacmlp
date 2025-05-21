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

class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = RichTextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

