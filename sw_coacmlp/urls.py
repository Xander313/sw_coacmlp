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





    #########################################################
    ############## URLS RUMBO A LA AUTENTICACION#############
    #########################################################

    path('autenticacion/', include('Aplicaciones.Autenticacion.urls')),  


    

]