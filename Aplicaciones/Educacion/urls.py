from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [

    path('logout/', views.salir, name='logout'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('errorSesion/', views.salirDefinitivo, name='errorSesion'),
    path('volverInicio/', views.volverInicio, name='volverInicio'),
    path('login/', lambda request: redirect('errorSesion'), name='login'),
    path('perfil/', views.perfilVisitante, name='perfilVisitante'),

    #####################################################################
    ###################SIRVIENDO CAPITULOS####################
    #####################################################################
    
    path('capitulo/<int:id>/', views.capitulo, name='capitulo'),
    path('examen/<int:id>/', views.examen, name='examen_capitulo'),

    #####################################################################
    ###################SIRVIENDO CAPITULOS y certificacion####################
    #####################################################################

    path('capitulo/avanzar/<int:id>/', views.avanzarCapitulo, name='avanzarCapitulo'),
    path('capitulo/<int:capitulo_id>/evaluar/', views.evaluarExamen, name='evaluarExamen'),
    path('certificado/', views.certificado, name='certificadoEducacion'),
    path('ejecutarCertificacion/', views.ejecutarCertificacion, name='ejecutarCertificacion'),

    

]

