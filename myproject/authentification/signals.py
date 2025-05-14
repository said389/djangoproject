from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AffectationAuto, Engin

@receiver(post_save, sender=AffectationAuto)
def update_engin_status(sender, instance, created, **kwargs):
    if created:
        # Marquer l'engin comme occupé
        instance.engin.statut = 'occupe'
        instance.engin.save()
        
        # Vous pouvez aussi ajouter ici la génération de la feuille de service