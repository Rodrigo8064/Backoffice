from django import forms
from . import models
from django_select2 import forms as s2forms


class ParentSearchWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__unaccent__icontains"]


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
        labels = {
            'name': 'Nome',
            'parent': 'Família'
        }
