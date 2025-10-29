from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].required = False
        self.fields['executor'].empty_label = _('Not assigned')
        self.fields['labels'].required = False