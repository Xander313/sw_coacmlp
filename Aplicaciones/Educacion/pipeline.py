from django.utils.timezone import now
from .models import Visitante

def guardar_visitante(strategy, details, backend, user=None, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    email = details.get('email')
    if email is None:
        return

    visitante, creado = Visitante.objects.get_or_create(
        email=email,
        defaults={'ultimoAcceso': now()}
    )

    if not creado:
        visitante.ultimoAcceso = now()
        visitante.save()
