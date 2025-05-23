from django import forms
from .models import Capitulo
from ckeditor.widgets import CKEditorWidget

class CuerpoForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['cuerpo']
        widgets = {
            'cuerpo': CKEditorWidget(config_name='default')
        }
