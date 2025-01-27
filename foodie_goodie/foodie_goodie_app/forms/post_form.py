from django import forms
from django.core.exceptions import ValidationError
from ..models import Post, Forum

class PostForm(forms.ModelForm):

    trescPost = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Wpisz odpowiedź...', 'rows': 5}),
        required=True,
        min_length=8,
    )

    obrazek = forms.ImageField(required=False)


    class Meta:
        model = Post
        fields = ['trescPost', 'obrazek']


    def clean_obrazek(self):
        print("clean obrazek")
        obrazek = self.cleaned_data.get('obrazek')
        if obrazek:
            if not obrazek.name.endswith(('jpg', 'jpeg', 'png', 'gif')):
                raise ValidationError('Dozwolone są tylko pliki JPG, JPEG lub PNG.')
        return obrazek

    def clean_trescPost(self):
        print("clean trescpost")
        tresc = self.cleaned_data.get('trescPost')
        if not tresc.strip():
            raise ValidationError('Treść nie może być pusta.')
        return tresc
    

class ThreadForm(forms.ModelForm):

    tytulForum = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Tytuł wątku'}),
        required=True
    )

    trescPost = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Wpisz odpowiedź...', 'rows': 5}),
        required=True,
        min_length=10,
        strip=True
    )

    obrazek = forms.ImageField(required=False)

    class Meta:
        model = Forum
        fields = ['tytulForum', 'trescPost', 'obrazek']

    def clean_tytulForum(self):
        tytul = self.cleaned_data.get('tytulForum')
        if len(tytul) < 5:
            raise ValidationError('Tytuł powinien mieć co najmniej 5 znaków.')
        return tytul


