from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps


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