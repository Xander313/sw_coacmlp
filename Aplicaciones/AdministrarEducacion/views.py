from django.shortcuts import render,redirect
from Aplicaciones.Capitulo.models import Capitulo
from Aplicaciones.Capitulo.forms import CapituloForm 



def index(request):
    return render(request, 'AdministrarEducacion/sesionIniciada.html')

def administracion(request):
    capitulos = Capitulo.objects.all()
    return render(request, 'AdministrarEducacion/modulos.html', {'capitulos': capitulos})




def crearCapitulo(request):
    if request.method == 'POST':
        form = CapituloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nombre_url_lista_capitulos')  # Redirige tras guardar
    else:
        form = CapituloForm()
    
    return render(request, 'AdministrarEducacion/nuevoCapitulo.html', {
        'form': form,
        'titulo_pagina': 'Crear Capítulo'  # Contexto adicional
    })