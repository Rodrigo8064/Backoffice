from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models, forms


class CategoryListView(LoginRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        parent = self.request.GET.get('parent')
        if parent:
            try:
                parent_object = models.Category.objects.get(pk=parent)
                queryset = parent_object.get_descendants(include_self=True)

            except models.Category.DoesNotExist:
                queryset = queryset.none()
        if name:
            queryset = queryset.filter(name__unaccent__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_options'] = models.Category.objects.filter(parent__isnull=True)
        context['total_count'] = models.Category.objects.count()
        context['name'] = self.request.GET.get('name', '')
        context['parent_filter'] = self.request.GET.get('parent', '')
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = models.Category
    template_name = 'category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')
