from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps
from Aplicaciones.Noticias.models import Noticia
from Aplicaciones.Noticias.forms import DescripcionForm
from Aplicaciones.Mision.models import Mision


def redireccionador(request):
    return redirect('loginAdministracion')


def admin_required(tipo_admin):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.session.get('admin_token')
            print(f"[Decorador] Tipo requerido: {tipo_admin}, Token actual: {token}")
            if request.session.get('admin_token') == tipo_admin:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "No tienes permiso para acceder a esta página. Por favor, inicia sesión.")
                return redirect('loginAdministracion')
        return _wrapped_view
    return decorator


@admin_required('contenido')
def perfilContenido(request):
    messages.success(request, "¡Todo en orden, se ha inicado sesión!")
    return render(request, 'inicio/inicioSesion.html')

#ACCIONES PARA ADMINISTRAR LAS NOTICAS
#Se mostratará el listado de la noticias disponibles
def inicio(request):
    listadoNoticias = Noticia.objects.all()
    return render(request, "Noticias/iniciote.html", {'noticia': listadoNoticias})
# Crearemos la noticia
def nuevaNoticia(request):
    if request.method == 'POST':
        form = DescripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciote')
    else:
        form = DescripcionForm()
    
    return render(request,"Noticias/nuevaNoticia.html", {
        'form': form 
    })
#Guardaremos los datos de noticias en la Bdd
def guardarNoticia(request):
    
    titulo=request.POST["titulo"]
    imagenURL=request.POST["imagenURL"]
    descripcion=request.POST["descripcion"]
    referenciaURL=request.POST["referenciaURL"]

    nuevaNoticia=Noticia.objects.create(
        titulo=titulo,
        imagenURL=imagenURL,
        descripcion=descripcion,
        referenciaURL=referenciaURL)
    #mensaje de confirmacion
    messages.success(request,"Noticia guardada exitosamente")
    return redirect('iniciote')
def eliminarNoticia(request,id):
    noticiaEliminar=Noticia.objects.get(id=id)
    noticiaEliminar.delete()
    #mensaje de confirmacion
    messages.success(request,"Noticia eliminada exitosamente")
    return redirect('iniciote')

def editarNoticia(request,id):
    noticiaEditar=Noticia.objects.get(id=id)

    if request.method == 'POST':
        form = DescripcionForm(request.POST)
        if form.is_valid():
            noticiaEditar.descripcion = form.cleaned_data['descripcion']
            noticiaEditar.save()
            return redirect('iniciote')
    else:
        form = DescripcionForm(instance=noticiaEditar)

    return render(request,"Noticias/editarNoticias.html",{'noticiaEditar':noticiaEditar, 'form': form })

def procesarEdicionNoticia(request):
    id = request.POST['id']
    titulo=request.POST["titulo"]
    imagenURL=request.POST["imagenURL"]
    descripcion=request.POST["descripcion"]
    referenciaURL=request.POST["referenciaURL"]

    noticia=Noticia.objects.get(id=id)
    noticia.titulo=titulo
    noticia.imagenURL=imagenURL
    noticia.descripcion=descripcion
    noticia.referenciaURL=referenciaURL
    noticia.save()
    #mensaje de confirmacion
    messages.success(request,"Noticia actualizada exitosamente")
    return redirect('iniciote')















#######################desion contendio ###############

from django.shortcuts import render, redirect
from Aplicaciones.Mision.models import Mision
from Aplicaciones.Vision.models import Vision
from Aplicaciones.Historia.models import Historia
from Aplicaciones.Mision.forms import MisionForm
from Aplicaciones.Vision.forms import VisionForm
from Aplicaciones.Historia.forms import HistoriaForm
from Aplicaciones.Valores.models import Valores
from Aplicaciones.Valores.forms import ValoresForm



def general(request):
    return render(request, 'contenido/indexEdicion.html')

def generalMain(request):
    return render(request, 'contenido/inicioIndex.html')


def mision_view(request):
    mision = Mision.objects.get_or_create(id=1)[0]
    form = MisionForm(request.POST or None, instance=mision)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Se ha editado la misión correctamente.   ")
    return render(request, 'contenido/mision.html', {'form': form})


def vision_view(request):
    vision = Vision.objects.get_or_create(id=1)[0]
    form = VisionForm(request.POST or None, instance=vision)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Se ha editado la visión correctamente.")
    return render(request, 'contenido/vision.html', {'form': form})


def historia_view(request):
    historia = Historia.objects.get_or_create(id=1)[0]
    form = HistoriaForm(request.POST or None, instance=historia)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Se ha editado la historia correctamente.")
    return render(request, 'contenido/historia.html', {'form': form})


def valores_view(request):
    valores = Valores.objects.get_or_create(id=1)[0]
    form = ValoresForm(request.POST or None, instance=valores)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Se ha editado los valores correctamente.")
    return render(request, 'contenido/valores.html', {'form': form})








##################### VISTAS DE TESTIMONIOS #########################
from django.shortcuts import render, redirect
from Aplicaciones.Testimonios.models import Testimonio
from Aplicaciones.Testimonios.forms import DescripcionForm

def inicios(request):
    listadoTestimonios = Testimonio.objects.all()
    return render(request, "Testimonios/iniciotes.html", {'testimonio': listadoTestimonios})
def nuevoTestimonio(request):
    if request.method == 'POST':
        form = DescripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciotes')
    else:
        form = DescripcionForm()
    
    return render(request,"Testimonios/nuevoTestimonio.html", {
        'form': form 
    })

def guardarTestimonio(request):
    
    titulo=request.POST["titulo"]
    nombre=request.POST["nombre"]
    imagenURL=request.POST["imagenURL"]
    descripcion=request.POST["descripcion"]
    

    nuevaTestimonio=Testimonio.objects.create(
        titulo=titulo,
        nombre=nombre,
        imagenURL=imagenURL,
        descripcion=descripcion)
    #mensaje de confirmacion
    messages.success(request,"Testimonio guardado exitosamente")
    return redirect('iniciotes')
def eliminarTestimonio(request,id):
    testimonioEliminar=Testimonio.objects.get(id=id)
    testimonioEliminar.delete()
    #mensaje de confirmacion
    messages.success(request,"Testimonio eliminado exitosamente")
    return redirect('iniciotes')

def editarTestimonios(request,id):
    testimonioEditar=Testimonio.objects.get(id=id)

    if request.method == 'POST':
        form = DescripcionForm(request.POST)
        if form.is_valid():
            testimonioEditar.descripcion = form.cleaned_data['descripcion']
            testimonioEditar.save()
            return redirect('iniciotes')
    else:
        form = DescripcionForm(instance=testimonioEditar)

    return render(request,"Testimonios/editarTestimonios.html",{'testimonioEditar':testimonioEditar, 'form': form })
def procesarEdicionTestimonio(request):
    id = request.POST['id']
    titulo=request.POST["titulo"]
    nombre=request.POST["nombre"]
    imagenURL=request.POST["imagenURL"]
    descripcion=request.POST["descripcion"]

    testimonio=Testimonio.objects.get(id=id)
    testimonio.titulo=titulo
    testimonio.nombre=nombre
    testimonio.imagenURL=imagenURL
    testimonio.descripcion=descripcion
    testimonio.save()
    #mensaje de confirmacion
    messages.success(request,"Testimonio actualizado exitosamente")
    return redirect('iniciotes')