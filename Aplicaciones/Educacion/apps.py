from django.apps import AppConfig


class EducacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Educacion'

    def ready(self):
        import Aplicaciones.Educacion.signals
