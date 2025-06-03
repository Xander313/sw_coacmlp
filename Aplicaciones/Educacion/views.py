from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Examen.models import Examen
from django.utils import timezone
from Aplicaciones.Progreso.models import Progreso
from Aplicaciones.Respuesta.models import Respuesta
from .models import Visitante
from functools import wraps
import os
from django.http import HttpResponse
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.contrib import messages





def session_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('email'):
            return redirect('errorSesion')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



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

        messages.success(request, "¡Sesión iniciada correctamente!")
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
@session_required
def capitulo(request, id):
    try:
        esta = Examen.objects.get(capitulo=id)
    except Examen.DoesNotExist:
        esta = None 

    capitulo = Capitulo.objects.get(orden=id)
    lCap = Capitulo.objects.all()
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')

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


@session_required
def examen(request, id):
    capitulo = get_object_or_404(Capitulo, id=id)
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')

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

@session_required
def avanzarCapitulo(request, id):
    capitulo = get_object_or_404(Capitulo, id=id)
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')
    
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
        messages.success(request, "¡Felicidades, usted ahora puede certificarse!")
        return redirect('perfilVisitante')  
    messages.success(request, "¡Muy bien, ha completado un capítulo más!")
    return redirect('capitulo', id=capitulo.id) 



@session_required
def certificado(request):
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')

    visitante = get_object_or_404(Visitante, email=email)
    name = request.session.get('name', 'Usuario')
    picture = request.session.get('picture', '')

    capitulos = Capitulo.objects.all()

    progreso_dict = {p.capitulo.id: p for p in Progreso.objects.filter(visitante=visitante)}

    todo_aprobado = True
    for capitulo in capitulos:
        progreso = progreso_dict.get(capitulo.id)
        if not (progreso and progreso.aprobado):
            todo_aprobado = False
            break

    return render(request, 'Educacion/certificacion.html', {
        'name': name,
        'picture': picture,
        'capitulos': capitulos,
        'todo_aprobado': todo_aprobado,
    })










@session_required
def evaluarExamen(request, capitulo_id):
    if request.method == 'POST':
        email = request.session.get('email')
        if not email:
            return redirect('errorSesion')
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
            messages.success(request, "¡Felicidades, usted ahora puede certificarse!")
            return redirect('perfilVisitante')  
        messages.success(request, "¡Muy bien, ha completado un capítulo más!")
        return redirect('capitulo', id=capitulo.id) 







@session_required
def perfilVisitante(request):
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')

    visitante = get_object_or_404(Visitante, email=email)

    capitulos = Capitulo.objects.all().order_by('orden')
    progreso_dict = {p.capitulo.id: p for p in Progreso.objects.filter(visitante=visitante)}
    lCap = Capitulo.objects.all()

    actividad = []
    todo_aprobado = True 

    for capitulo in capitulos:
        progreso = progreso_dict.get(capitulo.id)
        aprobado = progreso and progreso.aprobado
        actividad.append({
            'titulo': capitulo.titulo,
            'fecha': progreso.fechaProgreso.strftime('%Y-%m-%d %H:%M') if progreso else 'No registrado',
            'nota': progreso.calificacion if progreso else 'No registrado',
            'aprobado': 'Sí' if aprobado else ('No' if progreso else 'No registrado'),
            'orden': capitulo.orden
        })

        if not aprobado:
            todo_aprobado = False

    return render(request, 'Educacion/perfil.html', {
        'name': request.session.get('name'),
        'picture': request.session.get('picture'),
        'actividad': actividad,
        'capitulos': lCap,
        'todo_aprobado': todo_aprobado
    })



def ejecutarCertificacion(request):
    email = request.session.get('email')
    if not email:
        return redirect('errorSesion')

    visitante = get_object_or_404(Visitante, email=email)

    capitulos = Capitulo.objects.all().order_by('orden')

    progreso_dict = {p.capitulo.id: p for p in Progreso.objects.filter(visitante=visitante)}

    todo_aprobado = True
    for capitulo in capitulos:
        progreso = progreso_dict.get(capitulo.id)
        if not progreso or not progreso.aprobado:
            todo_aprobado = False
            break

    if not todo_aprobado:
        messages.error(request, "Usted no puede certificarse sin antes haber completado todos los capítulos.")
        return redirect('perfilVisitante')

    fuente_path = os.path.join('Aplicaciones', 'static', 'fonts', 'Symphony.ttf')
    pdfmetrics.registerFont(TTFont('Symphony', fuente_path))

    if request.method == "POST":
        nombre_visitante = request.POST.get('nombre')
    else:
        nombre_visitante = request.GET.get('nombre')

    if not nombre_visitante:
        return HttpResponse("Nombre no proporcionado.", status=400)

    plantilla_path = 'Aplicaciones/static/certificado/cert.pdf'

    with open(plantilla_path, "rb") as f:
        lector_pdf = PdfReader(f)
        writer_pdf = PdfWriter()

        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFont("Symphony", 20)
        can.drawString(100, 500, f"{nombre_visitante}")
        can.save()
        packet.seek(0)

        nuevo_pdf = PdfReader(packet)
        pagina = lector_pdf.pages[0]
        pagina.merge_page(nuevo_pdf.pages[0])
        writer_pdf.add_page(pagina)

        salida = io.BytesIO()
        writer_pdf.write(salida)
        salida.seek(0)

    descargar = request.GET.get('descargar') == '1'
    response = HttpResponse(salida.read(), content_type='application/pdf')

    if descargar:
        response['Content-Disposition'] = f'attachment; filename="certificado_{nombre_visitante}.pdf"'
    else:
        response['Content-Disposition'] = 'inline; filename="certificado.pdf"'

    return response