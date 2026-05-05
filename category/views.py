from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import forms, models


class CategoryListView(LoginRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        parent = self.request.GET.get('parent')
        subparent = self.request.GET.get('subparent')
        if parent:
            try:
                parent_object = models.Category.objects.get(pk=parent)
                queryset = parent_object.get_descendants(include_self=True)

            except models.Category.DoesNotExist:
                queryset = queryset.none()

        if subparent:
            try:
                subparent_object = models.Category.objects.get(pk=subparent)
                queryset = subparent_object.get_descendants(include_self=True)
            except models.Category.DoesNotExist:
                queryset = queryset.none()

        if name:
            queryset = queryset.filter(
                Q(name__unaccent__icontains=name) | Q(url__icontains=name)
            )

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_filter = self.request.GET.get('parent', '')
        context['parent_options'] = models.Category.objects.filter(
            parent__isnull=True
        )

        if parent_filter:
            try:
                parent_object = models.Category.objects.get(pk=parent_filter)
                context['subparent_options'] = parent_object.get_children()
            except models.Category.DoesNotExist:
                context['subparent_options'] = models.Category.objects.none()
        else:
            context['subparent_options'] = models.Category.objects.none()

        context['total_count'] = models.Category.objects.count()
        context['name'] = self.request.GET.get('name', '')
        context['parent_filter'] = parent_filter
        context['subparent_filter'] = self.request.GET.get('subparent', '')

        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = models.Category
    template_name = 'category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    form_class = forms.CategoryUpdateForm
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')
