from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Driver, Navire  # Ajoutez Navire
from django.http import JsonResponse
import json
from django.utils import timezone
from django.db import connection


def connexion(request):
    if request.method == "POST":
        role = request.POST.get('role')

        if role == 'chef':
            email = request.POST.get('email')
            mot_de_passe = request.POST.get('mot_de_passe')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=mot_de_passe)

                if user is not None:
                    login(request, user)
                    request.session['role'] = 'chef'
                    return redirect('chef_escale') 
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except User.DoesNotExist:
                messages.error(request, "L'adresse email n'existe pas.")

        elif role == 'conducteur':
            matricule = request.POST.get('matricule')
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT firstname, lastname FROM authentification_driver WHERE matricule = %s",
                    [matricule]
                )
                row = cursor.fetchone()

            if row:
                full_name = f"{row[0]} {row[1]}"
                request.session['utilisateur'] = full_name
                request.session['role'] = 'conducteur'
                return redirect('conducteur_home') 
            else:
                messages.error(request, "Matricule incorrect.")

        else:
            messages.error(request, "Veuillez choisir un rôle.")

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
            # Validation des champs (votre code existant)
            required_fields = [
                'nom_navire', 'imo_number', 'operation-type',
                'origin-port', 'berth', 'arrival-time',
                'stay-duration', 'departure-time', 'cargo-type'
            ]
            
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f"Le champ {field} est obligatoire")
            
            # Conversion des dates/heures
            heure_arrivee = timezone.make_aware(
                timezone.datetime.strptime(
                    request.POST.get('arrival-time'), 
                    '%Y-%m-%dT%H:%M'
                )
            )
            
            heure_depart = timezone.make_aware(
                timezone.datetime.strptime(
                    request.POST.get('departure-time'), 
                    '%Y-%m-%dT%H:%M'
                )
            )
            
            # Vérifications (votre code existant)
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
            
            # Création du navire (sans sauvegarde immédiate)
            navire = Navire(
                nom=request.POST.get('nom_navire'),
                imo=imo_number,
                type_operation=request.POST.get('operation-type'),
                port_origine=request.POST.get('origin-port'),
                poste=poste,
                heure_arrivee=heure_arrivee,
                duree_sejour=request.POST.get('stay-duration'),
                heure_depart=heure_depart,
                type_marchandise=type_marchandise.code,  # Utilisez code au lieu de l'objet
                chef_escale=request.user,
                statut='En attente'
            )
            
            # Sauvegarde temporaire pour obtenir un ID
            navire.save()
            
            # Optionnel: Redirection vers une autre page ou afficher un message de confirmation
            messages.success(request, "Le navire a été ajouté avec succès!")
            redirect('dashboard')  
            
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




def navires_actifs(request):
    navires = Navire.get_navires_actifs()
    return JsonResponse(list(navires), safe=False)

def check_poste_disponible(request):
    poste = request.GET.get('poste')
    heure_arrivee = request.GET.get('arrival')
    heure_depart = request.GET.get('departure')
    
    disponible = Navire.check_poste_disponible(poste, heure_arrivee, heure_depart)
    return JsonResponse({'disponible': disponible})

from .models import AbsenceRequest
from django.core.files.storage import FileSystemStorage

def gestion_absences(request):
    drivers = Driver.objects.all()

    if request.method == 'POST':
        matricule = request.POST.get('conducteur_matricule')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        motif = request.POST.get('motif')
        commentaires = request.POST.get('commentaires')
        justificatif = request.FILES.get('justificatif')

        AbsenceRequest.objects.create(
            conducteur_matricule=matricule,
            date_debut=date_debut,
            date_fin=date_fin,
            motif=motif,
            commentaires=commentaires,
            justificatif=justificatif
        )

        message = "Demande envoyée avec succès."
        return render(request, 'gestion_absences.html', {'drivers': drivers, 'message': message})

    return render(request, 'gestion_absences.html', {'drivers': drivers})


def absence_management(request):
    if request.method == 'POST' and 'action' in request.POST:
        try:
            absence = AbsenceRequest.objects.get(id=request.POST['id'])
            absence.statut = request.POST['action']
            absence.save()
            messages.success(request, f"Demande {absence.get_statut_display()}")
        except AbsenceRequest.DoesNotExist:
            messages.error(request, "Demande introuvable")
    
    absences = AbsenceRequest.objects.all().order_by('-date_debut')
    return render(request, 'absence-management.html', {'absences': absences})


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



from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Navire, Engin, EnginMarchandise, Driver, AffectationDriver

def affecter_engins(request):
    navires = Navire.objects.filter(chef_escale=request.user)
    selected_navire_id = request.GET.get('navire_id') or request.POST.get('navire_id')
    engins = []
    marchandise = None
    chauffeurs = []
    
    if selected_navire_id:
        navire = get_object_or_404(Navire, id=selected_navire_id)
        marchandise = navire.type_marchandise
        
        engins_ids = EnginMarchandise.objects.filter(
            marchandise_type=marchandise
        ).values_list('engin_id', flat=True)
        
        engins = Engin.objects.filter(
            id__in=engins_ids,
            statut='disponible'
        )
        
    if request.method == 'POST':
        nombre_engins = int(request.POST.get('nombre_engins', 0))
        if nombre_engins <= 0:
            messages.error(request, "Veuillez saisir un nombre valide d'engins.")
        else:
            engins_disponibles = engins[:nombre_engins]
            if engins_disponibles.count() < nombre_engins:
                messages.error(request, f"Seulement {engins_disponibles.count()} engin(s) disponible(s).")
            else:
                # Affecter les engins
                for engin in engins_disponibles:
                    engin.statut = 'occupé'
                    engin.save()
                messages.success(request, f"{nombre_engins} engin(s) affecté(s).")
                
                # Récupérer les types des engins affectés (en minuscule)
                types_engins_affectes = [engin.type_engin.lower() for engin in engins_disponibles]

                # Trouver chauffeurs compatibles
                for driver in Driver.objects.all():
                    equip_list_lower = [e.lower() for e in driver.equipment]
                    if any(t in equip_list_lower for t in types_engins_affectes):
                        chauffeurs.append(driver)
                
                if chauffeurs:
                    chauffeur_affecte = chauffeurs[0]
                    AffectationDriver.objects.create(
                        chauffeur=chauffeur_affecte,
                        navire=navire
                    )
                    messages.success(request, f"Chauffeur {chauffeur_affecte.firstname} affecté au navire.")
                else:
                    messages.warning(request, "Aucun chauffeur compatible trouvé.")

    return render(request, 'affecter_engins.html', {
        'navires': navires,
        'selected_navire_id': selected_navire_id,
        'marchandise': marchandise,
        'engins': engins,
        'chauffeurs': chauffeurs,
    })




from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Navire, AffectationDriver, Engin, FeuilleService
from xhtml2pdf import pisa
import io

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Erreur lors de la génération du PDF")


def feuille_service(request):
    navire_id = request.GET.get('navire_id')
    navire = get_object_or_404(Navire, id=navire_id)

    engins = Engin.objects.filter(statut='occupé')
    affectation = AffectationDriver.objects.filter(navire=navire).first()
    chauffeur = affectation.chauffeur if affectation else None

    publication_succes = False

    if request.method == 'POST' and request.POST.get('publish'):
        feuille = FeuilleService.objects.create(navire=navire)
        feuille.engins.set(engins)
        if chauffeur:
            feuille.drivers.set([chauffeur])
        feuille.save()
        publication_succes = True

    context = {
        'navire': navire,
        'engins': engins,
        'chauffeur': chauffeur,
        'user': request.user,
        'publication_succes': publication_succes,
    }

    # Si "pdf" est demandé via GET
    if request.GET.get('pdf'):
        return render_to_pdf('feuille_service.html', context)

    return render(request, 'feuille_service.html', context)




def daily_shifts(request):
    # On affiche seulement les feuilles publiées (FeuilleService)
    feuilles = FeuilleService.objects.all().order_by('-date')

    context = {
        'feuilles': feuilles,
        'user': request.user,
    }

    return render(request, 'daily-shifts.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def supprimer_feuille(request, feuille_id):
    try:
        feuille = FeuilleService.objects.get(id=feuille_id)
        feuille.delete()
        return JsonResponse({'success': True})
    except FeuilleService.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Feuille non trouvée'}, status=404)
    



def conducteur_home(request):
    nom = request.session.get('utilisateur', 'Conducteur')

    absences = AbsenceRequest.objects.filter(conducteur_matricule=nom)
    return render(request, 'conducteur_home.html', {'nom': nom, 'absences': absences})

