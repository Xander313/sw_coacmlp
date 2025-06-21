from django.urls import path
from . import views

urlpatterns = [

    #######################nmoticias##########################
    path('iniciarSesion/', views.redireccionador, name='redireccionador'),
    path('perfilContenido/', views.perfilContenido, name='perfilContenido'),
    path('iniciote/',views.inicio, name='iniciote'),
    path('nuevaNoticia/',views.nuevaNoticia, name='nuevaNoticia'),
    path('guardarNoticia/',views.guardarNoticia,name='guardarNoticia'),
    path('eliminarNoticia/<int:id>',views.eliminarNoticia,name='eliminarNoticia'),
    path('editarNoticia/<int:id>',views.editarNoticia,name='editarNoticia'),
    path('procesarEdicionNoticia/',views.procesarEdicionNoticia,name='procesarEdicionNoticia'),


    #######################mContenido##########################
    path('general/', views.general, name='generalParaMOdificar'),
    path('main/', views.generalMain, name='generamain'),


    path('mision/', views.mision_view, name='misionAd'),
    path('vision/', views.vision_view, name='visionAd'),
    path('historia/', views.historia_view, name='historiaAd'),
    path('valores/', views.valores_view, name='valoresAd'),
    



]