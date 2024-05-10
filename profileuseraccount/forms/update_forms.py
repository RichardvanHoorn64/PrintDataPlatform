from django import forms
from profileuseraccount.models import *


class UpdateKlantForm(forms.ModelForm):
    company = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'company'}), max_length=100)
    manager = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
                              max_length=50)
    telefoonnummer_algemeen = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefoonnummer'}), max_length=12,
        required=False)
    e_mail_algemeen = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Vul een geldig emailadres is'}),
        required=False)

    straat_huisnummer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straat en huisnummer'}), max_length=30,
        required=False)
    postcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
                               max_length=7, required=False)
    plaats = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plaats'}),
                             max_length=30, required=False)

    class Meta:
        model = Klanten
        fields = (
            'company', 'manager', 'telefoonnummer_algemeen', 'e_mail_algemeen',
            'straat_huisnummer', 'postcode', 'plaats',)


class UpdateProfielForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Functie'}),
                                 max_length=20, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Functie'}),
                                max_length=20, required=False)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Vul een geldig emailadres is'}),
        required=False)

    algemeen_telefoonnummer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Algemeen telefoonnummer'}),
        max_length=12, required=False)

    mobiel_telefoonnummer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobiel telefoonnummer'}), max_length=12,
        required=False)

    functie = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Functie'}),
                              max_length=20, required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'algemeen_telefoonnummer', 'mobiel_telefoonnummer', 'functie',)


class UpdateProducentForm(forms.ModelForm):
    company = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Producentnaam'}), max_length=100)

    productiemanager = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Productiemanager'}),
        max_length=50)
    telefoonnummer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefoonnummer'}), max_length=12)
    e_mail_algemeen = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Vul een geldig emailadres is'}),
        required=False)
    e_mail_orders = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Emailadres voor orderaanlevering'}),
        required=False)

    straat_huisnummer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straat en huisnummer'}), max_length=30,
        required=True)
    postcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
                               max_length=7, required=True)
    plaats = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plaats'}),
                             max_length=30, required=True)

    class Meta:
        model = Producenten
        fields = (
            'company', 'productiemanager', 'telefoonnummer', 'e_mail_algemeen',
            'straat_huisnummer', 'postcode', 'plaats', 'productiemanager', 'e_mail_orders')
