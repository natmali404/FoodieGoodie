from django import forms
from .models import Wpis

from django import forms
from .models import Wpis, Jadlospis, JadlospisPrzepis, Przepis

class WpisForm(forms.ModelForm):
    class Meta:
        model = Wpis
        fields = ['tresc', 'zdjecie']  # Pola widoczne w formularzu

class WpisCreateForm(forms.ModelForm):
    class Meta:
        model = Wpis
        fields = ['tresc', 'zdjecie']  # Include the content and image fields for creating a new post

class WpisUpdateForm(forms.ModelForm):
    class Meta:
        model = Wpis
        fields = ['tresc', 'zdjecie']  


class JadlospisForm(forms.ModelForm):
    class Meta:
        model = Jadlospis
        fields = ["nazwa"]  # Tylko pole nazwa będzie widoczne w formularzu




class JadlospisPrzepisForm(forms.Form):
    przepis = forms.ModelChoiceField(queryset=Przepis.objects.all(), label="Wybierz przepis")
    dzienTygodnia = forms.ChoiceField(choices=JadlospisPrzepis.DZIEŃ_TYGODNIA_CHOICES, label="Dzien tygodnia")
    godzina = forms.ChoiceField(choices=JadlospisPrzepis.PORA_DNIA_CHOICES, label="Pora dnia")

    class Meta:
        model = JadlospisPrzepis
        fields = ["jadlospis", "przepis", "dzienTygodnia", "godzina"]
