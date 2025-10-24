from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class UsersView(View):
    def get(self, request, *args, **kwargs):
        # Здесь позже добавим логику для отображения пользователей
        return render(request, 'users.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Здесь позже добавим форму входа
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        # Здесь позже добавим форму регистрации
        return render(request, 'register.html')