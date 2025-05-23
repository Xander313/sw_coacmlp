from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from Aplicaciones.Capitulo.models import Capitulo


def salir(request):
    logout(request)
    request.session.flush()
    return redirect('/')



def iniciarSesion(request):
    return render(request, 'Educacion/iniciarSesion.html')


@login_required
def postlogin(request):
    try:
        user = request.user
        social = user.social_auth.filter(provider='google-oauth2').first()
        picture = social.extra_data.get('picture') if social else None
        name = social.extra_data.get('name') if social else None
        email = social.extra_data.get('email') if social else user.email

        # Guardar en sesión
        request.session['picture'] = picture
        request.session['name'] = name
        request.session['email'] = email

        lCap = Capitulo.objects.all()

        return render(request, 'Educacion/sesionIniciada.html', {
            'user': user,
            'picture': picture,
            'name': name,
            'email': email,
            'capitulos': lCap 
        })

    except Exception as e:
        print(e)
        return redirect('errorSesion')





def salirDefinitivo(request):
    return render(request, 'Educacion/errorSesion.html')


def volverInicio(request):
    logout(request)
    request.session.flush()
    return redirect('/')



#####################################################################
#####################SIRVIENDO EL CONTENIDO#########################
#####################################################################
def capitulo(request, id):
    capitulo = Capitulo.objects.get(id=id)
    lCap = Capitulo.objects.all()

    # Recuperar datos de sesión
    name = request.session.get('name', 'Usuario')
    picture = request.session.get('picture', '')

    return render(request, 'Educacion/capitulo.html', {
        'capitulo': capitulo,
        'capitulos': lCap,
        'name': name,
        'picture': picture
    })


