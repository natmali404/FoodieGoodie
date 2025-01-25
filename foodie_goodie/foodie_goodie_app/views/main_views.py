from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# def home(request):
#     return HttpResponse("<h1>Witaj w aplikacji FoodieGoodie!</h1><p>To jest strona powitalna.</p>")

def home(request):
    return render(request, "home.html")
