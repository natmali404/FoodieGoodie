from django.core.management.base import BaseCommand
from foodie_goodie_app.models import ElementListy, ListaZakupow, Przepis, Skladnik, Jednostka, SkladnikPrzepisu
from datetime import date

class Command(BaseCommand):
    help = 'Seed elements of lists data for testing purposes...'

    def handle(self, *args, **kwargs):

        if(ListaZakupow.objects.filter(idLista=1).exists() and ListaZakupow.objects.filter(idLista=2).exists()):
            print("Znaleziono listy, seeding...")
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

            self.stdout.write(self.style.SUCCESS('Successfully seeded the database with elements of lists!'))

        else:
            print("Najpierw uruchom seeder seed_lists_and_recipes")


        
