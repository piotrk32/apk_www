import django
django.setup()

from models import Osoba, Stanowisko

def execute_queries():
    # 1. Wyświetlenie wszystkich obiektów modelu Osoba
    wszystkie_osoby = Osoba.objects.all()
    print(f'Wszystkie osoby: {wszystkie_osoby}')

    # 2. Wyświetlenie obiektu modelu Osoba z id = 3
    try:
        osoba_id_3 = Osoba.objects.get(id=3)
        print(f'Osoba z ID 3: {osoba_id_3}')
    except Osoba.DoesNotExist:
        print('Nie ma osoby z ID 3')

    # 3. Wyświetlenie obiektów modelu Osoba, których nazwisko rozpoczyna się na wybraną przez Ciebie literę alfabetu
    osoby_z_litera_k = Osoba.objects.filter(nazwisko__startswith='K')
    print(f'Osoby, których nazwiska zaczynają się na literę K: {osoby_z_litera_k}')

    # 4. Wyświetlenie unikalnej listy stanowisk przypisanych dla modeli Osoba
    unikalne_stanowiska = Osoba.objects.values_list('stanowisko__nazwa', flat=True).distinct()
    print(f'Unikalne stanowiska: {unikalne_stanowiska}')

    # 5. Wyświetlenie nazw stanowisk posortowanych alfabetycznie malejąco
    nazwy_stanowisk_malejaco = Stanowisko.objects.order_by('-nazwa').values_list('nazwa', flat=True)
    print(f'Nazwy stanowisk malejąco: {nazwy_stanowisk_malejaco}')

    # 6. Dodanie nowej instancji obiektu klasy Osoba i zapisanie w bazie
    nowe_stanowisko, created = Stanowisko.objects.get_or_create(nazwa='Nowe Stanowisko')
    nowa_osoba = Osoba(imie='Jan', nazwisko='Kowalski', plec='M', stanowisko=nowe_stanowisko)
    nowa_osoba.save()
    print(f'Dodano nową osobę: {nowa_osoba}')

if __name__ == "__main__":
    execute_queries()
