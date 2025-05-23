from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.index, name='perfil'),
    path('administracion/', views.administracion, name='administracion'),
    path('crearCapitulo/', views.crearCapitulo, name='crearCapitulo'),
    path('crearNuevoCapitulo/', views.crearNuevoCapitulo, name='crearNuevoCapitulo'),



]
