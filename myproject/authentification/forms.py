from django import forms
from .models import Navire

class NavireForm(forms.ModelForm):
    class Meta:
        model = Navire
        fields = '__all__'
        widgets = {
            'heure_arrivee': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'heure_depart': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        exclude = ['chef_escale']  # Exclure le champ chef_escale du formulaire


from django import forms
from .models import Engin
from django.contrib.auth.models import User

class EnginForm(forms.ModelForm):
    class Meta:
        model = Engin
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date_acquisition': forms.DateInput(attrs={'type': 'date'}),
            'maintenance_info': forms.Textarea(attrs={'rows': 3}),
            'commentaires': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'prochaine_maintenance' and field != 'commentaires' and field != 'maintenance_info':
                self.fields[field].required = True



