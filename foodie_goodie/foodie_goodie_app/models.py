from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from django.db.models import Min

class Uzytkownik(models.Model):
    idUzytkownik = models.AutoField(primary_key=True)
    nazwaUzytkownika = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    haslo = models.CharField(max_length=80)

    def __str__(self):
        return self.nazwaUzytkownika


class Profil(models.Model):
    idProfil = models.AutoField(primary_key=True)
    preferencjeDiety = models.TextField()
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE, related_name="profil")


class Uprawnienia(models.Model):
    idUprawnienia = models.AutoField(primary_key=True)
    nazwaUprawnienia = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwaUprawnienia


class UprawnieniaUzytkownikow(models.Model):
    uprawnienia = models.ForeignKey(Uprawnienia, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('uprawnienia', 'uzytkownik')


class Wpis(models.Model):
    idWpis = models.AutoField(primary_key=True)
    autor = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, related_name="wpisy")
    tresc = models.TextField()
    dataDodania = models.DateField()

    def __str__(self):
        return f"Wpis {self.idWpis}"


class GlosyWpis(models.Model):
    wpis = models.ForeignKey(Wpis, on_delete=models.CASCADE)
    autorGlosu = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    zaglosowano = models.BooleanField()

    class Meta:
        unique_together = ('wpis', 'autorGlosu')


class Forum(models.Model):
    idForum = models.AutoField(primary_key=True)
    tytulForum = models.CharField(max_length=50)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    def __str__(self):
        return self.tytulForum
    def data_zalozenia(self):
        pierwsza_data = self.posty.aggregate(Min('dataDodaniaPostu'))['dataDodaniaPostu__min']
        return pierwsza_data


class Post(models.Model):
    idPost = models.AutoField(primary_key=True)
    trescPost = models.TextField()
    dataDodaniaPostu = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="posty")
    autor = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    glosy = models.IntegerField(default=0)
    obrazek = models.ImageField(
        upload_to='img/upload/', 
        null=True, 
        blank=True, 
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])]
    )



# fixed fields
class Przepis(models.Model):
    idPrzepis = models.AutoField(primary_key=True)
    autorPrzepisu = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    nazwaPrzepisu = models.CharField(max_length=50)
    #skladniki = models.JSONField() <- Skladnik ma ForeignKey i trzeba to pobrac; potrzebne np do listy zakupow
    instrukcje = models.JSONField()
    dataPublikacji = models.DateField()

    def __str__(self):
        return self.nazwaPrzepisu
    

class ListaZakupow(models.Model):
    idLista = models.AutoField(primary_key=True)
    nazwaListy = models.CharField(max_length=50)
    autor = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, related_name="listy_zakupow")

    def __str__(self):
        return self.nazwaListy


# new tables: skladnik, skladnikprzepisu, elementlisty, jednostka
class Jednostka(models.Model):
    idJednostka = models.AutoField(primary_key=True)
    nazwaJednostki = models.CharField(max_length=5)

class Skladnik(models.Model):
    idSkladnik = models.AutoField(primary_key=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    nazwaSkladnika = models.CharField(max_length=50)
    ilosc = models.FloatField()
    jednostka = models.ForeignKey(Jednostka, on_delete=models.CASCADE)

# class SkladnikPrzepisu(models.Model):
#     idSkladnikPrzepis = models.AutoField(primary_key=True)
#     przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
#     skladnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)

class ElementListy(models.Model):
    idElement = models.AutoField(primary_key=True)
    lista = models.ForeignKey(ListaZakupow, on_delete=models.CASCADE)
    nazwaElementu = models.CharField(max_length=50)
    ilosc = models.FloatField()
    jednostka = models.ForeignKey(Jednostka, on_delete=models.CASCADE)
    zaznaczony = models.BooleanField(default = False)

###


class Ranking(models.Model):
    idRanking = models.AutoField(primary_key=True)
    nazwaRankingu = models.CharField(max_length=20)
    typRankingu = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwaRankingu


class OcenyPrzepisu(models.Model):
    idOceny = models.AutoField(primary_key=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, related_name="oceny")
    oceniajacy = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    wartosc = models.IntegerField()

    def __str__(self):
        return f"Ocena {self.idOceny} - {self.wartosc}"


class PrzepisyWRankingu(models.Model):
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    pozycja = models.IntegerField()

    class Meta:
        unique_together = ('ranking', 'przepis')


class KomentarzePrzepisu(models.Model):
    idKomentarz = models.AutoField(primary_key=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, related_name="komentarze")
    komentarz = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="odpowiedzi")
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    dataKomentarza = models.DateField()
    trescKomentarza = models.CharField(max_length=250)

    def __str__(self):
        return f"Komentarz {self.idKomentarz}"






class KategorieDiety(models.Model):
    idKategoria = models.AutoField(primary_key=True)
    nazwaKategorii = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwaKategorii


class ListyZDietami(models.Model):
    lista = models.ForeignKey(ListaZakupow, on_delete=models.CASCADE)
    kategoria = models.ForeignKey(KategorieDiety, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lista', 'kategoria')

#diet

class Jadlospis(models.Model):
    idJadlospis = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    autor = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, related_name="jadlospisy")
    dataUtworzenia = models.DateField(default=now)

    def __str__(self):
        return f"Jadlospis {self.idJadlospis} - {self.autor.nazwaUzytkownika}"


class JadlospisPrzepis(models.Model):
    DZIEŃ_TYGODNIA_CHOICES = [
        (0, "Poniedziałek"),
        (1, "Wtorek"),
        (2, "Środa"),
        (3, "Czwartek"),
        (4, "Piątek"),
        (5, "Sobota"),
        (6, "Niedziela"),
    ]
    PORA_DNIA_CHOICES =[
        (0, "Sniadanie"),
        (1, "Lunch"),
        (2, "Obiad"),
        (3, "Podwieczorek"),
        (4, "Kolacja"),
    ]

    idJadlospisPrzepis = models.AutoField(primary_key=True)
    jadlospis = models.ForeignKey(Jadlospis, on_delete=models.CASCADE, related_name="przepisy")
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    dzienTygodnia = models.IntegerField(choices=DZIEŃ_TYGODNIA_CHOICES)
    godzina = models.IntegerField(choices=PORA_DNIA_CHOICES)


    class Meta:
        unique_together = ('jadlospis', 'przepis', 'dzienTygodnia', 'godzina')

    def __str__(self):
        dzien = dict(self.DZIEŃ_TYGODNIA_CHOICES).get(self.dzienTygodnia, "Nieznany dzień")
        godz = dict(self.PORA_DNIA_CHOICES).get(self.PORA_DNIA_CHOICES, "Nieznana pora dnia")
        return f"{self.przepis.nazwaPrzepisu} - {dzien} {godz}"