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
    return render(request,"Noticias/editarNoticias.html",{'noticiaEditar':noticiaEditar})

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

from Aplicaciones.Mision.models import Mision

def general(request):
    mision, creado = Mision.objects.get_or_create(id=1)
    
    # Si el contenido está vacío, asignar el valor por defecto
    if not mision.descripcion:
        mision.descripcion = Mision._meta.get_field('descripcion').default
        mision.save()

    return render(request, 'AdministrarContenido/templates/contenido/index.html', {
        'mision': mision
    })


def general(request):
    mision = Mision.objects.first()  # Trae la primera misión, o ajusta según tu modelo
    vision = None  # Lo mismo para visión, historia y valores si tienes
    historia = None
    valores = None

    return render(request, 'contenido/index.html', {
        'mision': mision,
        'vision': vision,
        'historia': historia,
        'valores': valores,
    })