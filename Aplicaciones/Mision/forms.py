from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Mision

class MisionForm(forms.ModelForm):
    class Meta:
        model = Mision
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(attrs={'class': 'ckeditor-custom'})
        }
