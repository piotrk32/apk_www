import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Osoba, Druzyna, Stanowisko

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class StanowiskoType(DjangoObjectType):
    class Meta:
        model = Stanowisko
        fields = ('id', 'nazwa', 'opis')

class OsobaType(DjangoObjectType):
    class Meta:
        model = Osoba
        fields = ('id', 'imie', 'nazwisko', 'plec', 'stanowisko', 'miesiacDodania', 'wlasciciel')

    wlasciciel = graphene.Field(UserType)
    stanowisko = graphene.Field(StanowiskoType)

    def resolve_wlasciciel(self, info):
        return self.wlasciciel

    def resolve_stanowisko(self, info):
        return self.stanowisko

class DruzynaType(DjangoObjectType):
    class Meta:
        model = Druzyna
        fields = ('id', 'nazwa', 'zalozyciel', 'data_zalozenia')

class Query(graphene.ObjectType):
    all_persons = graphene.List(OsobaType)
    all_teams = graphene.List(DruzynaType)
    person_by_id = graphene.Field(OsobaType, id=graphene.Int(required=True))
    team_by_id = graphene.Field(DruzynaType, id=graphene.Int(required=True))

    def resolve_all_persons(self, info, **kwargs):
        return Osoba.objects.all()

    def resolve_all_teams(self, info, **kwargs):
        return Druzyna.objects.all()

    def resolve_person_by_id(self, info, id):
        return Osoba.objects.get(pk=id)

    def resolve_team_by_id(self, info, id):
        return Druzyna.objects.get(pk=id)

    find_persons_by_name = graphene.List(
        OsobaType,
        substr=graphene.String(required=True)
    )
    find_persons_by_surname = graphene.List(OsobaType, substr=graphene.String(required=True))

    find_persons_by_position = graphene.List(OsobaType, position_name=graphene.String(required=True))

    find_persons_by_month_added = graphene.List(OsobaType, month=graphene.Int(required=True))

    def resolve_find_persons_by_month_added(self, info, month):
        return Osoba.objects.filter(miesiac_dodania=month)

    def resolve_find_persons_by_position(self, info, position_name):
        return Osoba.objects.filter(stanowisko__nazwa__iexact=position_name)

    def resolve_find_persons_by_surname(self, info, substr):
        return Osoba.objects.filter(nazwisko__icontains=substr)

    def resolve_find_persons_by_name(self, info, substr):
        return Osoba.objects.filter(imie__iexact=substr)

schema = graphene.Schema(query=Query)
