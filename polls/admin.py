from django.contrib import admin
from .models import Osoba, Stanowisko

@admin.display(description='Stanowisko (id)')
def stanowisko_display(obj):
    return f'{obj.stanowisko.nazwa} ({obj.stanowisko.id})'

class OsobaAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'plec', 'stanowisko_display', 'data_dodania')  # Uwzględnienie stanowisko_display
    list_filter = ('stanowisko',)  # Dodanie filtru dla stanowiska

admin.site.register(Stanowisko)
admin.site.register(Osoba, OsobaAdmin)
