from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import gestion_engins, ajouter_engin, modifier_engin, supprimer_engin
from . import views



urlpatterns = [
    # Authentification
    path('connexion/', views.connexion, name='connexion'),
    path('chef_escale/', views.chef_escale, name='chef_escale'),
    path('ajout_navire/', views.ajout_navire, name='ajout_navire'),
    path('navire/<int:navire_id>/', views.detail_navire, name='detail_navire'),
    path('navire/<int:navire_id>/modifier/', views.modifier_navire, name='modifier_navire'),
    path('navire/<int:navire_id>/supprimer/', views.supprimer_navire, name='supprimer_navire'),
    path('gestion_absences/', views.gestion_absences, name='ajout_absence'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Pages de gestion
    path('absence-management/', views.absence_management, name='absence_management'),
    path('index/', views.index, name='index'),
    path('daily-shifts/', views.daily_shifts, name='daily_shifts'),
    path('add-driver/', views.add_driver, name='add_driver'),
    path('api/drivers/', views.api_drivers, name='api_drivers'),
     path('driver/<int:driver_id>/update/', views.update_driver, name='update_driver'),
    path('driver/<int:driver_id>/delete/', views.delete_driver, name='delete_driver'),
    path('api/drivers/', views.api_drivers, name='api_drivers'),
    path('api/drivers/<int:driver_id>/', views.api_driver_detail, name='api_driver_detail'),


     path('engins/', gestion_engins, name='gestion_engins'),
     path('', views.dashboard, name='accueil'),  # ou views.index selon ta logique
     path('engins/<int:pk>/', views.details_engin, name='details_engin'),
    path('engins/ajouter/', ajouter_engin, name='ajouter_engin'),
    path('engins/modifier/<int:pk>/', modifier_engin, name='modifier_engin'),
    path('engins/supprimer/<int:pk>/', supprimer_engin, name='confirm_delete'),

    path('engins/details/', views.engin_details_view, name='engin_details_view'),

     path('conducteurs/', views.conducteurs_par_chef, name='conducteurs'),


    path('navire/<int:navire_id>/affectation/', views.page_affectation, name='page_affectation'),
    path('navire/<int:navire_id>/affecter-engins/', views.affecter_engins, name='affecter_engins'), 
    
         
     path('dashboard/', views.dashboard, name='dashboard'),  # Ajoutez cette ligne
]

