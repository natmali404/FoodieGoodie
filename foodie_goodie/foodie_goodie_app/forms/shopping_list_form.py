from django import forms
from ..models import ListaZakupow

class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ListaZakupow
        fields = [
            'nazwaListy',
            ]
