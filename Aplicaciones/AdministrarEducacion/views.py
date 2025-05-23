from django.shortcuts import render,redirect
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Capitulo.forms import CuerpoForm




def index(request):
    return render(request, 'AdministrarEducacion/sesionIniciada.html')

def administracion(request):
    capitulos = Capitulo.objects.all()
    return render(request, 'AdministrarEducacion/modulos.html', {'capitulos': capitulos})




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

from Aplicaciones.Examen.models import Examen  # Ajusta el import según tu estructura
from django.utils import timezone

def crearNuevoCapitulo(request):
    if request.method == 'POST':
        form = CuerpoForm(request.POST)
        if form.is_valid():
            cuerpo = form.cleaned_data['cuerpo']
            titulo = request.POST.get('titulo')
            orden = request.POST.get('orden')
            imagenURL = request.POST.get('imagenURL')
            videoURL = request.POST.get('videoURL')
            haprox = request.POST.get('haprox')
            aplica_examen = request.POST.get('examenS') == 'on'

            nuevo_examen = None
            if aplica_examen:
                pregunta = request.POST.get('pregunta') 

                nuevo_examen = Examen.objects.create(
                    pregunta=pregunta
                )

            capitulo = Capitulo.objects.create(
                titulo=titulo,
                orden=orden,
                cuerpo=cuerpo,
                horasProximadas=haprox,
                imagenURL=imagenURL,
                videoURL=videoURL,
                fechaCreacion=timezone.now(),
                idExamen=nuevo_examen
            )

            return redirect('administracion')
    else:
        form = CuerpoForm()

    return render(request, 'AdministrarEducacion/nuevoCapitulo.html', {
        'form': form
    })
