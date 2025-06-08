from django.urls import path
from . import views

urlpatterns = [
    path('iniciarSesion/', views.redireccionador, name='redireccionador'),
    path('perfilContenido/', views.perfilContenido, name='perfilContenido'),
    path('iniciote/',views.inicio, name='iniciote'),
    path('nuevaNoticia/',views.nuevaNoticia, name='nuevaNoticia'),
    path('guardarNoticia/',views.guardarNoticia,name='guardarNoticia'),

]