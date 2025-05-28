from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Examen.models import Examen
from django.utils import timezone
from Aplicaciones.Progreso.models import Progreso
from Aplicaciones.Respuesta.models import Respuesta

from .models import Visitante


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
    try:
        esta = Examen.objects.get(capitulo=id)
    except Examen.DoesNotExist:
        esta = None 

    capitulo = Capitulo.objects.get(orden=id)
    lCap = Capitulo.objects.all()

    # Recuperar datos de sesión
    name = request.session.get('name', 'Usuario')
    picture = request.session.get('picture', '')
    email = request.session.get('email', None)

    aprobado = False

    if email:
        try:
            visitante = Visitante.objects.get(email=email)
            progreso = Progreso.objects.get(capitulo=capitulo, visitante=visitante)
            aprobado = progreso.aprobado
        except Progreso.DoesNotExist:
            aprobado = False

    return render(request, 'Educacion/capitulo.html', {
        'capitulo': capitulo,
        'capitulos': lCap,
        'name': name,
        'picture': picture,
        'examen': esta,
        'aprobado': aprobado
    })



def examen(request, id):
    capitulo = get_object_or_404(Capitulo, id=id)

    if not hasattr(capitulo, 'examen'):
        return render(request, 'Educacion/sin_examen.html', {'capitulo': capitulo})

    examen = capitulo.examen
    preguntas = examen.preguntas.prefetch_related('respuestas')

    name = request.session.get('name', 'Usuario')
    picture = request.session.get('picture', '')
    lCap = Capitulo.objects.all()

    return render(request, 'Educacion/examen.html', {
        'capitulo': capitulo,
        'examen': examen,
        'preguntas': preguntas,
        'name': name,
        'picture': picture,
        'capitulos': lCap,

    })


def avanzarCapitulo(request, id):
    capitulo = get_object_or_404(Capitulo, id=id)
    email = request.session.get('email')
    visitante = get_object_or_404(Visitante, email=email)

    progreso_actual, created = Progreso.objects.update_or_create(
        capitulo=capitulo,
        visitante=visitante,
        defaults={
            'calificacion': 10,
            'aprobado': True,
            'fechaProgreso': timezone.now()
        }
    )
    progreso_actual.refresh_from_db()

    todos = set(Capitulo.objects.values_list('id', flat=True))
    aprobados = set(
        Progreso.objects.filter(visitante=visitante, aprobado=True)
        .values_list('capitulo_id', flat=True)
    )
    pendientes = todos - aprobados

    if not pendientes:
        return redirect('certificado')  

    return redirect('capitulo', id=capitulo.id) 


def certificado(request):

    name = request.session.get('name', 'Usuario')
    picture = request.session.get('picture', '')
    lCap = Capitulo.objects.all()

    return render(request, 'Educacion/certificacion.html', {
        'name': name,
        'picture': picture,
        'capitulos': lCap,
    })



def evaluarExamen(request, capitulo_id):
    if request.method == 'POST':
        capitulo = get_object_or_404(Capitulo, id=capitulo_id)
        examen = capitulo.examen
        preguntas = examen.preguntas.prefetch_related('respuestas')

        correctas = 0
        total = preguntas.count()

        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_id:
                respuesta = Respuesta.objects.get(id=respuesta_id)
                if respuesta.correcta:
                    correctas += 1

        nota = Decimal((correctas / total) * 10).quantize(Decimal('0.01'))

        email = request.session.get('email')
        visitante = get_object_or_404(Visitante, email=email)

        progreso, created = Progreso.objects.update_or_create(
            capitulo=capitulo,
            visitante=visitante,
            defaults={
                'calificacion': nota,
                'aprobado': True, 
                'fechaProgreso': timezone.now()
            }
        )
        progreso.refresh_from_db()

        todos = set(Capitulo.objects.values_list('id', flat=True))
        aprobados = set(
            Progreso.objects.filter(visitante=visitante, aprobado=True)
            .values_list('capitulo_id', flat=True)
        )
        pendientes = todos - aprobados

        if not pendientes:
            return redirect('certificado')  

        return redirect('capitulo', id=capitulo.id) 








def perfilVisitante(request):
    email = request.session.get('email')
    visitante = get_object_or_404(Visitante, email=email)

    capitulos = Capitulo.objects.all().order_by('orden')
    progreso_dict = {p.capitulo.id: p for p in Progreso.objects.filter(visitante=visitante)}
    lCap = Capitulo.objects.all()

    actividad = []

    for capitulo in capitulos:
        progreso = progreso_dict.get(capitulo.id)
        actividad.append({
            'orden': capitulo.orden,
            'titulo': capitulo.titulo,
            'fecha': progreso.fechaProgreso.strftime('%Y-%m-%d %H:%M') if progreso else 'No registrado',
            'nota': progreso.calificacion if progreso else 'No registrado',
            'aprobado': 'Sí' if progreso and progreso.aprobado else ('No' if progreso else 'No registrado')
        })

    return render(request, 'Educacion/perfil.html', {
        'name': request.session.get('name'),
        'picture': request.session.get('picture'),
        'actividad': actividad,
        'capitulos': lCap
    })
