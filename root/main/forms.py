from django import forms
from .models import Beheerder

class BeheerderForm(forms.ModelForm):
    class Meta:
        model = Beheerder
        fields = ['email', 'username', 'password', 'voornaam', 'achternaam', 'functie', 'status']
        widgets = {
            'password': forms.PasswordInput(),
        }

