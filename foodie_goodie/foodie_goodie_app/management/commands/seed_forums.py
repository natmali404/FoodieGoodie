from django.core.management.base import BaseCommand
from foodie_goodie_app.models import Uzytkownik, Forum, Post
from datetime import date

class Command(BaseCommand):
    help = 'Seed database for testing purposes...'

    def handle(self, *args, **kwargs):

        #additional users
        
        uzytkownik = Uzytkownik.objects.create(
            nazwaUzytkownika="marmolada45",
            email="testuser2@example.com",
            haslo="password123"
        )

        uzytkownik = Uzytkownik.objects.create(
            nazwaUzytkownika="JaTuTylkoCzytam",
            email="testuser3@example.com",
            haslo="password123"
        )
        
        forums = [
            {
           "tytulForum": "Jakie znacie zdrowe przepisy?",
           "uzytkownik": 1,
           "posts": [
               {
                   "trescPost": "Jak w tytule. Prosze podzielcie sie.",
                   "dataDodaniaPostu": "2024-01-25 16:15:00",
                   "autor": 1,
                   "glosy": 2,
               },
               {
                   "trescPost": "Ja lubie placki z bananow i jajek",
                    "dataDodaniaPostu": "2024-01-25 16:16:00",
                   "autor": 2,
                   "glosy": 8,
               },
               {
                   "trescPost": "TYLKO TYLE WYSTARCZY???? WOW",
                    "dataDodaniaPostu": "2024-01-25 16:17:00",
                   "autor": 1,
                   "glosy": -1,
               },
               {
                   "trescPost": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "dataDodaniaPostu": "2024-01-25 16:18:00",
                   "autor": 2,
                   "glosy": 20,
               }
            ]    
            },
        {
            "tytulForum": "Najlepsze ćwiczenia na siłowni",
            "uzytkownik": 2,
            "posts": [
                {
                    "trescPost": "Jakie są wasze ulubione ćwiczenia na siłowni?",
                    "dataDodaniaPostu": "2024-01-24 09:30:00",
                    "autor": 2,
                    "glosy": 5
                },
                {
                    "trescPost": "Przysiady to podstawa! Zawsze robię 4 serie po 12 powtórzeń",
                    "dataDodaniaPostu": "2024-01-24 10:15:00",
                    "autor": 2,
                    "glosy": 12
                },
                {
                    "trescPost": "Ktoś wie coś o treningu na mięśnie pleców?",
                    "dataDodaniaPostu": "2024-01-24 11:00:00",
                    "autor": 1,
                    "glosy": 3
                },
                {
                    "trescPost": "Martwica to król wszystkich ćwiczeń! Zmienia sylwetkę całkowicie",
                    "dataDodaniaPostu": "2024-01-24 12:45:00",
                    "autor": 3,
                    "glosy": 15
                }
            ]
            }
        ]

        for forum in forums:
            new_forum = Forum.objects.create(
                tytulForum = forum["tytulForum"],
                uzytkownik = Uzytkownik.objects.get(idUzytkownik=forum["uzytkownik"])
            )

            for post in forum["posts"]:
                Post.objects.create(
                    trescPost = post["trescPost"],
                    dataDodaniaPostu = post["dataDodaniaPostu"],
                    forum = new_forum,
                    autor = Uzytkownik.objects.get(idUzytkownik=post["autor"]),
                    glosy = post["glosy"]

                )


        
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
