from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from .forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            messages.error(request, _('You do not have permission to edit this user'))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            messages.error(request, _('You do not have permission to delete this user'))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)
    
    # def form_valid(self, form):
    #     messages.success(self.request, self.success_message)
    #     return super().form_valid(form)

