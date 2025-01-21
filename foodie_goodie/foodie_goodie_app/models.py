from django.db import models

from django.db import models

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
    tytulPost = models.CharField(max_length=50)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    def __str__(self):
        return self.tytulPost


class Post(models.Model):
    idPost = models.AutoField(primary_key=True)
    tytulPost = models.CharField(max_length=255)
    trescPost = models.TextField()
    dataDodaniaPostu = models.DateField()
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="posty")
    autor = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    def __str__(self):
        return self.tytulPost


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
    nazwaSkladnika = models.CharField(max_length=50)
    ilosc = models.FloatField()
    jednostka = models.ForeignKey(Jednostka, on_delete=models.CASCADE)

class SkladnikPrzepisu(models.Model):
    idSkladnikPrzepis = models.AutoField(primary_key=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    skladnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)

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
