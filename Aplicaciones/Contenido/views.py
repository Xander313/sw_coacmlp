from django.shortcuts import render
from Aplicaciones.Mision.models import Mision
from Aplicaciones.Noticias.models import Noticia


# Create your views here.
def index(request):
    return render(request, 'Contenido/index.html')

def aboutUs(request):
    return render(request, 'Contenido/contentido.html')


def contenido_view(request):
    mision = Mision.objects.first()
    return render(request, 'Contenido/contenido.html', {'mision': mision})




def newsLetter(request):
    noticias = Noticia.objects.all()
    return render(request, 'Contenido/noticias.html', {'noticias': noticias})