from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Historia

class HistoriaForm(forms.ModelForm):
    class Meta:
        model = Historia
        fields = ['descripcion']
        widgets = {
            'descripcion': CKEditorWidget(attrs={'class': 'ckeditor-custom'})
        }
