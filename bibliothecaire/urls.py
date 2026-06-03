from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    path('membres/<int:id>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('medias/ajouter/', views.ajouter_media, name='ajouter_media'),
    path('emprunts/creer/', views.creer_emprunt, name='creer_emprunt'),
    path('emprunts/retour/', views.retour_emprunt, name='retour_emprunt'),
]