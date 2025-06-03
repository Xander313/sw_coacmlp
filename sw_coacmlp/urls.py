from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),





    ##############################################
    ####### URLS PARA EDUCACION FINANCIERA #######
    ##############################################

    path('educacion/', include('Aplicaciones.Educacion.urls')),  
    path('auth/', include('social_django.urls', namespace='social')),




    ####################################################################
    ####### URLS PARA ADMINISTRAR MODULO DE EDUCACION FINANCIERA #######
    ####################################################################

    
    path('administrarEducacion/', include('Aplicaciones.AdministrarEducacion.urls')),  




    ##############################################
    ############## URLS PARA NOTICIAS#############
    ##############################################



<<<<<<< HEAD
=======


    #########################################################
    ############## URLS RUMBO A LA AUTENTICACION#############
    #########################################################

    path('autenticacion/', include('Aplicaciones.Autenticacion.urls')),  


>>>>>>> 5230f0fbe70ac4662625ddfa379a075f651d960b
    

]