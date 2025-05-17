from django.utils.timezone import now
from .models import Visitante
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated

def get_user_by_email(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    email = details.get('email')
    if email:
        User = get_user_model()
        try:
            # Solo devolvemos el usuario si no tiene una cuenta social asociada
            user = User.objects.get(email=email)
            if not user.social_auth.filter(provider='google-oauth2').exists():
                return {'user': user}
            return None
        except User.DoesNotExist:
            return None

def guardar_visitante(strategy, details, backend, user=None, *args, **kwargs):
    if backend.name != 'google-oauth2' or not user:
        return

    email = details.get('email')
    if not email:
        return

    visitante, creado = Visitante.objects.get_or_create(
        email=email,
        defaults={'ultimoAcceso': now()}
    )

    if not creado:
        visitante.ultimoAcceso = now()
        visitante.save()

def prevent_account_conflict(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return None
    
    email = details.get('email')
    if email:
        User = get_user_model()
        # Verificamos si existe un usuario con este email Y tiene cuenta social asociada
        users = User.objects.filter(email=email, social_auth__provider='google-oauth2')
        if users.exists():
            raise AuthAlreadyAssociated(backend)
    
    return None