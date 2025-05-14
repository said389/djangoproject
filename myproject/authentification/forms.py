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



from django import forms
from .models import Navire, EnginMarchandise, AffectationEngin

class EnginMarchandiseForm(forms.ModelForm):
    class Meta:
        model = EnginMarchandise
        fields = ['engin', 'type_marchandise']
        widgets = {
            'engin': forms.Select(attrs={'class': 'form-control'}),
            'type_marchandise': forms.Select(attrs={'class': 'form-control'}),
        }

class AffectationEnginForm(forms.ModelForm):
    class Meta:
        model = AffectationEngin
        fields = ['engin', 'chauffeur']
        
    def __init__(self, *args, **kwargs):
        navire = kwargs.pop('navire', None)
        super().__init__(*args, **kwargs)
        
        if navire:
            # Filtrer les engins compatibles avec le navire
            self.fields['engin'].queryset = navire.get_engins_compatibles()



# forms.py
from django import forms

class AffectationForm(forms.Form):
    nombre_engins = forms.IntegerField(
        label="Nombre d'engins nécessaires",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le nombre d\'engins requis'
        })
    )