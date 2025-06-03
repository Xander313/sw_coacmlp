from django.shortcuts import render
from .models import Contenido

# Create your views here.
def index(request):
    return render(request, 'Contenido/index.html')