from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Osoba, Druzyna
from .serializers import OsobaSerializer, DruzynaSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Osoba
from .serializers import OsobaSerializer
from django.core.exceptions import PermissionDenied

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def osoba_view(request, pk):
    """
    Widok, który wymaga uprawnienia 'can_view_other_persons' dla wyświetlania osób,
    których użytkownik nie jest właścicielem.
    """
    try:
        osoba = Osoba.objects.get(pk=pk)

        if osoba.wlasciciel == request.user or request.user.has_perm('app.can_view_other_persons'):
            serializer = OsobaSerializer(osoba)
            return Response(serializer.data)
        else:
            raise PermissionDenied()

    except Osoba.DoesNotExist:
        return HttpResponse(f"W bazie nie ma osoby o id={pk}.")
    except PermissionDenied:
        return Response({'detail': 'You do not have permission to view this object.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated, DjangoModelPermissions])
def osoba_view(request, pk):
    """
    Widok, który wymaga uprawnienia 'view_osoba'.
    """
    try:
        if not request.user.has_perm('app.view_osoba'):
            raise PermissionDenied()

        osoba = Osoba.objects.get(pk=pk)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)
    except Osoba.DoesNotExist:
        return HttpResponse(f"W bazie nie ma osoby o id={pk}.")
    except PermissionDenied:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def osoba_stanowisko_list(request, stanowisko_id):
    if request.method == 'GET':
        osoby = Osoba.objects.filter(stanowisko_id=stanowisko_id)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([DjangoModelPermissions])
def osoba_list(request):
    if request.method == 'GET':
        osoby = Osoba.objects.filter(wlasciciel=request.user)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def osoba_detail(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OsobaSerializer(osoba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def osoba_search(request, name):
    osoby = Osoba.objects.filter(nazwa__icontains=name)
    serializer = OsobaSerializer(osoby, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def druzyna_list(request):
    if request.method == 'GET':
        druzyny = Druzyna.objects.all()
        serializer = DruzynaSerializer(druzyny, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DruzynaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def druzyna_detail(request, pk):
    try:
        druzyna = Druzyna.objects.get(pk=pk)
    except Druzyna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DruzynaSerializer(druzyna)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DruzynaSerializer(druzyna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        druzyna.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
