from django.db import models
from ckeditor.fields import RichTextField

class Valores(models.Model):
    titulo = models.CharField(max_length=100, default='Valores')
    descripcion = RichTextField(default='Aquí van los valores institucionales...')
