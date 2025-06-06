from django.shortcuts import render,redirect, get_object_or_404
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Capitulo.forms import CuerpoForm
from Aplicaciones.Examen.models import Examen  
from Aplicaciones.Pregunta.models import Pregunta
from Aplicaciones.Respuesta.models import Respuesta
from django.utils import timezone 
from django.contrib import messages
from functools import wraps



def admin_required(tipo_admin):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('admin_token') == tipo_admin:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "No tienes permiso para acceder a esta página. Por favor, inicia sesión.")
                return redirect('loginAdministracion')
        return _wrapped_view
    return decorator

@admin_required('educacion')
def index(request):
    messages.success(request, "¡Todo en orden, se ha inicado sesión!")
    return render(request, 'AdministrarEducacion/sesionIniciada.html')


@admin_required('educacion')
def administracion(request):
    capitulos = Capitulo.objects.all()
    return render(request, 'AdministrarEducacion/modulos.html', {'capitulos': capitulos})


@admin_required('educacion')
def crearCapitulo(request):
    if request.method == 'POST':
        form = CuerpoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administracion')
    else:
        form = CuerpoForm()
    
    return render(request, 'AdministrarEducacion/nuevoCapitulo.html', {
        'form': form 
    })


@admin_required('educacion')
def crearNuevoCapitulo(request):
    if request.method == 'POST':
        form = CuerpoForm(request.POST)
        if form.is_valid():
            cuerpo = form.cleaned_data['cuerpo']
            titulo = request.POST.get('titulo')
            orden = int(request.POST.get('orden'))
            imagenURL = request.POST.get('imagenURL')
            videoURL = request.POST.get('videoURL')
            haprox = request.POST.get('haprox')
            timer = request.POST.get('timer')
            aplica_examen = request.POST.get('examenS') == 'on'

            capitulo_existente = Capitulo.objects.filter(orden=orden).first()
            if capitulo_existente:
                messages.error(request,f'Ya existe un capítulo con el número de orden {orden}: "{capitulo_existente.titulo}".')

                preguntas_raw = request.POST.getlist('preguntas')  
                preguntas_data = []

                for key in request.POST:
                    if key.startswith('preguntas[') and '][texto]' in key:
                        index = key.split('[')[1].split(']')[0]
                        texto = request.POST.get(f'preguntas[{index}][texto]', '')
                        respuestas = request.POST.getlist(f'preguntas[{index}][respuestas][]')
                        correcta = request.POST.get(f'preguntas[{index}][respuesta_correcta]')
                        preguntas_data.append({
                            'index': index,
                            'texto': texto,
                            'respuestas': respuestas,
                            'correcta': correcta,
                        })


                return render(request, 'AdministrarEducacion/nuevoCapitulo.html', {
                    'form': form,
                    'titulo': titulo,
                    'orden': orden,
                    'imagenURL': imagenURL,
                    'videoURL': videoURL,
                    'haprox': haprox,
                    'timer': timer,
                    'aplica_examen': aplica_examen,
                    'preguntas_data': preguntas_data
                })

            capitulo = Capitulo.objects.create(
                titulo=titulo,
                orden=orden,
                cuerpo=cuerpo,
                horasProximadas=haprox,
                imagenURL=imagenURL,
                videoURL=videoURL,
                activacion=timer,
                fechaCreacion=timezone.now(),
            )
            if aplica_examen:
                titulo_examen = request.POST.get('titulo_examen', f"Examen de {titulo}")
                examen = Examen.objects.create(
                    titulo=titulo_examen,
                    capitulo=capitulo
                )
                preguntas_data = {}
                for key in request.POST:
                    if key.startswith('preguntas['):
                        partes = key.split('[')
                        index = partes[1][:-1]
                        campo = partes[2][:-1]
                        if index not in preguntas_data:
                            preguntas_data[index] = {}
                        if campo not in preguntas_data[index]:
                            preguntas_data[index][campo] = []
                        if 'respuestas' in key:
                            preguntas_data[index][campo] = request.POST.getlist(key)
                        else:
                            preguntas_data[index][campo] = request.POST.get(key)
                for index, data in preguntas_data.items():
                    texto_pregunta = data.get('texto', '')
                    respuestas = data.get('respuestas', [])
                    correcta = data.get('respuesta_correcta', '')
                    if texto_pregunta.strip() == '':
                        continue  
                    pregunta = Pregunta.objects.create(
                        texto=texto_pregunta,
                        examen=examen
                    )
                    for i, texto_respuesta in enumerate(respuestas):
                        if texto_respuesta.strip() == '':
                            continue 
                        Respuesta.objects.create(
                            texto=texto_respuesta,
                            correcta=(str(i) == str(correcta)),
                            pregunta=pregunta
                        )
            messages.success(request,'¡Se ha creado el capítulo correctamente!')
            return redirect('administracion')
    else:
        form = CuerpoForm()
    return render(request, 'AdministrarEducacion/nuevoCapitulo.html', {
        'form': form
    })




@admin_required('educacion')
def servirEdicion(request, id):
    cap = get_object_or_404(Capitulo, id=id)
    exam = Examen.objects.filter(capitulo=cap).first() 

    if request.method == 'POST':
        form = CuerpoForm(request.POST)
        if form.is_valid():
            # Procesar guardado aquí
            cap.cuerpo = form.cleaned_data['cuerpo']
            cap.save()
            # Redireccionar o mostrar mensaje
            return redirect('alguna_vista')
    else:
        form = CuerpoForm(initial={'cuerpo': cap.cuerpo})

    preguntas_data = []
    if exam is not None:
        for pregunta in exam.preguntas.all():
            respuestas_texto = []
            correcta_index = None
            for i, r in enumerate(pregunta.respuestas.all()):
                respuestas_texto.append(r.texto)
                if r.correcta:
                    correcta_index = i

            preguntas_data.append({
                'index': str(pregunta.id),
                'texto': pregunta.texto,
                'respuestas': respuestas_texto,
                'correcta': str(correcta_index) if correcta_index is not None else ''
            })

    return render(request, 'AdministrarEducacion/editarCapitulo.html', {
        'capitulo': cap,
        'examen': exam,
        'preguntas_data': preguntas_data,
        'form': form 
    })



@admin_required('educacion')
def ejecutarEdicionapitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulo, pk=capitulo_id)
    examen = getattr(capitulo, 'examen', None)
    preguntas_data = []

    if request.method == 'POST':
        form = CuerpoForm(request.POST)

        # Capturar campos del POST
        titulo = request.POST.get('titulo', '').strip()
        orden_str = request.POST.get('orden', '').strip()
        haprox = request.POST.get('haprox', '').strip()
        imagenURL = request.POST.get('imagenURL', '').strip()
        videoURL = request.POST.get('videoURL', '').strip()
        timer = request.POST.get('timer', '').strip()
        aplica_examen = request.POST.get('examenS') == 'on'

        
        try:
            orden = int(orden_str)
        except (ValueError, TypeError):
            messages.error(request, "El campo orden debe ser un número entero válido.")
            orden = None

        
        if orden is not None:
            capitulo_existente = Capitulo.objects.filter(orden=orden).exclude(pk=capitulo.pk).first()
            if capitulo_existente:
                messages.error(
                    request,
                    f'Ya existe un capítulo con el número de orden {orden}: "{capitulo_existente.titulo}".'
                )
                # Extraer preguntas del POST para mantener los datos
                preguntas_data = []
                for key in request.POST:
                    if key.startswith('preguntas[') and '][texto]' in key:
                        index = key.split('[')[1].split(']')[0]
                        texto = request.POST.get(f'preguntas[{index}][texto]', '')
                        respuestas = request.POST.getlist(f'preguntas[{index}][respuestas][]')
                        correcta = request.POST.get(f'preguntas[{index}][respuesta_correcta]')
                        preguntas_data.append({
                            'index': index,
                            'texto': texto,
                            'respuestas': respuestas,
                            'correcta': correcta,
                        })

                return render(request, 'AdministrarEducacion/editarCapitulo.html', {
                    'form': form,
                    'titulo': titulo,
                    'orden': orden_str,
                    'imagenURL': imagenURL,
                    'videoURL': videoURL,
                    'haprox': haprox,
                    'timer': timer,
                    'aplica_examen': aplica_examen,
                    'preguntas_data': preguntas_data,
                    'capitulo': capitulo
                })

        # Validar formulario
        if form.is_valid() and orden is not None:
            # Guardar datos capítulo
            capitulo.titulo = titulo
            capitulo.orden = orden
            capitulo.horasProximadas = haprox
            capitulo.imagenURL = imagenURL
            capitulo.videoURL = videoURL
            capitulo.activacion = timer
            capitulo.cuerpo = form.cleaned_data['cuerpo']
            capitulo.save()

            # Manejo del examen
            if aplica_examen:
                if not examen:
                    examen = Examen.objects.create(titulo=f"Examen de {capitulo.titulo}", capitulo=capitulo)
                else:
                    examen.titulo = f"Examen de {capitulo.titulo}"
                    examen.save()

                # Borrar preguntas previas
                examen.preguntas.all().delete()


                # Reconstruir preguntas y respuestas
                preguntas_data = {}
                for key in request.POST:
                    if key.startswith('preguntas['):
                        partes = key.split('[')
                        index = partes[1][:-1]
                        campo = partes[2][:-1]
                        if index not in preguntas_data:
                            preguntas_data[index] = {}
                        if 'respuestas' in key:
                            preguntas_data[index]['respuestas'] = request.POST.getlist(key)
                        else:
                            preguntas_data[index][campo] = request.POST.get(key)

                for index, data in preguntas_data.items():
                    texto_pregunta = data.get('texto', '').strip()
                    respuestas = data.get('respuestas', [])
                    correcta = data.get('respuesta_correcta', '')
                    if texto_pregunta == '':
                        continue
                    pregunta = Pregunta.objects.create(
                        texto=texto_pregunta,
                        examen=examen
                    )
                    for i, texto_respuesta in enumerate(respuestas):
                        texto_respuesta = texto_respuesta.strip()
                        if texto_respuesta == '':
                            continue
                        Respuesta.objects.create(
                            texto=texto_respuesta,
                            correcta=(str(i) == str(correcta)),
                            pregunta=pregunta
                        )
            else:
                # Si no aplica examen, borramos si existía
                if examen:
                    examen.delete()

            messages.success(request, "¡Capítulo actualizado correctamente!")
            return redirect('administracion')

        else:
            # Formulario inválido o orden inválido, mostrar errores
            if orden is None:
                messages.error(request, "Debe ingresar un número válido para el orden.")

            preguntas_data = []
            for key in request.POST:
                if key.startswith('preguntas[') and '][texto]' in key:
                    index = key.split('[')[1].split(']')[0]
                    texto = request.POST.get(f'preguntas[{index}][texto]', '')
                    respuestas = request.POST.getlist(f'preguntas[{index}][respuestas][]')
                    correcta = request.POST.get(f'preguntas[{index}][respuesta_correcta]')
                    preguntas_data.append({
                        'index': index,
                        'texto': texto,
                        'respuestas': respuestas,
                        'correcta': correcta,
                    })

            return render(request, 'AdministrarEducacion/editarCapitulo.html', {
                'form': form,
                'titulo': titulo,
                'orden': orden_str,
                'imagenURL': imagenURL,
                'videoURL': videoURL,
                'haprox': haprox,
                'timer': timer,
                'aplica_examen': aplica_examen,
                'preguntas_data': preguntas_data,
                'capitulo': capitulo
            })

    else:
        # Método GET: cargar formulario con datos actuales del capítulo
        form = CuerpoForm(initial={'cuerpo': capitulo.cuerpo})

        # Cargar preguntas si existe examen para mostrar en el formulario
        if examen:
            preguntas_data = []
            for pregunta in examen.pregunta_set.all():
                respuestas = list(pregunta.respuesta_set.all())
                preguntas_data.append({
                    'index': pregunta.pk,
                    'texto': pregunta.texto,
                    'respuestas': [r.texto for r in respuestas],
                    'correcta': next((str(i) for i, r in enumerate(respuestas) if r.correcta), '')
                })

        return render(request, 'AdministrarEducacion/editarCapitulo.html', {
            'form': form,
            'titulo': capitulo.titulo,
            'orden': capitulo.orden,
            'imagenURL': capitulo.imagenURL,
            'videoURL': capitulo.videoURL,
            'haprox': capitulo.horasProximadas,
            'timer': capitulo.activacion,
            'aplica_examen': examen is not None,
            'preguntas_data': preguntas_data,
            'capitulo': capitulo
        })

@admin_required('educacion')
def ejecutareliminacionCapitulo(request, id):
    capitulo = Capitulo.objects.get(id=id)
    capitulo.delete()
    messages.success(request, "¡Capítulo eliminado correctamente!")

    return redirect('administracion')

