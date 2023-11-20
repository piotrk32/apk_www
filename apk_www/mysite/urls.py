from django.contrib import admin
from django.urls import include, path

from apk_www.tk.views import osoba_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tk/', include('tk.urls')),
    path('api/', include('tk.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('osoby/<int:pk>/', osoba_view, name='osoba_view')
]