from django import forms
from django_select2 import forms as s2forms

from . import models


class ParentSearchWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__unaccent__icontains']

    def get_queryset(self):
        return models.ProductType.objects.all().order_by('name')

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.ProductType
        fields = ['name', 'parent']
        widgets = {
            'parent': ParentSearchWidget(
                attrs={
                    'data-width': '100%',
                    'class': 'form-control',
                }
            ),
        }
        labels = {'name': 'Nome', 'parent': 'Família'}


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ProductType
        fields = ['name', 'is_active', 'parent']
        widgets = {
            'parent': ParentSearchWidget(
                attrs={
                    'data-width': '100%',
                    'class': 'form-control',
                }
            ),
        }
        labels = {'name': 'Nome', 'parent': 'Família', 'is_active': 'Ativo'}
