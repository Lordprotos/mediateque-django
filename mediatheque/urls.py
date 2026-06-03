from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bibliothecaire/', include('bibliothecaire.urls')),
    path('membre/', include('membre.urls')),
]