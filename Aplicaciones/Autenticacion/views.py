from django.shortcuts import render
import hashlib
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages



# Create your views here.
def loginAdministracion(request):
    return render(request, 'Autenticacion/autenticacion.html')

def ejecutarInicioSesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        
        if usuario == settings.USER_CONTENIDO and password_hash == settings.PASSWORD_CONTENIDO:
            request.session['admin_token'] = 'contenido'
            messages.success(request, 'Sesión iniciada como administrador de Contenido.')
            return redirect('contenido:index')

        elif usuario == settings.USER_EDUCACION and password_hash == settings.PASSWORD_EDUCACION:
            request.session['admin_token'] = 'educacion'
            return redirect('perfil') 

        else:
            messages.error(request, 'Algo salió mal, verifique sus credenciales')
            return redirect('loginAdministracion')  
        
    messages.success(request, 'Algo salió mal, no sabesmos que ocurrió')
    return render(request, 'Autenticacion/autenticacion.html')