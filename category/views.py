from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category.html'
