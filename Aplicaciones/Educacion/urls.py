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

    #####################################################################
    ###################SIRVIENDO CAPITULOS####################
    #####################################################################
    path('capitulo/<int:id>', views.capitulo, name='capitulo'),

]

