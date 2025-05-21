from django import forms
from .models import Capitulo
from ckeditor.widgets import CKEditorWidget

class CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = '__all__'  
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuerpo'].widget = CKEditorWidget(config_name='default')
        self.fields['titulo'].widget.attrs.update({'placeholder': 'Ej: Introducción al curso'})
        self.fields['imagenURL'].widget.attrs.update({'placeholder': 'https://ejemplo.com/imagen.jpg'})