from django.db import models
from django.utils import timezone

# Classe abstraite pour éviter la duplication
class Media(models.Model):
    nom = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    class Meta:
        abstract = True  # Pas de table créée pour cette classe

class Livre(Media):
    auteur = models.CharField(max_length=200)

class Dvd(Media):
    realisateur = models.CharField(max_length=200)

class Cd(Media):
    artiste = models.CharField(max_length=200)

class JeuDePlateau(models.Model):  # Pas de Media car pas d'emprunt
    nom = models.CharField(max_length=200)
    createur = models.CharField(max_length=200)

class Membre(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)

    def est_bloque(self):
        # Calculé dynamiquement, pas stocké en base
        return self.emprunt_set.filter(
            date_retour__isnull=True,
            date_emprunt__lt=timezone.now() - timezone.timedelta(weeks=1)
        ).exists()

    def peut_emprunter(self):
        emprunts_actifs = self.emprunt_set.filter(date_retour__isnull=True)
        return not self.est_bloque() and emprunts_actifs.count() < 3

class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    # On utilise un champ générique pour lier Livre, Dvd ou Cd
    media_type = models.CharField(max_length=50)   # 'livre', 'dvd', 'cd'
    media_id = models.IntegerField()
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)