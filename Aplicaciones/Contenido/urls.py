from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('acerca-de-nosotros', views.aboutUs, name="aboutUs"),
    
]