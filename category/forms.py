from django import forms
from django_select2 import forms as s2forms

from . import models


class ParentSearchWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__unaccent__icontains']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', 'parent', 'url', 'notes']
        widgets = {
            'parent': ParentSearchWidget(
                attrs={
                    'data-width': '100%',
                    'class': 'form-control',
                }
            ),
        }
        labels = {
            'name': 'Nome',
            'parent': 'Família',
            'url': 'ID',
            'notes': 'status'
        }


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', 'parent', 'url', 'is_active', 'notes']
        widgets = {
            'parent': ParentSearchWidget(
                attrs={
                    'data-width': '100%',
                    'class': 'form-control',
                }
            ),
        }
        labels = {
            'name': 'Nome',
            'parent': 'Família',
            'url': 'ID',
            'is_active': 'Ativo',
            'notes': 'status'
        }
