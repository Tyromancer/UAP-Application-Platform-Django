from django import forms
from django.forms import ModelForm, CharField
from ckeditor.widgets import CKEditorWidget
from .models import URP, Application


class URPCreateForm(ModelForm):
    class Meta:
        model = URP
        fields = ['title', 'summary', 'description']
    
    description = CharField(widget=CKEditorWidget())


class ApplicationCreateForm(ModelForm):
    class Meta:
        model = Application
        fields = ['description']
    
    description = CharField()


class ApplicationManageForm(forms.Form):
    ACTIONS = (
        ('A', "Accept"),
        ('R', "Reject"),
    )

    action = forms.ChoiceField(widget=forms.Select, choices=ACTIONS)
