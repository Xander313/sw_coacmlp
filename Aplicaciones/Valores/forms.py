from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Valores

class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(attrs={'class': 'ckeditor-custom'})
        }
