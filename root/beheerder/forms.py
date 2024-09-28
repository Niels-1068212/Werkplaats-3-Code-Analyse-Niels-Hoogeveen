from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from ervaringsdeskundige.models import User


class RegistratieFormulier(UserCreationForm):
    functie = forms.CharField(max_length=100,)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Voornaam',
            'autofocus': 'true'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Achternaam'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Gebruikersnaam'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'E-mailadres'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Wachtwoord'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Herhaal wachtwoord'
        })


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
