from django.test import TestCase

from ..models import Osoba, Druzyna, Stanowisko

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Osoba.objects.create(name='Jan', shirt_size='L')
        # pass

    def test_first_name_label(self):
        person = Osoba.objects.get(id=1)
        field_label = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        # pass

    def test_first_name_max_length(self):
        person = Osoba.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)
        # pass
    def test_creating_two_persons_assigns_unique_ids(self):
        person1 = Osoba.objects.create(imie='Jan', nazwisko='Kowalski', plec='M')
        person2 = Osoba.objects.create(imie='Anna', nazwisko='Nowak', plec='K')
        self.assertNotEqual(person1.id, person2.id)
        # pass

class DruzynaModeltest(TestCase):
    @classmethod
    def test_creating_two_druzyna_assigns_unique_ids(self):
        druzyna1 = Druzyna.objects.create(nazwa='Orly', zalozyciel='JanK')
        druzyna2 = Druzyna.objects.create(nazwa='Wilky', zalozyciel='AnnaN')
        self.assertNotEqual(druzyna1.id, druzyna2.id)
        # pass

class StanowiskoModeltest(TestCase):
    @classmethod
    def test_creating_two_druzyna_assigns_unique_ids(self):
        stanowisko1 = Stanowisko.objects.create(nazwa='Manager')
        stanowisko2 = Stanowisko.objects.create(nazwa='Kierownik')
        self.assertNotEqual(stanowisko1.id, stanowisko2.id)
        # pass
