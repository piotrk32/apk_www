from your_app_name.models import Osoba, Stanowisko

# 1. Wyświetlenie wszystkich obiektów modelu Osoba
wszystkie_osoby = Osoba.objects.all()
print(wszystkie_osoby)

# 2. Wyświetlenie obiektu modelu Osoba z id = 3
osoba_id_3 = Osoba.objects.get(id=3)
print(osoba_id_3)

# 3. Wyświetlenie obiektów modelu Osoba, których nazwisko rozpoczyna się na wybraną przez Ciebie literę alfabetu
# Zakładając, że wybrana litera to 'K'
osoby_z_litera_k = Osoba.objects.filter(nazwisko__startswith='K')
print(osoby_z_litera_k)

# 4. Wyświetlenie unikalnej listy stanowisk przypisanych dla modeli Osoba
unikalne_stanowiska = Osoba.objects.values_list('stanowisko', flat=True).distinct()
print(unikalne_stanowiska)

# 5. Wyświetlenie nazw stanowisk posortowanych alfabetycznie malejąco
nazwy_stanowisk_malejaco = Stanowisko.objects.order_by('-nazwa').values_list('nazwa', flat=True)
print(nazwy_stanowisk_malejaco)

# 6. Dodanie nowej instancji obiektu klasy Osoba i zapisanie w bazie
nowa_osoba = Osoba(imie='Jan', nazwisko='Kowalski', plec='M', stanowisko=Stanowisko.objects.get(id=1))
nowa_osoba.save()