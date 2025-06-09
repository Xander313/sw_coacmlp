from django.utils.timezone import now
from social_django.models import UserSocialAuth
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from Aplicaciones.Educacion.models import Visitante

@receiver(user_logged_in)
def registrar_visitante(sender, request, user, **kwargs):
    try:
        social = user.social_auth.get(provider='google-oauth2')
        email = social.extra_data.get('email')
        if email:
            Visitante.objects.update_or_create(
                email=email,
                defaults={
                    'ultimoAcceso': now()
                }
            )
            request.session['from_login'] = True
    except UserSocialAuth.DoesNotExist:
        pass
