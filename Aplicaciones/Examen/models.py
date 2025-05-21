from django.db import models

# Create your models here.
class Examen(models.Model):
    titulo = models.CharField(max_length=200)
