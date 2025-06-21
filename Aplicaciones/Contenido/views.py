from django.shortcuts import render
from Aplicaciones.Mision.models import Mision
from Aplicaciones.Noticias.models import Noticia
from Aplicaciones.Vision.models import Vision
from Aplicaciones.Historia.models import Historia
from Aplicaciones.Valores.models import Valores
from Aplicaciones.Testimonios.models import Testimonio


# Create your views here.
def index(request):
    return render(request, 'Contenido/index.html')

def aboutUs(request):
    return render(request, 'Contenido/contentido.html')

def contenido_view(request):
    mision = Mision.objects.first()
    vision = Vision.objects.first()
    historia = Historia.objects.first()
    valores = Valores.objects.first()

    return render(request, 'Contenido/contentido.html', {
        'mision': mision,
        'vision': vision,
        'historia': historia,
        'valores': valores,
    })




def newsLetter(request):
    noticias = Noticia.objects.all()
    return render(request, 'Contenido/noticias.html', {'noticias': noticias})

########################TARJETA PARA TESTIMONIOS####################
def testi(request):
    testimonios = Testimonio.objects.all()
    return render(request, 'Contenido/testimonios.html', {'testimonios': testimonios})