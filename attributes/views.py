from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from category.models import Family, Source

from .forms import AttributeForm, AttributeUpdateForm
from .models import Attribute


class AttributeListView(LoginRequiredMixin, ListView):
    model = Attribute
    template_name = 'attributes_list.html'
    context_object_name = 'attributes'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        family = self.request.GET.get('family')
        source = self.request.GET.get('source')
        search = self.request.GET.get('search')

        if family:
            queryset = queryset.filter(families__id=family)

        if source == 'all':
            all_source_ids = Source.objects.filter(is_active=True).values_list('id', flat=True)
            for source_id in all_source_ids:
                queryset = queryset.filter(sources__id=source_id)
        elif source:
            queryset = queryset.filter(sources__id=source)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['families'] = Family.objects.filter(is_active=True)
        context['sources'] = Source.objects.filter(is_active=True)
        context['search'] = self.request.GET.get('search', '')
        context['family'] = self.request.GET.get('family', '')
        context['source'] = self.request.GET.get('source', '')
        return context


class AttributeCreateView(LoginRequiredMixin, CreateView):
    model = Attribute
    template_name = 'attributes_create.html'
    form_class = AttributeForm
    success_url = reverse_lazy('attribute_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AttributeUpdateView(LoginRequiredMixin, UpdateView):
    model = Attribute
    template_name = 'attributes_update.html'
    form_class = AttributeUpdateForm
    success_url = reverse_lazy('attribute_list')


class AttributeDetailView(LoginRequiredMixin, DetailView):
    model = Attribute
    template_name = 'attributes_detail.html'
