from django.core.management.base import BaseCommand
from foodie_goodie_app.models import Jadlospis, JadlospisPrzepis, Przepis, Uzytkownik
from datetime import date

class Command(BaseCommand):
    help = 'Seed diets for testing purposes...'

    def handle(self, *args, **kwargs):
        user = Uzytkownik.objects.get(idUzytkownik=1)
        
        jadlospis1 = Jadlospis.objects.create(
                nazwa = f"Przykładowy jadłospis",
                autor = user,
                dataUtworzenia = date.today()
            )
        for i in range(3):
            JadlospisPrzepis.objects.create(
                jadlospis = jadlospis1,
                przepis = Przepis.objects.get(idPrzepis=i+1),
                dzienTygodnia = i,
                godzina = i
            )
            
        jadlospis2 = Jadlospis.objects.create(
                nazwa = f"Jadłospis bezglutenowy",
                autor = user,
                dataUtworzenia = date.today()
            )
        for i in range(3,6):
            JadlospisPrzepis.objects.create(
                jadlospis = jadlospis2,
                przepis = Przepis.objects.get(idPrzepis=i+1),
                dzienTygodnia = i,
                godzina = i
            )
            

        
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the diets!'))
