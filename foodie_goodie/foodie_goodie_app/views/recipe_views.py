import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from ..models import Przepis,SkladnikPrzepisu,Uzytkownik,OcenyPrzepisu,KomentarzePrzepisu
from ..recalculatingAmount import recalculate

logged_user=Uzytkownik.objects.filter(idUzytkownik=1).first()

def przepis_detail(request, id):
    #print("przepis_detils")

    # Pobierz przepis na podstawie ID
    przepis = get_object_or_404(Przepis, idPrzepis=id)
    # Pobierz składniki przypisane do przepisu
    skladniki_przepisu = SkladnikPrzepisu.objects.filter(przepis=przepis)
    skladniki=[item.skladnik for item in skladniki_przepisu]
    komentarza=KomentarzePrzepisu.objects.filter(przepis=przepis)
    ocena= OcenyPrzepisu.objects.filter(oceniajacy=logged_user).first() 
    if ocena:
        ocena=ocena.wartosc
    else:
        ocena=0
    liczby = range(1, 21)  # Lista liczb od 1 do 20
    porcja=przepis.porcja
    error=""
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
        'liczby':liczby,
        'porcja':porcja,
        'error':error,
        'ocena':ocena
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
    


    
    