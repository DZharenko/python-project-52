from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, _('You are logged in'))
            return redirect('index')
        else:
            messages.error(request, _('Please enter a correct username and password.'))
            return render(request, 'login.html')


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('index')


# class RegisterView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'register.html')


def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            # ИСПРАВИЛ: используем правильную константу для Django 5.x
            request.session['django_language'] = language
            messages.success(request, _('Language changed successfully'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))