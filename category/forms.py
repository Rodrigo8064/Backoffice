from django import forms
from . import models
from django_select2 import forms as s2forms


class ParentSearchWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__unaccent__icontains"]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'parent', 'url']
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
            'url': 'ID'
        }
