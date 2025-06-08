from django import forms
from .models import Noticia
from ckeditor.widgets import CKEditorWidget

class DescripcionForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(config_name='default')
        }
