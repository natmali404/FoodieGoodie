from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from ..models import Przepis,SkladnikPrzepisu
# def home(request):
#     return HttpResponse("<h1>Witaj w aplikacji FoodieGoodie!</h1><p>To jest strona powitalna.</p>")

def home(request):
    return render(request, "home.html")

def przepis_detail(request, id):
    # Pobierz przepis na podstawie ID
    przepis = get_object_or_404(Przepis, idPrzepis=id)
    # Pobierz składniki przypisane do przepisu
    skladniki_przepisu = SkladnikPrzepisu.objects.filter(przepis=przepis)
    
    return render(request, 'recipedetails/recipe_detail.html', {
        'przepis': przepis,
        'skladniki_przepisu': skladniki_przepisu
    })