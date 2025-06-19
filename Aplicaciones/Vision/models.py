from django.db import models
from ckeditor.fields import RichTextField


class Vision(models.Model):
    titulo = models.CharField(max_length=100, default='Visión')
    descripcion = RichTextField(default='Nuestra visión es ser una cooperativa líder que transforma vidas con valores Salesianos.')