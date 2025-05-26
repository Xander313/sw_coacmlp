from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.index, name='perfil'),
    path('administracion/', views.administracion, name='administracion'),
    path('crearCapitulo/', views.crearCapitulo, name='crearCapitulo'),
    path('crearNuevoCapitulo/', views.crearNuevoCapitulo, name='crearNuevoCapitulo'),
    path('edicion/<int:id>', views.servirEdicion, name='edicion'),
    path('ejecutarEdicionCapitulo/<int:capitulo_id>', views.ejecutarEdicionapitulo, name='ejecutarEdicionCapitulo'),
    path('ejecutareliminacionCapitulo/<int:id>', views.ejecutareliminacionCapitulo, name='ejecutareliminacionCapitulo'),





]
