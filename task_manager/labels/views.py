from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label

LABELS_URL = reverse_lazy('labels_index')

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['created_at']


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = LABELS_URL
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = LABELS_URL
    success_message = _('Label successfully updated')


# class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Label
#     template_name = 'labels/delete.html'
#     success_url = LABELS_URL
#     success_message = _('Label successfully deleted')

#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except models.ProtectedError:
#             messages.error(
#                 self.request,
#                 _('Cannot delete label because it is in use')
#             )
#             return redirect(LABELS_URL)

class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = LABELS_URL
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
                
        if self.object.tasks.exists():
            messages.error(
                request,
                _('Cannot delete label because it is in use')
            )
            return redirect(self.success_url)
        
        return super().post(request, *args, **kwargs)