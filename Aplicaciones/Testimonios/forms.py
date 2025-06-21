from django import forms
from .models import Testimonio
from ckeditor.widgets import CKEditorWidget

class DescripcionForm(forms.ModelForm):
    class Meta:
        model = Testimonio
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(config_name='default')
        }
