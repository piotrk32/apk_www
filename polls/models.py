import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=255, blank=False)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa

import datetime
from django.db import models

class Osoba(models.Model):
    PLEC_CHOICES = [
        ('K', 'Kobieta'),
        ('M', 'Mężczyzna'),
        ('I', 'Inne'),
    ]
    imie = models.CharField(max_length=255, blank=False)
    nazwisko = models.CharField(max_length=255, blank=False)
    plec = models.CharField(max_length=1, choices=PLEC_CHOICES)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)
    miesiac_dodania = models.IntegerField(default=lambda: timezone.now().month)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    def clean(self):
        # Walidacja dla pola 'nazwa'
        if not self.nazwa.replace(' ', '').isalpha():
            raise ValidationError({'nazwa': 'Nazwa może zawierać tylko litery.'})

        # Walidacja dla pola 'miesiac_dodania'
        current_month = timezone.now().month
        current_year = timezone.now().year
        if self.miesiac_dodania > current_month and self.rok_dodania >= current_year:
            raise ValidationError({'miesiac_dodania': 'Miesiąc dodania nie może być z przyszłości.'})