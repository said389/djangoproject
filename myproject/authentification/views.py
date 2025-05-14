from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Driver, Navire  # Ajoutez Navire
from django.http import JsonResponse
import json
from django.utils import timezone

# Fonction de connexion (inchangée)
def connexion(request):
    if request.method == "POST":
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=mot_de_passe)

            if user is not None:
                login(request, user)
                return redirect('chef_escale')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except User.DoesNotExist:
            messages.error(request, "L'adresse email n'existe pas.")

    return render(request, 'connexion.html', {'message': messages.get_messages(request)})

# Vue chef_escale modifiée pour inclure les navires
@login_required
def chef_escale(request):
    # Filtrer par statut si paramètre présent
    statut = request.GET.get('statut')
    if statut:
        navires = Navire.objects.filter(statut=statut).order_by('-heure_arrivee')
    else:
        navires = Navire.objects.all().order_by('-heure_arrivee')
    
    # Calcul des statistiques
    total_navires = Navire.objects.count()
    navires_actifs = Navire.get_navires_actifs().count()
    postes_occupes = Navire.postes_occupes()
    
    context = {
        'navires': navires,
        'postes_occupes': postes_occupes,
        'now': timezone.now(),
        'total_navires': total_navires,
        'navires_actifs': navires_actifs,
        'statut_filter': statut
    }
    return render(request, 'chef_escale.html', context)

from django.shortcuts import get_object_or_404
from .forms import NavireForm  # Vous devrez créer ce formulaire

@login_required
def detail_navire(request, navire_id):
    navire = get_object_or_404(Navire, id=navire_id)
    return render(request, 'detail_navire.html', {'navire': navire})

@login_required
def modifier_navire(request, navire_id):
    navire = get_object_or_404(Navire, id=navire_id)
    
    if request.method == 'POST':
        form = NavireForm(request.POST, instance=navire)
        if form.is_valid():
            form.save()
            messages.success(request, "Navire modifié avec succès!")
            return redirect('detail_navire', navire_id=navire.id)
    else:
        form = NavireForm(instance=navire)
    
    return render(request, 'modifier_navire.html', {'form': form, 'navire': navire})

@login_required
def supprimer_navire(request, navire_id):
    navire = get_object_or_404(Navire, id=navire_id)
    
    if request.method == 'POST':
        navire.delete()
        messages.success(request, "Navire supprimé avec succès!")
        return redirect('chef_escale')
    
    return render(request, 'supprimer_navire.html', {'navire': navire})

# Vue ajout_navire modifiée pour gérer l'enregistrement
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Navire, TypeMarchandise
import logging


logger = logging.getLogger(__name__)

@login_required
def ajout_navire(request):
    types_marchandises = TypeMarchandise.objects.all().order_by('libelle')
    
    if request.method == 'POST':
        try:
            required_fields = [
                'nom_navire', 'imo_number', 'operation-type',
                'origin-port', 'berth', 'arrival-time',
                'stay-duration', 'departure-time', 'cargo-type'
            ]
            
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f"Le champ {field} est obligatoire")
            
            heure_arrivee = timezone.make_aware(
                timezone.datetime.strptime(
                    request.POST.get('arrival-time'), '%Y-%m-%dT%H:%M'
                )
            )
            
            heure_depart = timezone.make_aware(
                timezone.datetime.strptime(
                    request.POST.get('departure-time'), '%Y-%m-%dT%H:%M'
                )
            )
            
            if heure_arrivee >= heure_depart:
                raise ValueError("La date d'arrivée doit être avant la date de départ")
            
            imo_number = request.POST.get('imo_number')
            if not imo_number.isdigit() or len(imo_number) != 7:
                raise ValueError("Le numéro IMO doit contenir exactement 7 chiffres")
            
            type_marchandise = TypeMarchandise.objects.get(
                code=request.POST.get('cargo-type')
            )
            
            poste = request.POST.get('berth')
            if Navire.objects.filter(
                poste=poste,
                heure_arrivee__lte=heure_depart,
                heure_depart__gte=heure_arrivee
            ).exists():
                raise ValueError(f"Le poste {poste} est déjà occupé pendant cette période")
            
            # Création du navire
            navire = Navire(
                nom=request.POST.get('nom_navire'),
                imo=imo_number,
                type_operation=request.POST.get('operation-type'),
                port_origine=request.POST.get('origin-port'),
                poste=poste,
                heure_arrivee=heure_arrivee,
                duree_sejour=request.POST.get('stay-duration'),
                heure_depart=heure_depart,
                type_marchandise=type_marchandise.code,
                chef_escale=request.user,
                statut='En attente'
            )
            
            navire.save()
            
            # Affection automatique des engins
            try:
                # Récupérer les engins compatibles avec le type de marchandise
                engins_compatibles = Engin.objects.filter(
                    enginmarchandise__type_marchandise=type_marchandise,
                    statut='disponible'
                ).distinct()
                
                # Affecter tous les engins disponibles (ou adapter selon vos besoins)
                for engin in engins_compatibles:
                    AffectationEngin.objects.create(
                        navire=navire,
                        engin=engin,
                        date_debut=timezone.now()
                    )
                    engin.statut = 'occupe'
                    engin.save()
                
                messages.success(
                    request, 
                    f"Navire ajouté avec succès. {engins_compatibles.count()} engins affectés automatiquement."
                )
                
            except Exception as e:
                messages.warning(
                    request, 
                    f"Navire ajouté mais erreur lors de l'affectation des engins: {str(e)}"
                )
                logger.error(f"Erreur affectation engins: {str(e)}", exc_info=True)
            
            # Redirection vers la page de détail du navire ou liste des navires
                return redirect('affecter_engins', navire_id=navire.id)
            
        except TypeMarchandise.DoesNotExist:
            messages.error(request, "Type de marchandise invalide")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement: {str(e)}")
            logger.error(f"Erreur ajout navire: {str(e)}", exc_info=True)
    
    context = {
        'types_marchandises': types_marchandises,
    }
    return render(request, 'ajout_navire.html', context)

def page_affectation(request, navire_id):
    navire = get_object_or_404(Navire, pk=navire_id)
    form = AffectationForm()
    
    # Pré-calcul des engins disponibles
    type_marchandise = TypeMarchandise.objects.get(code=navire.type_marchandise)
    engins_disponibles = Engin.objects.filter(
        enginmarchandise__type_marchandise=type_marchandise,
        statut='disponible'
    ).count()
    
    context = {
        'navire': navire,
        'form': form,
        'engins_disponibles': engins_disponibles,
    }
    return render(request, 'page_affectation.html', context)

def affecter_engins(request, navire_id):
    navire = get_object_or_404(Navire, pk=navire_id)
    
    if request.method == 'POST':
        form = AffectationForm(request.POST)
        if form.is_valid():
            nombre_engins = form.cleaned_data['nombre_engins']
            
            # Récupération des engins compatibles
            type_marchandise = TypeMarchandise.objects.get(code=navire.type_marchandise)
            engins = Engin.objects.filter(
                enginmarchandise__type_marchandise=type_marchandise,
                statut='disponible'
            )[:nombre_engins]
            
            # Affectation des engins
            for engin in engins:
                AffectationEngin.objects.create(
                    navire=navire,
                    engin=engin
                )
                engin.statut = 'occupe'
                engin.save()
            
            messages.success(
                request, 
                f"Navire ajouté avec succès. {engins.count()} engins affectés automatiquement."
            )
            return redirect('detail_navire', navire_id=navire.id)
    
    return redirect('page_affectation', navire_id=navire.id)


def navires_actifs(request):
    navires = Navire.get_navires_actifs()
    return JsonResponse(list(navires), safe=False)

def check_poste_disponible(request):
    poste = request.GET.get('poste')
    heure_arrivee = request.GET.get('arrival')
    heure_depart = request.GET.get('departure')
    
    disponible = Navire.check_poste_disponible(poste, heure_arrivee, heure_depart)
    return JsonResponse({'disponible': disponible})

# Les autres vues restent inchangées
def gestion_absences(request):
    drivers = Driver.objects.all()
    return render(request, 'gestion_absences.html', {'drivers': drivers})

def absence_management(request):
    return render(request, 'absence-management.html')

def index(request):
    return render(request, 'index.html')

def daily_shifts(request):
    return render(request, 'daily-shifts.html')



from django.contrib.auth.models import User
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render
from .models import Driver, Engin
import json



def add_driver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            supervisor_user = User.objects.get(id=data['supervisorId'])
            
            driver = Driver.objects.create(
                firstname=data['firstname'],
                lastname=data['lastname'],
                matricule=data['matricule'],
                phone=data['phone'],
                email=data.get('email', ''),
                CIN=data.get('CIN', ''),
                shiftPeriod=data['shiftPeriod'],
                supervisor=supervisor_user.get_full_name() or supervisor_user.username,
                equipment=data['equipment'],  # Liste des types d'engins sélectionnés
                address=data.get('address', ''),
                birthdate=data.get('birthdate') or None,
                joinDate=data['joinDate']
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Récupère tous les types d'engins distincts
    types_engins = Engin.objects.values_list(
        'type_engin', flat=True
    ).distinct().order_by('type_engin')
    
    chefs_escale = User.objects.filter(is_staff=True).annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'))
    )
    
    return render(request, 'add-driver.html', {
        'chefs_escale': chefs_escale,
        'supervisors': User.objects.filter(is_staff=True),
        'types_engins': types_engins  # Liste des types d'engins uniques
    })

def api_drivers(request):
    drivers = Driver.objects.all().values(
        'id', 'firstname', 'lastname', 'matricule', 'phone',
        'shiftPeriod', 'supervisor', 'equipment'
    )
    return JsonResponse({'drivers': list(drivers)})

def dashboard(request):
    return render(request, 'dashboard.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Driver  # Assurez-vous que votre modèle Driver existe
import json

def update_driver(request, driver_id):
    if request.method == 'POST':
        try:
            driver = get_object_or_404(Driver, id=driver_id)
            
            # Traitement des données du formulaire
            driver.firstname = request.POST.get('firstname')
            driver.lastname = request.POST.get('lastname')
            driver.matricule = request.POST.get('matricule')
            driver.phone = request.POST.get('phone')
            driver.email = request.POST.get('email', '')
            driver.CIN = request.POST.get('CIN', '')
            driver.shiftPeriod = request.POST.get('shiftPeriod')
            driver.supervisor = request.POST.get('supervisor')
            driver.address = request.POST.get('address', '')
            driver.birthdate = request.POST.get('birthdate', None)
            driver.joinDate = request.POST.get('joinDate')
            
            # Traitement des équipements (checkboxes)
            equipment = json.loads(request.POST.get('equipment', '[]'))
            driver.equipment = equipment
            
            driver.save()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def delete_driver(request, driver_id):
    if request.method == 'POST':
        try:
            driver = get_object_or_404(Driver, id=driver_id)
            driver.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


from django.core import serializers

def api_drivers(request):
    drivers = Driver.objects.all()
    data = {
        'drivers': [
            {
                'id': driver.id,
                'firstname': driver.firstname,
                'lastname': driver.lastname,
                'matricule': driver.matricule,
                'phone': driver.phone,
                'email': driver.email,
                'CIN': driver.CIN,
                'shiftPeriod': driver.shiftPeriod,
                'supervisor': driver.supervisor,
                'equipment': driver.equipment,
                'address': driver.address,
                'birthdate': driver.birthdate,
                'joinDate': driver.joinDate,
            }
            for driver in drivers
        ]
    }
    return JsonResponse(data)

def api_driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    data = {
        'id': driver.id,
        'firstname': driver.firstname,
        'lastname': driver.lastname,
        'matricule': driver.matricule,
        'phone': driver.phone,
        'email': driver.email,
        'CIN': driver.CIN,
        'shiftPeriod': driver.shiftPeriod,
        'supervisor': driver.supervisor,
        'equipment': driver.equipment,
        'address': driver.address,
        'birthdate': driver.birthdate,
        'joinDate': driver.joinDate,
    }
    return JsonResponse(data)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Engin
from .forms import EnginForm
from django.contrib import messages


def gestion_engins(request):
    engins = Engin.objects.all()
    return render(request, 'DT.html', {
        'engins': engins,
        'show_add_tab': False  # On affiche la liste par défaut
    })

def ajouter_engin(request):
    if request.method == 'POST':
        form = EnginForm(request.POST)
        if form.is_valid():
            engin = form.save(commit=False)
            engin.created_by = request.user
            engin.save()
            messages.success(request, 'Engin ajouté avec succès!')
            return redirect('gestion_engins')
    else:
        form = EnginForm()
    
    return render(request, 'DT.html', {
        'form': form,
        'engins': Engin.objects.all(),  # Nécessaire pour afficher le tableau
        'show_add_tab': True  # Force l'affichage du formulaire d'ajout
    })


def modifier_engin(request, pk):
    engin = get_object_or_404(Engin, pk=pk)
    if request.method == 'POST':
        form = EnginForm(request.POST, instance=engin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Engin modifié avec succès!')
            return redirect('gestion_engins')
    else:
        form = EnginForm(instance=engin)
    
    return render(request, 'DT.html', {
        'form': form,
        'engins': Engin.objects.all(),
        'show_add_tab': True  # Affiche le formulaire de modification
    })

def supprimer_engin(request, pk):
    engin = get_object_or_404(Engin, pk=pk)
    if request.method == 'POST':
        engin.delete()
        messages.success(request, 'Engin supprimé avec succès!')
        return redirect('gestion_engins')
    
    return render(request, 'confirm_delete.html', {'engin': engin})

@login_required
def details_engin(request, pk):
    engin = get_object_or_404(Engin, pk=pk)
    return render(request, 'details_engin.html', {'engin': engin})




def engin_details_view(request):
    # Récupère tous les engins triés par matricule
    engins = Engin.objects.all().order_by('matricule')
    return render(request, 'engin_details_view.html', {'engins': engins})




from django.contrib.auth.decorators import login_required

@login_required
def conducteurs_par_chef(request):
    # Si l'utilisateur est un chef d'escale, ne montre que ses conducteurs
    if request.user.is_staff:
        conducteurs = Driver.objects.filter(supervisor=request.user)
    # Si c'est un admin, montre tous les conducteurs groupés par chef
    else:
        conducteurs = Driver.objects.all().order_by('supervisor__last_name')
    
    return render(request, 'conducteurs.html', {
        'conducteurs': conducteurs,
        'is_chef': request.user.is_staff
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Navire, Engin, AffectationEngin, TypeMarchandise

def affecter_engins(request, navire_id):
    # Récupérer le navire
    navire = get_object_or_404(Navire, pk=navire_id)
    
    # Récupérer le type de marchandise du navire
    try:
        type_marchandise = TypeMarchandise.objects.get(code=navire.type_marchandise)
    except TypeMarchandise.DoesNotExist:
        messages.error(request, "Type de marchandise non trouvé")
        return redirect('detail_navire', navire_id=navire.id)
    
    # Récupérer les engins compatibles et disponibles
    engins_compatibles = Engin.objects.filter(
        enginmarchandise__type_marchandise=type_marchandise,
        statut='disponible'
    ).distinct()
    
    # Récupérer les affectations existantes
    affectations = AffectationEngin.objects.filter(navire=navire)
    
    if request.method == 'POST':
        # Gérer l'affectation manuelle
        if 'engin_id' in request.POST:
            engin_id = request.POST.get('engin_id')
            try:
                engin = Engin.objects.get(pk=engin_id, statut='disponible')
                
                # Créer l'affectation
                AffectationEngin.objects.create(
                    navire=navire,
                    engin=engin,
                    date_debut=timezone.now()
                )
                
                # Mettre à jour le statut de l'engin
                engin.statut = 'occupe'
                engin.save()
                
                messages.success(request, f"Engin {engin.matricule} affecté avec succès")
            except Engin.DoesNotExist:
                messages.error(request, "Engin non disponible")
        
        # Gérer la libération d'engin
        elif 'liberer_id' in request.POST:
            affectation_id = request.POST.get('liberer_id')
            try:
                affectation = AffectationEngin.objects.get(pk=affectation_id)
                engin = affectation.engin
                
                # Libérer l'engin
                engin.statut = 'disponible'
                engin.save()
                affectation.delete()
                
                messages.success(request, f"Engin {engin.matricule} libéré avec succès")
            except AffectationEngin.DoesNotExist:
                messages.error(request, "Affectation non trouvée")
        
        return redirect('affecter_engins', navire_id=navire.id)
    
    context = {
        'navire': navire,
        'engins_compatibles': engins_compatibles,
        'affectations': affectations,
        'type_marchandise': type_marchandise,
    }
    
    return render(request, 'affecter_engins.html', context)






    # views.py
def page_affectation(request, navire_id):
    navire = get_object_or_404(Navire, pk=navire_id)
    
    # Récupérer le type de marchandise
    try:
        type_marchandise = TypeMarchandise.objects.get(code=navire.type_marchandise)
    except TypeMarchandise.DoesNotExist:
        messages.error(request, "Type de marchandise non configuré")
        return redirect('detail_navire', navire_id=navire.id)
    
    # Engins disponibles
    engins_disponibles = Engin.objects.filter(
        enginmarchandise__type_marchandise=type_marchandise,
        statut='disponible'
    )
    
    context = {
        'navire': navire,
        'engins_disponibles': engins_disponibles,
        'type_marchandise': type_marchandise,
    }
    
    return render(request, 'affecter_engins.html', context)