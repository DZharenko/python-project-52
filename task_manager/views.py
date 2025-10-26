from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


# class UsersView(View):
#     def get(self, request, *args, **kwargs):
#         # Здесь позже добавим логику для отображения пользователей
#         return render(request, 'users.html')


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
            return redirect('home')
        else:
            messages.error(request, _('Please enter a correct username and password.'))
            return render(request, 'login.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('home')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        # Здесь позже добавим форму регистрации
        return render(request, 'register.html')
    

