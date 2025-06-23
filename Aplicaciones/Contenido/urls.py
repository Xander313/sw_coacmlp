from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('acerca-de-nosotros', views.contenido_view, name="aboutUs"),
    path('noticias', views.newsLetter, name="newsLetter"),
    path('testimonios', views.testi, name="testi"),
    path('contenido', views.contenido_view, name='contenido'),


    
]