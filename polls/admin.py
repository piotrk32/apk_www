from django.contrib import admin
from .models import Osoba, Stanowisko

class OsobaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'plec', 'stanowisko', 'data_dodania']

admin.site.register(Stanowisko)
admin.site.register(Osoba, OsobaAdmin)