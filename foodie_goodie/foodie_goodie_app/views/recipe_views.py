from datetime import date
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Przepis,SkladnikPrzepisu,Uzytkownik,OcenyPrzepisu,KomentarzePrzepisu,Obserwowanie
from ..recalculatingAmount import recalculate
from ..forms.comment_form import KomentarzForm
logged_user=Uzytkownik.objects.filter(idUzytkownik=1).first()

def przepis_detail(request, id):
 
    przepis = get_object_or_404(Przepis, idPrzepis=id)
  
    skladniki_przepisu = SkladnikPrzepisu.objects.filter(przepis=przepis)
    skladniki=[item.skladnik for item in skladniki_przepisu]

    komentarze=KomentarzePrzepisu.objects.filter(przepis=przepis)
    ocena= OcenyPrzepisu.objects.filter(oceniajacy=logged_user,przepis=przepis).first()
    if ocena:
        ocena=ocena.wartosc
    else:
        ocena=0
    oceny = [elem.wartosc for elem in OcenyPrzepisu.objects.filter(przepis=przepis)]
    if oceny:  
        srednia = sum(oceny) / len(oceny)
        srednia = round(srednia, 2) 
    else:
        srednia = 0

    liczby = range(1, 21)  # Lista liczb od 1 do 20
    porcja=przepis.porcja
    error=""
    obserwowanie=Obserwowanie.objects.filter(przepis=przepis, uzytkownik=logged_user).first()
    if obserwowanie:
        obserwowanie=True
    else:
        obserwowanie=False
    form = KomentarzForm()
    if request.method == 'POST':
        porcja = int(request.POST.get('porcja_select'))
        try:
            recalculate(skladniki,przepis.wartosciodzywcze,przepis.porcja,porcja)
        except ValueError as e:
            error=f"Nie można przeliczyć przepisu na {porcja} osoby"
            porcja=przepis.porcja

    return render(request, 'recipedetails/recipe_detail.html', {
        'przepis': przepis,
        'skladniki_przepisu': skladniki,
        'komentarze':komentarze,
        'liczby':liczby,
        'porcja':porcja,
        'error':error,
        'ocena':ocena,
        'obserwowanie':obserwowanie,
        'form': form,
        'srednia':srednia,
        'logged_user':logged_user
    })

def przepis_detail_stars(request,id):
    body = json.loads(request.body)
    przepis = get_object_or_404(Przepis, idPrzepis=id)
    ocena = int(body.get('rating',0))
    #print(f"przepis_stars {przepis.nazwaPrzepisu}  {logged_user.nazwaUzytkownika}  {ocena}")
    if request.method == 'POST':
        
        ocena, created = OcenyPrzepisu.objects.update_or_create(
            przepis=przepis,
            oceniajacy=logged_user,
            defaults={"wartosc": ocena}
            )
 
        return JsonResponse({'message': 'Ocena została zapisana'}, status=200)
    return JsonResponse({'message': "Ten adres nie ma metody GET"}, status=400)   
    

def add_komentarz(request, id):
    przepis = get_object_or_404(Przepis, idPrzepis=id)
    
    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid():
            komentarz = form.save(commit=False)
            komentarz.przepis = przepis
            komentarz.uzytkownik = logged_user
            komentarz.dataKomentarza = date.today()
            komentarz.save()

    return redirect('recipe_detail', id=przepis.idPrzepis)
    
def obserwuj_przepis(request, id):
    przepis = Przepis.objects.get(idPrzepis=id)
    uzytkownik = logged_user

    # Sprawdź, czy użytkownik już obserwuje przepis
    obserwacja = Obserwowanie.objects.filter(przepis=przepis, uzytkownik=uzytkownik).first()

    if obserwacja:
        # Jeśli użytkownik już obserwuje, usuń obserwację (przestań obserwować)
        obserwacja.delete()
    else:
        # Jeśli użytkownik nie obserwuje, dodaj nową obserwację
        Obserwowanie.objects.create(przepis=przepis, uzytkownik=uzytkownik)

    # Przekierowanie z powrotem do strony przepisu
    return redirect('recipe_detail', id=przepis.idPrzepis)

def usun_komentarz(request, idrecipe, idcomment):
    przepis = get_object_or_404(Przepis, idPrzepis=idrecipe)
    komentarz = get_object_or_404(KomentarzePrzepisu, idKomentarz=idcomment, przepis=przepis)
    if komentarz.uzytkownik == logged_user:
        komentarz.delete()
    
    return redirect('recipe_detail', id=przepis.idPrzepis)