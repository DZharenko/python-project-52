from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

TASKS_URL = reverse_lazy('tasks:tasks')

class TaskListView(LoginRequiredMixin, FilterView):  
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter  
    ordering = ['created_at']

    def get_queryset(self):
        return Task.objects.select_related('author', 'executor', 'status')

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs['data'] is None:
            kwargs['data'] = {}
        return kwargs


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
    success_url = TASKS_URL
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = TASKS_URL
    success_message = _('Task successfully updated')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = TASKS_URL
    success_message = _('Task successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.author:
            messages.error(
                request,
                _('A task can only be deleted by its author')
            )
            return redirect(TASKS_URL)
        return super().dispatch(request, *args, **kwargs)

