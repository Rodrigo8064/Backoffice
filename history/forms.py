from django import forms
from . import models


class HistoryForm(forms.ModelForm):

    class Meta:
        model = models.History
        fields = '__all__'
        labels = {
            'entity': 'Entidade',
            'record': 'Ficha',
            'new_tax': 'Nova Taxonomia'
        }
