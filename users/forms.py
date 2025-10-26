from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username'),
            'email': _('Email'),
        }

class UserUpdateForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username'),
            'email': _('Email'),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )