from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Vision

class VisionForm(forms.ModelForm):
    class Meta:
        model = Vision
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(attrs={'class': 'ckeditor-custom'})
        }
