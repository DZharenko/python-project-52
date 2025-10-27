from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
        # УБИРАЕМ help_texts если они были
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }