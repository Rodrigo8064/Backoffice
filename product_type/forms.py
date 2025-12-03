from django import forms
from . import models
from mptt.forms import TreeNodeChoiceField

class ProductForm(forms.ModelForm):

    parent = TreeNodeChoiceField(
        label="Categoria Pai",
        queryset=models.ProductType.objects.all(),
        required=False,
        level_indicator='---'
    )

    class Meta:
        model = models.ProductType
        fields = ['nome', 'parent']
        labels = {
            'nome': 'Nome',
            'parent': 'Categoria'
        }
