# Test Serializera Django Rest Framework

## Przykład użycia serializerów dla modeli `Stanowisko` i `Osoba`

```python
# Importy modeli i serializerów
from aplikacja.models import Stanowisko, Osoba
from aplikacja.serializers import StanowiskoSerializer, OsobaSerializer

# Importy Django Rest Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

# Tworzenie instancji modelu Stanowisko
stanowisko = Stanowisko(nazwa='Dyrektor', opis='Odpowiedzialny za zarządzanie firmą')
stanowisko.save()

# Serializacja instancji Stanowisko
stanowisko_serializer = StanowiskoSerializer(stanowisko)
stanowisko_data = stanowisko_serializer.data
print(stanowisko_data)

# Serializacja danych do formatu JSON
stanowisko_json = JSONRenderer().render(stanowisko_data)
print(stanowisko_json)

# Tworzenie instancji modelu Osoba
osoba = Osoba(imie='Jan', nazwisko='Kowalski', plec='M', stanowisko=stanowisko)
osoba.save()

# Serializacja instancji Osoba
osoba_serializer = OsobaSerializer(osoba)
osoba_data = osoba_serializer.data
print(osoba_data)

# Serializacja danych do formatu JSON
osoba_json = JSONRenderer().render(osoba_data)
print(osoba_json)

# Deserializacja danych z formatu JSON
osoba_stream = io.BytesIO(osoba_json)
osoba_parsed_data = JSONParser().parse(osoba_stream)

# Tworzenie obiektu serializera z deserializowanymi danymi
osoba_deserializer = OsobaSerializer(data=osoba_parsed_data)

# Walidacja i zapis danych
if osoba_deserializer.is_valid():
    osoba_deserializer.save()
    print('Deserializacja i zapis danych zakończony sukcesem.')
else:
    print('Błąd walidacji:', osoba_deserializer.errors)

# Wyświetlenie pól wczytanego serializera
print(osoba_deserializer.fields)