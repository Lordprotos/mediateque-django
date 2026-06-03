from django.urls import path
from . import views

urlpatterns = [
    path('medias/', views.liste_medias, name='membre_liste_medias'),
]