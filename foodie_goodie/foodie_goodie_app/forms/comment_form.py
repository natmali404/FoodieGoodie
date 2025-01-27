from django import forms
from ..models import KomentarzePrzepisu

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = KomentarzePrzepisu
        fields = ['trescKomentarza']  # Tylko pole dla treści komentarza
        widgets = {
            'trescKomentarza': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napisz komentarz...'}),
        }
