from django.urls import path
from . import views

urlpatterns = [

    path('logout/', views.salir, name='logout'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('errorSesion/', views.salirDefinitivo, name='errorSesion'),
    path('volver-inicio/', views.volver_inicio, name='volver_inicio'),

]