from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    ordering = ['created_at']

    def get_queryset(self):
        return Task.objects.select_related('author', 'executor', 'status')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.select_related('author', 'executor', 'status')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully updated')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.author:
            messages.error(
                request,
                _('A task can only be deleted by its author')
            )
            return redirect('tasks:tasks')
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     messages.success(self.request, self.success_message)
    #     return super().form_valid(form)