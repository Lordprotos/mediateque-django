from django.shortcuts import render
from catalogue.models import Livre, Dvd, Cd, JeuDePlateau

def liste_medias(request):
    return render(request, 'membre/liste_medias.html', {
        'livres': Livre.objects.all(),
        'dvds': Dvd.objects.all(),
        'cds': Cd.objects.all(),
        'jeux': JeuDePlateau.objects.all(),
    })