from django.core.management.base import BaseCommand
from foodie_goodie_app.models import Uzytkownik, ListaZakupow, Przepis, Skladnik, Jednostka, ElementListy
from datetime import date

class Command(BaseCommand):
    help = 'Seed database for testing purposes...'

    def handle(self, *args, **kwargs):
        # user
        print("Seeding users...")
        uzytkownik = Uzytkownik.objects.create(
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        
        
        
        # units
        print("Seeding units...")
        jednostka_g = Jednostka.objects.create(nazwaJednostki="g")
        jednostka_kg = Jednostka.objects.create(nazwaJednostki="kg")
        jednostka_szt = Jednostka.objects.create(nazwaJednostki="szt")
        jednostka_ml = Jednostka.objects.create(nazwaJednostki="ml")
        jednostka_l = Jednostka.objects.create(nazwaJednostki="l")
        
        


        # lists
        print("Seeding lists...")
        lista_1 = ListaZakupow.objects.create(
            nazwaListy="Tygodniowe zakupy",
            autor=uzytkownik
        )

        lista_2 = ListaZakupow.objects.create(
            nazwaListy="Urodziny Natalki",
            autor=uzytkownik
        )
        
        element_11 = ElementListy.objects.create(
            lista = ListaZakupow.objects.get(idLista = 1),
            nazwaElementu = 'szpinak',
            ilosc = 500.0,
            jednostka = Jednostka.objects.get(nazwaJednostki = 'g')
        )

        element_12 = ElementListy.objects.create(
            lista = ListaZakupow.objects.get(idLista = 1),
            nazwaElementu = 'pomidory',
            ilosc = 250.0,
            jednostka = Jednostka.objects.get(nazwaJednostki = 'g')
        )

        element_13 = ElementListy.objects.create(
            lista = ListaZakupow.objects.get(idLista = 1),
            nazwaElementu = 'śmietana 30%',
            ilosc = 200.0,
            jednostka = Jednostka.objects.get(nazwaJednostki = 'ml')
        )

        element_21 = ElementListy.objects.create(
            lista = ListaZakupow.objects.get(idLista = 2),
            nazwaElementu = 'jajka',
            ilosc = 6.0,
            jednostka = Jednostka.objects.get(nazwaJednostki = 'szt')
        )

    

        # recipes with ingredients
        print("Seeding recipes...")
        user = Uzytkownik.objects.get(idUzytkownik=1)

        przepisy = [
            {
                "nazwa": "Czekoladowe ciasto",
                "instrukcje": ["Wymieszaj składniki", "Upiecz w piekarniku przez 30 minut"],
                "skladniki": [
                    ("Mąka", 1.0, "kg"),
                    ("Jajko", 2.0, "szt"),
                    ("Czekolada", 100.0, "g")
                ]
            },
            {
                "nazwa": "Owocowy koktajl",
                "instrukcje": ["Zblenduj owoce", "Dodaj mleko i wymieszaj"],
                "skladniki": [
                    ("Banan", 2.0, "szt"),
                    ("Mleko", 250.0, "ml"),
                    ("Truskawki", 100.0, "g"),
                    ("Jogurt", 150.0, "ml")
                ]
            },
            {
                "nazwa": "Makaron z sosem",
                "instrukcje": ["Ugotuj makaron", "Dodaj sos i podawaj na ciepło"],
                "skladniki": [
                    ("Makaron", 200.0, "g"),
                    ("Sos pomidorowy", 300.0, "ml"),
                    ("Ser", 50.0, "g")
                ]
            },
            {
                "nazwa": "Sałatka grecka",
                "instrukcje": ["Pokroj warzywa", "Dodaj ser feta i oliwki"],
                "skladniki": [
                    ("Pomidor", 3.0, "szt"),
                    ("Ogórek", 1.0, "szt"),
                    ("Ser feta", 200.0, "g"),
                    ("Oliwki", 50.0, "g"),
                    ("Oliwa", 30.0, "ml")
                ]
            },
            {
                "nazwa": "Spaghetti Bolognese",
                "instrukcje": ["Podsmaż mięso", "Dodaj sos pomidorowy", "Gotuj przez 20 minut"],
                "skladniki": [
                    ("Makaron", 500, 'g'),
                    ("Mięso mielone", 300, 'g'),
                    ("Sos pomidorowy", 1, 'l'),
                    ("Cebula", 1, 'szt')
                ]
            },
            {
                "nazwa": "Placki ziemniaczane",
                "instrukcje": ["Zetrzyj ziemniaki", "Dodaj jajko", "Smaż na patelni"],
                "skladniki": [
                    ("Ziemniaki", 1, 'kg'),
                    ("Jajko", 1, 'szt'),
                    ("Mąka", 100, 'g'),
                    ("Olej", 50, 'ml')
                ]
            },
            {
                "nazwa": "Omlet z warzywami",
                "instrukcje": ["Roztrzep jajka", "Dodaj warzywa", "Smaż na patelni"],
                "skladniki": [
                    ("Jajka", 3, 'szt'),
                    ("Papryka", 1, 'szt'),
                    ("Ser żółty", 100, 'g')
                ]
            },
            {
                "nazwa": "Ciasto",
                "instrukcje": ["Wymieszaj składniki", "Upiecz w piekarniku przez 30 minut"],
                "skladniki": [
                    ("Mąka", 1.0, "kg"),
                    ("Jajko", 2.0, "szt")
                ]
            },
            {
                "nazwa": "Omlet",
                "instrukcje": ["Rozbij jajka", "Usmaż na patelni"],
                "skladniki": [
                    ("Jajko", 4.0, "szt"),
                    ("Masło", 10.0, "g"),
                    ("Mleko", 100.0, "ml")
                ]
            },
            {
                "nazwa": "Zupa pomidorowa",
                "instrukcje": ["Gotuj pomidory", "Dodaj przyprawy", "Podawaj z makaronem"],
                "skladniki": [
                    ("Pomidory", 1.0, "kg"),
                    ("Makaron", 200.0, "g")
                ]
            }
        ]


        for przepis_data in przepisy:
            przepis = Przepis.objects.create(
                autorPrzepisu=user,
                nazwaPrzepisu=przepis_data["nazwa"],
                instrukcje=przepis_data["instrukcje"],
                dataPublikacji=date.today()
            )
            
            for skladnik_nazwa, ilosc, jednostka_nazwa in przepis_data["skladniki"]:
                jednostka = Jednostka.objects.get(nazwaJednostki=jednostka_nazwa)
                skladnik = Skladnik.objects.create(
                    nazwaSkladnika=skladnik_nazwa,
                    przepis=przepis,
                    ilosc=ilosc,
                    jednostka=jednostka
                )

        
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
