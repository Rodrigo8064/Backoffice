from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import forms, models


class ProductListView(LoginRequiredMixin, ListView):
    model = models.ProductType
    template_name = 'product_list.html'
    context_object_name = 'products_type'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        parent = self.request.GET.get('parent')
        subparent = self.request.GET.get('subparent')

        if parent:
            try:
                parent_object = models.ProductType.objects.get(pk=parent)
                queryset = parent_object.get_descendants(include_self=True)
            except models.ProductType.DoesNotExist:
                queryset = queryset.none()
        
        if subparent:
            try:
                subparent_object = models.ProductType.objects.get(pk=subparent)
                queryset = subparent_object.get_descendants(include_self=True)
            except models.ProductType.DoesNotExist:
                queryset = queryset.none()
        if name:
            queryset = queryset.filter(name__unaccent__icontains=name)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parent_filter = self.request.GET.get('parent', '')
        context['parent_options'] = models.ProductType.objects.filter(
            parent__isnull=True
        )

        if parent_filter:
            try:
                parent_object = models.ProductType.objects.get(pk=parent_filter)
                context['subparent_options'] = parent_object.get_children()
            except models.ProductType.DoesNotExist:
                context['subparent_options'] = models.ProductType.objects.none()
        else:
            context['subparent_options'] = models.ProductType.objects.none()

        context['total_count'] = models.ProductType.objects.count()
        context['name'] = self.request.GET.get('name', '')
        context['parent_filter'] = parent_filter
        context['subparent_filter'] = self.request.GET.get('subparent', '')

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.ProductType
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProductType
    template_name = 'product_update.html'
    form_class = forms.ProductUpdateForm
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProductType
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
