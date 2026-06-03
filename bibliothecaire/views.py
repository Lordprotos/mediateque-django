from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from catalogue.models import Membre, Livre, Dvd, Cd, Emprunt

def accueil(request):
    return render(request, 'bibliothecaire/accueil.html')

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/liste_membres.html', {'membres': membres})

def creer_membre(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        Membre.objects.create(nom=nom, prenom=prenom)
        return redirect('liste_membres')
    return render(request, 'bibliothecaire/creer_membre.html')

def liste_medias(request):
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    return render(request, 'bibliothecaire/liste_medias.html', {
        'livres': livres, 'dvds': dvds, 'cds': cds
    })

def creer_emprunt(request):
    if request.method == 'POST':
        membre = get_object_or_404(Membre, id=request.POST['membre_id'])
        if not membre.peut_emprunter():
            return render(request, 'bibliothecaire/erreur.html', {
                'message': 'Ce membre ne peut pas emprunter.'
            })
        # Logique d'emprunt à compléter selon le type de média
        return redirect('liste_medias')
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/creer_emprunt.html', {'membres': membres})

def retour_emprunt(request):
    if request.method == 'POST':
        from django.utils import timezone
        emprunt = get_object_or_404(Emprunt, id=request.POST['emprunt_id'])
        emprunt.date_retour = timezone.now()
        emprunt.save()
        return redirect('liste_membres')
    emprunts = Emprunt.objects.filter(date_retour__isnull=True)
    return render(request, 'bibliothecaire/retour_emprunt.html', {'emprunts': emprunts})

def ajouter_media(request):
    if request.method == 'POST':
        type_media = request.POST['type']
        nom = request.POST['nom']
        if type_media == 'livre':
            Livre.objects.create(nom=nom, auteur=request.POST['auteur'])
        elif type_media == 'dvd':
            Dvd.objects.create(nom=nom, realisateur=request.POST['realisateur'])
        elif type_media == 'cd':
            Cd.objects.create(nom=nom, artiste=request.POST['artiste'])
        return redirect('liste_medias')
    return render(request, 'bibliothecaire/ajouter_media.html')

def modifier_membre(request, id):
    membre = get_object_or_404(Membre, id=id)
    if request.method == 'POST':
        membre.nom = request.POST['nom']
        membre.prenom = request.POST['prenom']
        membre.save()
        return redirect('liste_membres')
    return render(request, 'bibliothecaire/modifier_membre.html', {'membre': membre})