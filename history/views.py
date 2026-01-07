from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from.models import History


class HistoryListView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'history.html'
