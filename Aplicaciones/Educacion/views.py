from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


@never_cache
def salir(request):
    logout(request)
    request.session.flush()
    return redirect('/')



def iniciarSesion(request):
    return render(request, 'iniciarSesion.html')




@never_cache
@login_required
def postlogin(request):
    try:
        user = request.user
        social = user.social_auth.filter(provider='google-oauth2').first()
        picture = social.extra_data.get('picture') if social else None
        name = social.extra_data.get('name') if social else None
        email = social.extra_data.get('email') if social else user.email

        return render(request, 'perfil.html', {
            'user': user,
            'picture': picture,
            'name': name,
            'email': email,
        })

    except Exception as e:

        return redirect('salir_definitivo')


def salirDefinitivo(request):
    logout(request)
    request.session.flush()

    return render(request, 'errorSesion.html')


def volver_inicio(request):
    logout(request)
    request.session.flush()
    return redirect('/')


def error_social_auth(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        return redirect('/')
    return render(request, 'error_social_auth.html')
