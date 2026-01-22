from django.views.generic import ListView
from . import models, clients
from django.contrib.auth.mixins import LoginRequiredMixin


class SkuListView(LoginRequiredMixin, ListView):
    model = models.DataClient
    template_name = 'sku_data.html'
    context_object_name = 'data_type'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        navigation = self.request.GET.get('navigation')

        if navigation:
            try:
                client = clients.DataService()
                context['api_result'] = client.get_sku_data(navigation)
            except Exception as e:
                context['error'] = f"Erro ao buscar dados: {e}"

        return context
