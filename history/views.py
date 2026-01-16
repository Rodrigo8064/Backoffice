from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import History
from .forms import HistoryForm


class HistoryListView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'history_list.html'
    context_object_name = 'history'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        entity = self.request.GET.get('entity')

        if entity:
            queryset = queryset.filter(entity__icontains=entity)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = self.request.GET.get('entity', '')
        return context

class HistoryCreateView(LoginRequiredMixin, CreateView):
    model = History
    template_name = 'history_create.html'
    form_class = HistoryForm
    success_url = reverse_lazy('history_list')


class HistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = History
    template_name = 'history_update.html'
    form_class = HistoryForm
    success_url = reverse_lazy('history_list')


class HistoryDeleteView(LoginRequiredMixin, DeleteView):
    model = History
    template_name = 'history_delete.html'
    success_url = reverse_lazy('history_list')
