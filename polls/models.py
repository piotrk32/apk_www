
from django.db import models

class GenderChoices(models.IntegerChoices):
    Kobieta = 1
    Mężczyzna = 2
    Inne = 3


class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=255, blank=False)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa


class Osoba(models.Model):
    imie = models.CharField(max_length=255, blank=False)
    nazwisko = models.CharField(max_length=255, blank=False)
    plec = models.IntegerField(choices=GenderChoices.choices)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)
    data_dodania = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'
