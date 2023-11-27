from django.urls import path
from .views import osoba_list, osoba_detail, osoba_search, druzyna_list, druzyna_detail, osoba_view

urlpatterns = [
    path('osoby/', osoba_list),
    path('osoby/<int:pk>/', osoba_detail),
    path('osoby/search/<str:name>/', osoba_search),
    path('druzyny/', druzyna_list),
    path('druzyny/<int:pk>/', druzyna_detail),
    path('osoba/<int:pk>/', osoba_view, name='osoba-view')
]