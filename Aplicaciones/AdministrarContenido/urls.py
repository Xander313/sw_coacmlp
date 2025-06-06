from django.urls import path
from . import views

urlpatterns = [
    path('iniciarSesion/', views.redireccionador, name='redireccionador'),
    path('perfilContenido/', views.perfilContenido, name='perfilContenido'),
]