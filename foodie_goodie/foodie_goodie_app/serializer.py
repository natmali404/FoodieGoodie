from rest_framework import serializers
from .models import Wpis

class WpisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wpis
        fields = '__all__'
