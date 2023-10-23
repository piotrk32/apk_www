from django.contrib import admin
from .models import Osoba, Stanowisko

@admin.display(description='Stanowisko (id)')
def stanowisko_display(obj):
    return f'{obj.stanowisko.nazwa} ({obj.stanowisko.id})'

class OsobaAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'plec', 'stanowisko_display', 'data_dodania')
    list_filter = ('stanowisko', 'data_dodania')  # Dodanie filtru dla stanowiska i daty dodania

class StanowiskoAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'opis')
    list_filter = ('nazwa',)  # Dodanie filtra dla nazwy

admin.site.register(Stanowisko, StanowiskoAdmin)  # Zarejestrowanie modelu Stanowisko z niestandardowym adminem
admin.site.register(Osoba, OsobaAdmin)  # Zarejestrowanie modelu Osoba z niestandardowym adminem
