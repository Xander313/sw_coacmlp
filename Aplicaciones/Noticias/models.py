from django.db import models
from django.utils import timezone
# Create your models here.
from ckeditor.fields import RichTextField
# Create your models here.
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    imagenURL= models.TextField()
    descripcion= RichTextField()
    fechaCreacion = models.DateTimeField(default=timezone.now)
    referenciaURL= models.TextField() 

