from django import forms
from django.forms import ModelForm, CharField
from ckeditor.widgets import CKEditorWidget
from .models import URP, Application


class URPCreateForm(ModelForm):
    """Form for URP creation"""
    class Meta:
        model = URP
        fields = ['title', 'summary', 'description']
    
    description = CharField(widget=CKEditorWidget())


class ApplicationCreateForm(ModelForm):
    """Form for Application creation"""
    class Meta:
        model = Application
        fields = ['description']
    
    description = CharField()


class ApplicationManageForm(forms.Form):
    """Form for updating application status: Accept or Reject"""
    ACTIONS = (
        ('A', "Accept"),
        ('R', "Reject"),
    )

    action = forms.ChoiceField(widget=forms.Select, choices=ACTIONS)
