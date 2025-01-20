from django.core.management.base import BaseCommand
from foodie_goodie_app.models import Uzytkownik, ListaZakupow, Przepis, Skladnik, Jednostka, SkladnikPrzepisu
from datetime import date

class Command(BaseCommand):
    help = 'Seed list/recipe data for testing purposes...'

    def handle(self, *args, **kwargs):
        # user
        uzytkownik = Uzytkownik.objects.create(
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )

        # lists
        lista_1 = ListaZakupow.objects.create(
            nazwaListy="Tygodniowe zakupy",
            autor=uzytkownik
        )

        lista_2 = ListaZakupow.objects.create(
            nazwaListy="Urodziny Natalki",
            autor=uzytkownik
        )

        # units
        jednostka_g = Jednostka.objects.create(nazwaJednostki="g")
        jednostka_kg = Jednostka.objects.create(nazwaJednostki="kg")
        jednostka_szt = Jednostka.objects.create(nazwaJednostki="szt")
        jednostka_ml = Jednostka.objects.create(nazwaJednostki="ml")
        jednostka_l = Jednostka.objects.create(nazwaJednostki="l")
        
        



        # recipes with ingredients
        przepis_1 = Przepis.objects.create(
            autorPrzepisu=uzytkownik,
            nazwaPrzepisu="Ciasto",
            instrukcje=["Wymieszaj składniki", "Upiecz w piekarniku przez 30 minut"],
            dataPublikacji=date.today()
        )
        
        skladnik_11 = Skladnik.objects.create(
            nazwaSkladnika="Mąka",
            ilosc=1.0,
            jednostka=jednostka_kg
        )

        skladnik_12 = Skladnik.objects.create(
            nazwaSkladnika="Jajko",
            ilosc=2.0,
            jednostka=jednostka_szt
        )
        
        
        przepis_2 = Przepis.objects.create(
            autorPrzepisu=uzytkownik,
            nazwaPrzepisu="Omlet",
            instrukcje=["Rozbij jajka", "Usmaż na patelni"],
            dataPublikacji=date.today()
        )
        
        
        skladnik_21 = Skladnik.objects.create(
            nazwaSkladnika="Jajko",
            ilosc=4.0,
            jednostka=jednostka_szt
        )
        
        skladnik_22 = Skladnik.objects.create(
            nazwaSkladnika="Masło",
            ilosc=10,
            jednostka=jednostka_g
        )
        
        skladnik_23 = Skladnik.objects.create(
            nazwaSkladnika="Mleko",
            ilosc=100,
            jednostka=jednostka_ml
        )
        

        przepis_3 = Przepis.objects.create(
            autorPrzepisu=uzytkownik,
            nazwaPrzepisu="Zupa pomidorowa",
            instrukcje=["Gotuj pomidory", "Dodaj przyprawy", "Podawaj z makaronem"],
            dataPublikacji=date.today()
        )

        skladnik_31 = Skladnik.objects.create(
            nazwaSkladnika="Pomidory",
            ilosc=1.0,
            jednostka=jednostka_kg
        )
        
        skladnik_32 = Skladnik.objects.create(
            nazwaSkladnika="Makaron",
            ilosc=200,
            jednostka=jednostka_g
        )
        
        

        # 6. Przypisanie składników do przepisów
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik_11)
        SkladnikPrzepisu.objects.create(przepis=przepis_1, skladnik=skladnik_12)
        
        SkladnikPrzepisu.objects.create(przepis=przepis_2, skladnik=skladnik_21)
        SkladnikPrzepisu.objects.create(przepis=przepis_2, skladnik=skladnik_22)
        SkladnikPrzepisu.objects.create(przepis=przepis_2, skladnik=skladnik_23)
        5
        SkladnikPrzepisu.objects.create(przepis=przepis_3, skladnik=skladnik_31)
        SkladnikPrzepisu.objects.create(przepis=przepis_3, skladnik=skladnik_32)

        # 7. Wydrukowanie sukcesu
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with lists and recipes!'))
