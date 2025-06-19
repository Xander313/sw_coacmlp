from django.db import models
from ckeditor.fields import RichTextField

class Historia(models.Model):
    titulo = models.CharField(max_length=100, default='Historia')
    descripcion = RichTextField(default='Aquí va la historia institucional...')
