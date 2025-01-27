from django.test import TestCase

from foodie_goodie.foodie_goodie_app.recalculating_amount import recalculate
from .models import Skladnik, Jednostka

class RecalculateFunctionTest(TestCase):

    def setUp(self):
        self.jednostka_gram = Jednostka.objects.create(
            nazwaJednostki="g", minimalnaWartosc=1.0
        )
        self.jednostka_mililitr = Jednostka.objects.create(
            nazwaJednostki="ml", minimalnaWartosc=0.1
        )
        self.jednostka_szt=Jednostka.objects.create(
            nazwaJednostki="szt", minimalnaWartosc=1
        )

        self.ingredients = [
            Skladnik.objects.create(
                nazwaSkladnika="Mąka", ilosc=200, jednostka=self.jednostka_gram
            ),
            Skladnik.objects.create(
                nazwaSkladnika="Mleko", ilosc=500, jednostka=self.jednostka_mililitr
            ),
            Skladnik.objects.create(
                nazwaSkladnika="Jajko",ilosc=2,jednostka=self.jednostka_szt
            )
        ]

        self.eatvalues = {"kalorie": 1200, "białko": 20, "tłuszcz": 10}

    def test_recalculate_multiply(self):

        recalculate(self.ingredients, self.eatvalues, oldportion=2, newportion=4)


        self.assertEqual(self.ingredients[0].ilosc, 400)  # Mąka
        self.assertEqual(self.ingredients[1].ilosc, 1000)  # Mleko
        self.assertEqual(self.ingredients[2].ilosc, 4)

        self.assertEqual(self.eatvalues["kalorie"], 2400)
        self.assertEqual(self.eatvalues["białko"], 40)
        self.assertEqual(self.eatvalues["tłuszcz"], 20)

    def test_recalculate_divide(self):
        # Wywołanie funkcji z poprawnymi danymi
        recalculate(self.ingredients, self.eatvalues, oldportion=4, newportion=2)

        # Sprawdzanie składników
        self.assertEqual(self.ingredients[0].ilosc, 100)  # Mąka
        self.assertEqual(self.ingredients[1].ilosc, 250)  # Mleko
        self.assertEqual(self.ingredients[2].ilosc, 1)
        
        # Sprawdzanie wartości odżywczych
        self.assertEqual(self.eatvalues["kalorie"], 600)
        self.assertEqual(self.eatvalues["białko"], 10)
        self.assertEqual(self.eatvalues["tłuszcz"], 5)

    def test_recalculate_minimal_value_error(self):
        # Przypadek, gdy ilość składnika spada poniżej minimalnej wartości
        
        with self.assertRaises(ValueError) as context:
            recalculate(self.ingredients, self.eatvalues, oldportion=4, newportion=1)

        self.assertEqual(
            str(context.exception), "Nie można przeliczyc Jajko"
        )

    def test_recalculate_rounding(self):
        # Test zaokrąglania ilości składników
        self.ingredients[1].ilosc = 0.25  # Minimalna wartość jednostki mililitr to 0.1
        recalculate(self.ingredients, self.eatvalues, oldportion=1, newportion=2)

        self.assertEqual(self.ingredients[1].ilosc, 0.5)  # Powinno zaokrąglić do 0.5

    def test_recalculate_negative_portion(self):
        with self.assertRaises(ValueError) as context:
            recalculate(self.ingredients, self.eatvalues, oldportion=0, newportion=1)

        self.assertEqual(
            str(context.exception), "Wielkość porcji musi być dodatnia"
        )
