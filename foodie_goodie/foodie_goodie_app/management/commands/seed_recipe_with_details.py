from django.core.management.base import BaseCommand
from foodie_goodie_app.models import OcenyPrzepisu, Uzytkownik, ListaZakupow, Przepis, Skladnik, Jednostka, SkladnikPrzepisu, KomentarzePrzepisu,Obserwowanie
from datetime import date

class Command(BaseCommand):
    help = 'Recipe with details to show'

    def handle(self, *args, **kwargs):
        
        uzytkownik = Uzytkownik.objects.create(
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )

        uzytkownik2 = Uzytkownik.objects.create(
            nazwaUzytkownika="Ania Gotuje",
            email="aniagotuje@example.com",
            haslo="12345678"
        )

        jednostka_g = Jednostka.objects.create(nazwaJednostki="g",minimalnaWartosc=1)
        jednostka_szt = Jednostka.objects.create(nazwaJednostki="szt",minimalnaWartosc=1)
        jednostka_ml = Jednostka.objects.create(nazwaJednostki="ml",minimalnaWartosc=1)
       
        
        
        przepis_1 = Przepis.objects.create(
            autorPrzepisu=uzytkownik2,
            nazwaPrzepisu="Ciasto czekoladowe",
            instrukcje=["Jajka ogrzać np. w misce z ciepłą wodą. Dno małej tortownicy o średnicy 21 cm wyłożyć papierem do pieczenia, zapiąć obręcz. Piekarnik nagrzać do 175 stopni C.",
                        "W rondelku umieścić pokrojone masło oraz połamaną na kosteczki czekoladę, podgrzewać na minimalnym ogniu ciągle mieszając aż składniki się roztopią i otrzymamy gładką masę czekoladową. Odstawić z ognia, dodać mleko i wymieszać.",
                        "W misce ubić jajka z cukrem (ok. 4 minuty) na puszystą masę.",
                        "Do drugiej miski przesiać mąkę, dodać proszek do pieczenia i dokładnie wymieszać.",
                        "Do mąki dodać ubite jajka oraz masę czekoladową i zmiksować na minimalnych obrotach miksera lub wymieszać rózgą tylko do połączenia się składników w jednolite ciasto.",
                        "Przelać je do tortownicy, wstawić do piekarnika i piec przez ok. 43 minuty do suchego patyczka.",
                        "Polać polewą: do garnka włożyć połamaną na kosteczki czekoladę i pokrojone masło, cały czas mieszając podgrzewać na małym ogniu aż czekolada się roztopi (lub rozpuścić w mikrofali)."],
            wartosciodzywcze = {"Kalorie[kcal]":1400,
                                "Tłuszcze[g]":72,
                                "Wędlowodany[g]":180,
                                "Błonnik[g]":10,
                                "Białko[g]":20,
                                "Sód[mg]":800,
                                "Wapń[mg]":160,
                                "Zelazo[mg]":2},
            dataPublikacji=date.today(),
            czasprzygotowania=60,
            porcja=4
        )
        
        skladnik1 = Skladnik.objects.create(
            nazwaSkladnika="Masło",
            ilosc=80,
            jednostka=jednostka_g
        )

        skladnik2 = Skladnik.objects.create(
            nazwaSkladnika="Czekolada gorzka",
            ilosc=100,
            jednostka=jednostka_g
        )

        skladnik3 = Skladnik.objects.create(
            nazwaSkladnika="Mleko",
            ilosc=125,
            jednostka=jednostka_ml
        )
        
        skladnik4 = Skladnik.objects.create(
            nazwaSkladnika="Jajka",
            ilosc=2,
            jednostka=jednostka_szt
        )

        skladnik5 = Skladnik.objects.create(
            nazwaSkladnika="Cukier",
            ilosc=150,
            jednostka=jednostka_g
        )

        skladnik6 = Skladnik.objects.create(
            nazwaSkladnika="Mąka",
            ilosc=150,
            jednostka=jednostka_g
        )

        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik1)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik2)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik3)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik4)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik5)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik6)
        
        OcenyPrzepisu.objects.create(przepis=przepis_1, oceniajacy=uzytkownik2, wartosc=5)
        KomentarzePrzepisu.objects.create(  przepis = przepis_1, 
                                          komentarz = None,
                                          uzytkownik = uzytkownik2, 
                                          dataKomentarza = date.today(),
                                          trescKomentarza = "Jeden z moich najlepszych przepisów")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database with recipe {przepis_1.idPrzepis}'))
