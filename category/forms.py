from django import forms
from . import models
from django_select2 import forms as s2forms


class ParentSearchWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'url', 'parent']
        widgets = {
            'parent': ParentSearchWidget(
                attrs={'data-minimum-input-length': 0} # Começa a buscar ao clicar
            ),
        }
        labels = {
            'name': 'Nome',
            'url': 'ID',
            'parent': 'Categoria',
        }
