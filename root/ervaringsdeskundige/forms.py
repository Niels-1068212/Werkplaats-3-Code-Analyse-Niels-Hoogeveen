from typing import Any
from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from main.models import Beperkingen, Toezichthouders


class RegisterForm(UserCreationForm):
    geboortedatum = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    beschikbaar_vanaf = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    beschikbaar_tot = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'postcode', 'geslacht','email', 'telefoonnummer', 'geboortedatum', 'gebruikte_hulpmiddelen',
                  'bijzonderheden', 'bijzonderheden_beschikbaarheid', 'username', 'voorkeur_benadering', 'beschikbaar_vanaf', 'beschikbaar_tot')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'aria-label': 'voornaam',  'autofocus': 'true'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Achternaam', })
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Gebruikersnaam'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'aria-label': 'E-mailadres'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Wachtwoord'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Wachtwoord herhalen'})
        self.fields['postcode'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Postcode'})
        self.fields['geslacht'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Geslacht'})
        self.fields['telefoonnummer'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Telefoonnummer'})
        self.fields['gebruikte_hulpmiddelen'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Gebruikte hulpmiddelen', 'style': "height: 100px; resize: none;",})
        self.fields['geboortedatum'].widget.attrs.update({'class': 'form-control','aria-label': 'Geboortedatum', 'type': "date", 'id': "geboortedatum", 'onchange': "ageChecker()"})
        self.fields['beschikbaar_vanaf'].widget.attrs.update({'class': 'form-control','aria-label': 'beschikbaar_vanaf', 'type': "date", 'id': "beschikbaar_vanaf"})
        self.fields['beschikbaar_tot'].widget.attrs.update({'class': 'form-control','aria-label': 'beschikbaar_tot', 'type': "date", 'id': "beschikbaar_tot"})
        self.fields['bijzonderheden'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Bijzonderheden', 'style': "height: 100px; resize: none;"})
        self.fields['bijzonderheden_beschikbaarheid'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Bijzonderheden beschikbaarheid', 'style': "height: 100px; resize: none;"})
        self.fields['voorkeur_benadering'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Voorkeur benadering', })


class BeperkingForm(forms.Form):
    beperkingen = forms.ModelMultipleChoiceField(queryset=Beperkingen.objects.all(), widget=forms.CheckboxSelectMultiple)


class ToezichthoudersForm(forms.ModelForm):
    voornaam_1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    achternaam_1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefoonnummer_1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    voornaam_2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    achternaam_2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    telefoonnummer_2 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    ervaringsdeskundige = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Toezichthouders
        fields = (
            'voornaam_1', 'achternaam_1', 'telefoonnummer_1',
            'voornaam_2', 'achternaam_2', 'telefoonnummer_2', 'ervaringsdeskundige'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voornaam_1'].widget.attrs.update({'class': 'form-control','aria-label': 'voornaam toezichthouder 1, vereist'})
        self.fields['achternaam_1'].widget.attrs.update({'class': 'form-control', 'aria-label': 'achternaam toezichthouder 1, vereist'})
        self.fields['telefoonnummer_1'].widget.attrs.update({'class': 'form-control', 'aria-label': 'telefoonnummer toezichthouder 1, vereist'})
        self.fields['voornaam_2'].widget.attrs.update({'class': 'form-control',  'aria-label': 'voornaam toezichthouder 2, niet vereist'})
        self.fields['achternaam_2'].widget.attrs.update({'class': 'form-control',  'aria-label': 'achternaam toezichthouder 2, niet vereist'})
        self.fields['telefoonnummer_2'].widget.attrs.update({'class': 'form-control',  'aria-label': 'telefoonnummer toezichthouder 2, niet vereist'})
        self.fields['ervaringsdeskundige'].widget.attrs.update({'class': 'form-control'})



class UserChangeForm(UserChangeForm):
    class Meta:
        model = User()
        fields = ['first_name', 'last_name', 'username', 'email']


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'aria-label': 'voornaam'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'aria-label': 'achternaam'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'aria-label': 'gebruikersnaam'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'aria-label': 'e-mail'})