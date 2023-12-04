import uuid
from datetime import date
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from rest_framework import status
from rest_framework.test import APIClient
from base64 import b64encode
from django.test import TestCase
from rest_framework.authtoken.models import Token
from ..models import Osoba, Druzyna, Stanowisko


class PersonModelTest(TestCase):
    def setUp(self):
        stanowisko = Stanowisko.objects.create(nazwa='Manager', opis='Manages the team.')
        self.osoba = Osoba.objects.create(
            imie='Jan',
            nazwisko='Kowalski',
            plec='M',
            stanowisko=stanowisko
        )
        # pass

    def test_first_name_label(self):
        person = Osoba.objects.get(id=1)
        field_label = person._meta.get_field('imie').verbose_name
        self.assertEqual(field_label, 'imie')
        # pass

    def test_first_name_max_length(self):
        person = Osoba.objects.get(id=1)
        max_length = person._meta.get_field('imie').max_length
        self.assertEqual(max_length, 255)
        # pass
    def test_creating_two_persons_assigns_unique_ids(self):
        person2 = Osoba.objects.create(
            imie='Anna',
            nazwisko='Nowak',
            plec='K',
            stanowisko=self.osoba.stanowisko  # Reuse the stanowisko from setUp
        )
        self.assertNotEqual(self.osoba.id, person2.id)
        # pass

class DruzynaModeltest(TestCase):
    def test_creating_two_druzyna_assigns_unique_ids(self):
        druzyna1 = Druzyna.objects.create(nazwa='Orly', zalozyciel='JanK', data_zalozenia=date.today())
        druzyna2 = Druzyna.objects.create(nazwa='Wilky', zalozyciel='AnnaN', data_zalozenia=date.today())
        self.assertNotEqual(druzyna1.id, druzyna2.id)
        # pass

class StanowiskoModeltest(TestCase):
    def test_creating_two_druzyna_assigns_unique_ids(self):
        stanowisko1 = Stanowisko.objects.create(nazwa='Manager', opis='test')
        stanowisko2 = Stanowisko.objects.create(nazwa='Kierownik', opis='test')
        self.assertNotEqual(stanowisko1.id, stanowisko2.id)
        # pass

class TestOsobaCreationWithBasicAuth(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_lab7', 'wiocha22')
        permission = Permission.objects.get(codename='add_osoba', content_type__app_label='tk')
        self.user.user_permissions.add(permission)
        self.client = APIClient()
        self.stanowisko = Stanowisko.objects.create(nazwa='Manager', opis='Menadzere lelele')
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_create_osoba_with_basic_auth(self):
        credentials = b64encode(b'user1:user1password').decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        #print("WYNIK::::::::::::::::::::::::::: ", credentials)
        data = {
            'imie': 'test',
            'nazwisko': 'testt',
            'plec': 'M',
            'stanowisko_id': self.stanowisko.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/osoby/', data, format='json')
        print("WYNIK:::::::::::::::::::::::::::TestOsobaCreationWithBasicAuth:::", response.status_code)
        #print("CONTENT::::::::::::::::::::::::::: ", response.content)
        #print("KEY::::::::::::::::::::::::::: ", self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OsobaCreationTokenAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_lab7', 'wiocha22')
        self.stanowisko = Stanowisko.objects.create(nazwa='Manager', opis='Manages the team')
        permission = Permission.objects.get(codename='add_osoba', content_type__app_label='tk')
        self.user.user_permissions.add(permission)
        self.client = APIClient()
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_osoba_with_token_auth(self):
        data = {
            'imie': 'Siurek',
            'nazwisko': 'Murek',
            'plec': 'K',
            'stanowisko_id': self.stanowisko.id
        }

        response = self.client.post('/api/osoby/', data, format='json')
        #print("WYNIK::::::::::::::::::::::::::: ",response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("WYNIK:::::::::::::::::::::::::::OsobaCreationTokenAuthTest::: ",response.status_code)