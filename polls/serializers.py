from rest_framework import serializers
from .models import Stanowisko, Osoba, Druzyna


class DruzynaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Druzyna
        fields = '__all__'

class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = ['id', 'nazwa', 'opis']

class OsobaSerializer(serializers.ModelSerializer):

    stanowisko = StanowiskoSerializer(read_only=True)
    stanowisko_id = serializers.PrimaryKeyRelatedField(
        queryset=Stanowisko.objects.all(), source='stanowisko', write_only=True
    )

    class Meta:
        model = Osoba
        fields = ['id', 'imie', 'nazwisko', 'plec', 'stanowisko', 'stanowisko_id']

    def create(self, validated_data):
        # Tworzenie instancji Osoba z zagnieżdżonymi danymi stanowiska
        stanowisko_data = validated_data.pop('stanowisko', None)
        osoba = Osoba.objects.create(**validated_data)
        if stanowisko_data:
            Stanowisko.objects.create(osoba=osoba, **stanowisko_data)
        return osoba

    def update(self, instance, validated_data):
        # Aktualizacja instancji Osoba z zagnieżdżonymi danymi stanowiska
        stanowisko_data = validated_data.pop('stanowisko', None)
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.plec = validated_data.get('plec', instance.plec)
        instance.save()

        if stanowisko_data:
            stanowisko = instance.stanowisko
            stanowisko.nazwa = stanowisko_data.get('nazwa', stanowisko.nazwa)
            stanowisko.opis = stanowisko_data.get('opis', stanowisko.opis)
            stanowisko.save()

        return instance