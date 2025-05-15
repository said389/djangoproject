from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

class Navire(models.Model):
    TYPE_OPERATION = [
        ('import', 'Import'),
        ('export', 'Export'),
        ('transit', 'Transit'),
    ]

    TYPE_MARCHANDISE = [
        ('containers', 'Conteneurs'),
        ('bulk', 'Vrac'),
        ('general', 'Marchandises Générales'),
        ('vehicles', 'Véhicules'),
    ]

    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Accosté', 'Accosté'),
        ('En opération', 'En opération'),
        ('Terminé', 'Terminé'),
    ]

    POSTE_CHOICES = [
        ('1', 'Poste 1'),
        ('2', 'Poste 2'),
        ('3', 'Poste 3'),
        ('4', 'Poste 4'),
    ]

    nom = models.CharField(max_length=100)
    imo = models.CharField(max_length=7, unique=True)
    type_operation = models.CharField(max_length=10, choices=TYPE_OPERATION)
    port_origine = models.CharField(max_length=100)
    poste = models.CharField(max_length=10, choices=POSTE_CHOICES)
    heure_arrivee = models.DateTimeField()
    duree_sejour = models.IntegerField(help_text="Durée en heures")
    heure_depart = models.DateTimeField(blank=True, null=True)
    type_marchandise = models.CharField(max_length=20, choices=TYPE_MARCHANDISE)
    chef_escale = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-heure_arrivee']
        verbose_name = "Navire"
        verbose_name_plural = "Navires"

    def __str__(self):
        return f"{self.nom} (IMO: {self.imo})"

    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour calculer automatiquement l'heure de départ"""
        if not self.heure_depart and self.duree_sejour and self.heure_arrivee:
            self.heure_depart = self.heure_arrivee + timezone.timedelta(hours=self.duree_sejour)
        
        # Mise à jour automatique du statut
        if self.est_en_cours and self.statut != 'Accosté':
            self.statut = 'Accosté'
        elif not self.est_en_cours and self.statut == 'Accosté':
            self.statut = 'Terminé'
            
        super().save(*args, **kwargs)

    @property
    def est_en_cours(self):
        """Vérifie si le navire est actuellement au port"""
        now = timezone.now()
        return self.heure_arrivee <= now <= self.heure_depart

    @classmethod
    def postes_occupes(cls):
        """Retourne la liste des postes actuellement occupés"""
        now = timezone.now()
        return cls.objects.filter(
            Q(heure_arrivee__lte=now) & Q(heure_depart__gte=now)
        ).values_list('poste', flat=True)

    @classmethod
    def get_navires_actifs(cls):
        """Retourne les navires actuellement au port avec leurs postes"""
        now = timezone.now()
        return cls.objects.filter(
            Q(heure_arrivee__lte=now) & Q(heure_depart__gte=now)
        ).values('nom', 'poste')

    @classmethod
    def check_poste_disponible(cls, poste, heure_arrivee, heure_depart):
        """
        Vérifie si un poste est disponible pour une période donnée
        Retourne False si le poste est occupé, sinon True
        """
        conflits = cls.objects.filter(
            Q(poste=poste) &
            Q(heure_arrivee__lt=heure_depart) &
            Q(heure_depart__gt=heure_arrivee)
        ).exists()
        
        return not conflits
    
date_modification = models.DateTimeField(auto_now=True, null=True) 

class Driver(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Matin (6h - 14h)'),
        ('afternoon', 'Après-midi (14h - 22h)'),
        ('night', 'Nuit (22h - 6h)'),
    ]

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    CIN = models.CharField(max_length=20, blank=True, null=True)
    shiftPeriod = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    supervisor = models.CharField(max_length=100)
    equipment = models.JSONField(default=list)
    address = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    joinDate = models.DateField()

    is_flexible = models.BooleanField(default=False) 
    
    class Meta:
        db_table = 'authentification_driver'
        verbose_name = "Chauffeur"
        verbose_name_plural = "Chauffeurs"

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.matricule})"
    
    
    




from django.db import models
from django.contrib.auth.models import User

class Engin(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
        ('reserve', 'Réservé'),
    ]
    
    matricule = models.CharField(max_length=50, unique=True)
    type_engin = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee_fabrication = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    maintenance_info = models.TextField(blank=True, null=True)
    date_acquisition = models.DateField()
    kilometrage = models.DecimalField(max_digits=10, decimal_places=2)
    prochaine_maintenance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commentaires = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'engin' 
    
    def __str__(self):
        return f"{self.matricule} - {self.marque} {self.modele}"
    


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"



# models.py
class TypeMarchandise(models.Model):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libelle
    



class EnginMarchandise(models.Model):
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE)
    marchandise_type = models.CharField(max_length=20, choices=Navire.TYPE_MARCHANDISE)

    def __str__(self):
        return f"{self.engin.nom} - {self.marchandise_type}"


class FeuilleService(models.Model):
    navire = models.ForeignKey(Navire, on_delete=models.CASCADE)
    engins = models.ManyToManyField(Engin)
    drivers = models.ManyToManyField(Driver)
    date = models.DateField(auto_now_add=True)


    





