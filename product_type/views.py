from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models, forms


class ProductListView(LoginRequiredMixin, ListView):
    model = models.ProductType
    template_name = 'product_list.html'
    context_object_name = 'products_type'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        parent = self.request.GET.get('parent')
        if parent:
            try:
                parent_object = models.ProductType.objects.get(pk=parent)
                queryset = parent_object.get_descendants(include_self=True)
                
            except models.ProductType.DoesNotExist:
                queryset = queryset.none()
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_options'] = models.ProductType.objects.filter(parent__isnull=True)
        context['total_count'] = models.ProductType.objects.count()
        context['name'] = self.request.GET.get('name', '')
        context['parent_filter'] = self.request.GET.get('parent', '')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.ProductType
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProductType
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProductType
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
