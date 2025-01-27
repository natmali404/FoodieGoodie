from django.core.management.base import BaseCommand
from foodie_goodie_app.models import Forum, Post, Uzytkownik, ListaZakupow, Przepis, Skladnik, Jednostka, ElementListy
from datetime import date

class Command(BaseCommand):
    help = 'Seed database for testing purposes...'

    def handle(self, *args, **kwargs):
        # user
        print("Seeding users...")
        user_1 = Uzytkownik.objects.create(
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )

        user_2 = Uzytkownik.objects.create(
            nazwaUzytkownika="marmolada45",
            email="testuser2@example.com",
            haslo="password123"
        )

        user_3 = Uzytkownik.objects.create(
            nazwaUzytkownika="JaTuTylkoCzytam",
            email="testuser3@example.com",
            haslo="password123"
        )

        user_4 = Uzytkownik.objects.create(
            nazwaUzytkownika="sigma",
            email="testuser4@example.com",
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
            autor=user_1
        )

        lista_2 = ListaZakupow.objects.create(
            nazwaListy="Urodziny Natalki",
            autor=user_1
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
                autorPrzepisu=user_1,
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

        
        forums = [
            {
           "tytulForum": "Jakie znacie zdrowe przepisy?",
           "uzytkownik": user_1,
           "posts": [
               {
                   "trescPost": "Jak w tytule. Prosze podzielcie sie.",
                   "dataDodaniaPostu": "2024-01-25 16:15:00",
                   "autor": user_1,
                   "glosy": 2,
               },
               {
                   "trescPost": "Ja lubie placki z bananow i jajek",
                    "dataDodaniaPostu": "2024-01-25 16:16:00",
                   "autor": user_2,
                   "glosy": 8,
               },
               {
                   "trescPost": "TYLKO TYLE WYSTARCZY???? WOW",
                    "dataDodaniaPostu": "2024-01-25 16:17:00",
                   "autor": user_1,
                   "glosy": -1,
               },
               {
                   "trescPost": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "dataDodaniaPostu": "2024-01-25 16:18:00",
                   "autor": user_2,
                   "glosy": 20,
               }
            ]    
            },
        {
            "tytulForum": "Najlepsze ćwiczenia na siłowni",
            "uzytkownik": user_2,
            "posts": [
                {
                    "trescPost": "Jakie są wasze ulubione ćwiczenia na siłowni?",
                    "dataDodaniaPostu": "2024-01-24 09:30:00",
                    "autor": user_2,
                    "glosy": 5
                },
                {
                    "trescPost": "Przysiady to podstawa! Zawsze robię 4 serie po 12 powtórzeń",
                    "dataDodaniaPostu": "2024-01-24 10:15:00",
                    "autor": user_3,
                    "glosy": 12
                },
                {
                    "trescPost": "Ktoś wie coś o treningu na mięśnie pleców?",
                    "dataDodaniaPostu": "2024-01-24 11:00:00",
                    "autor": user_1,
                    "glosy": 3
                },
                {
                    "trescPost": "Martwica to król wszystkich ćwiczeń! Zmienia sylwetkę całkowicie",
                    "dataDodaniaPostu": "2024-01-24 12:45:00",
                    "autor": user_4,
                    "glosy": 15
                }
            ]
            }
        ]

        for forum in forums:
            new_forum = Forum.objects.create(
                tytulForum = forum["tytulForum"],
                uzytkownik = forum["uzytkownik"]
            )

            for post in forum["posts"]:
                Post.objects.create(
                    trescPost = post["trescPost"],
                    dataDodaniaPostu = post["dataDodaniaPostu"],
                    forum = new_forum,
                    autor = post["autor"],
                    glosy = post["glosy"]

                )

        
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
