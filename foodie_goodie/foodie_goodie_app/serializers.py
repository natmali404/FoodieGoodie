from rest_framework import serializers
from .models import ElementListy

class ElementListySerializer(serializers.ModelSerializer):
    jednostka = serializers.CharField(source='jednostka.nazwaJednostki')

    class Meta:
        model = ElementListy
        fields = ['idElement', 'nazwaElementu', 'ilosc', 'jednostka']