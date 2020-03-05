from django.forms import ModelForm, CharField
from ckeditor.widgets import CKEditorWidget
from .models import URP


class URPCreateForm(ModelForm):
    class Meta:
        model = URP
        fields = ['title', 'summary', 'description']
    
    description = CharField(widget=CKEditorWidget())