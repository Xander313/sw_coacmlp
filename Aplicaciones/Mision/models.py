from django.db import models
from ckeditor.fields import RichTextField

class Mision(models.Model):
    titulo = models.CharField(max_length=100, default='Misión')
    descripcion = RichTextField(default='La Cooperativa tiene como misión apoyar y promover el desarrollo ' \
    'social e integral de sus cooperados, por medio de la democratización del crédito en los ' \
    'segmentos productivos, rurales y urbanos marginales, brindando confianza y seguridad, ' \
    'con eficiencia, honestidad, responsabilidad, calidad y carisma Salesiano.')
