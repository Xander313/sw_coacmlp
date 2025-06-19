from django.shortcuts import render
from Aplicaciones.Mision.models import Mision


# Create your views here.
def index(request):
    return render(request, 'Contenido/index.html')

def aboutUs(request):
    return render(request, 'Contenido/contentido.html')


def contenido_view(request):
    mision = Mision.objects.first()
    return render(request, 'contenido.html', {'mision': mision})