from django import forms
from django.forms import CheckboxSelectMultiple

from category.models import Family, Source

from .models import Attribute


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'expected_value', 'sources', 'families']
        widgets = {
            'sources': CheckboxSelectMultiple(),
            'families': CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Nome do atributo',
            'expected_value': 'Valor esperado',
            'sources': 'Fonte(s)',
            'families': 'Família(s)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sources'].queryset = Source.objects.filter(is_active=True)
        self.fields['families'].queryset = Family.objects.filter(
            is_active=True
        )


class AttributeUpdateForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'expected_value', 'sources', 'families', 'is_active']
        widgets = {
            'sources': CheckboxSelectMultiple(),
            'families': CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Nome do atributo',
            'expected_value': 'Valor esperado',
            'sources': 'Fonte(s)',
            'families': 'Família(s)',
            'is_active': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sources'].queryset = Source.objects.filter(is_active=True)
        self.fields['families'].queryset = Family.objects.filter(
            is_active=True
        )
