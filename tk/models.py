from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Druzyna(models.Model):
    nazwa = models.CharField(max_length=100)
    zalozyciel = models.CharField(max_length=100)
    data_zalozenia = models.DateField()

    def __str__(self):
        return self.nazwa

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=255, blank=False)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa

def default_month():
    return timezone.now().month

def get_default_user():
    user, created = User.objects.get_or_create(username='tomaciej22')
    return user.id

class Osoba(models.Model):

    PLEC_CHOICES = [
        ('K', 'Kobieta'),
        ('M', 'Mężczyzna'),
        ('I', 'Inne'),
    ]
    imie = models.CharField(max_length=255, blank=False)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    nazwisko = models.CharField(max_length=255, blank=False)
    plec = models.CharField(max_length=1, choices=PLEC_CHOICES)
    stanowisko = models.ForeignKey('Stanowisko', on_delete=models.CASCADE)
    miesiac_dodania = models.IntegerField(default=default_month)

    class Meta:
        permissions = [
            ("can_view_other_persons", "Can view other persons"),
        ]

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    def clean(self):
        if not self.imie.replace(' ', '').isalpha():
            raise ValidationError({'imie': 'Imie może zawierać tylko litery.'})
        if not self.nazwisko.replace(' ', '').isalpha():
            raise ValidationError({'nazwisko': 'Nazwisko może zawierać tylko litery.'})

        current_month = timezone.now().month
        if self.miesiac_dodania > current_month:
            raise ValidationError({'miesiac_dodania': 'Miesiąc dodania nie może być z przyszłości.'})

class Meta:
    app_label1 = 'tk'
