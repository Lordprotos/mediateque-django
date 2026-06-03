from django.test import TestCase
from django.utils import timezone
import datetime

from catalogue.models import Membre, Livre, Emprunt


class MembrePeutEmprunterTest(TestCase):
    """Test : un membre sans emprunt peut emprunter"""

    def test_nouveau_membre_peut_emprunter(self):
        membre = Membre.objects.create(nom="Dupont", prenom="Jean")
        self.assertTrue(membre.peut_emprunter())


class MembreBloqueTest(TestCase):
    """Test : un membre avec un emprunt en retard est bloqué"""

    def test_membre_bloque_si_retard(self):
        membre = Membre.objects.create(nom="Martin", prenom="Paul")
        livre = Livre.objects.create(nom="Python avancé", auteur="Guido")

        # On crée un emprunt daté d'il y a 2 semaines (donc en retard)
        Emprunt.objects.create(
            membre=membre,
            media_type="livre",
            media_id=livre.id,
            date_emprunt=timezone.now() - datetime.timedelta(weeks=2)
        )

        self.assertTrue(membre.est_bloque())
        self.assertFalse(membre.peut_emprunter())


class MembreMaxEmpruntsTest(TestCase):
    """Test : un membre ne peut pas avoir plus de 3 emprunts"""

    def test_membre_bloque_apres_3_emprunts(self):
        membre = Membre.objects.create(nom="Durand", prenom="Marie")

        # On crée 3 emprunts actifs
        for i in range(3):
            livre = Livre.objects.create(nom=f"Livre {i}", auteur="Auteur")
            Emprunt.objects.create(
                membre=membre,
                media_type="livre",
                media_id=livre.id
            )

        self.assertFalse(membre.peut_emprunter())

    def test_membre_peut_emprunter_apres_retour(self):
        membre = Membre.objects.create(nom="Durand", prenom="Marie")

        # On crée 3 emprunts puis on en retourne un
        emprunts = []
        for i in range(3):
            livre = Livre.objects.create(nom=f"Livre {i}", auteur="Auteur")
            e = Emprunt.objects.create(
                membre=membre,
                media_type="livre",
                media_id=livre.id
            )
            emprunts.append(e)

        # Retour d'un emprunt
        emprunts[0].date_retour = timezone.now()
        emprunts[0].save()

        self.assertTrue(membre.peut_emprunter())