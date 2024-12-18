from index.forms.form_fieldtypes import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from profileuseraccount.models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kies een gebruikersnaam', 'label': 'Gebruikersnaam'}),
        max_length=16,
        error_messages={'required': 'Kies een gebruikersnaam'})
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Persoonlijk emailadres'}),
        error_messages={'required': 'Vul een geldig email adres in!'}, max_length=254)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kies een wachtwoord'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Herhaal wachtwoord'}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Voornaam'}),
                                 max_length=100, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achternaam'}),
                                max_length=100)
    jobtitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Functie'}),
                               max_length=100, required=False)
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobiel telefoonnummer'}), max_length=12)
    company = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bedrijfsnaam'}), max_length=150,
        required=True)
    street_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straat en huisnummer'}),
        max_length=254)
    tel_general = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Algemeen telefoonnummer'}),
        max_length=30, required=False)

    e_mail_general = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Algemeen emailadres'}),
        max_length=254, required=False)

    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
                                  max_length=7, )
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plaats'}),
                           max_length=30)

    conditions_approved = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'kt-checkbox', 'type': 'checkbox'}),
        required=True,
        error_messages={
            'required': 'Vink dit vakje aan. Om deel te nemen aan het PrintDataPlatform moet u akkoord zijn met onze '
                        'spelregels'}, )
    gender = char_field_100_false
    linkedin_url = url_field_false
    company_url = url_field_false
    country_code = char_field_100_false
    producer_application = boolean_field

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'producer', 'member', 'jobtitle', 'company', 'tel_general', 'mobile_number', 'e_mail_general',
                  'street_number', 'postal_code', 'city', 'country_code', 'linkedin_url', 'company_url',
                  'conditions_approved', 'producer_application', 'gender'
                  )


class UserProfileUpdateForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Persoonlijk emailadres'}),
        error_messages={'required': 'Vul een geldig email adres in!'})

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uw voornaam'}),
                                 max_length=30, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uw achternaam'}),
                                max_length=30)
    jobtitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uw functie'}),
                               max_length=20, required=False)
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobiel telefoonnummer'}), max_length=12)

    linkedin_url = url_field_false

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'jobtitle', 'mobile_number', 'linkedin_url')


class CoWorkerUserProfileCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kies een gebruikersnaam', 'label': 'Gebruikersnaam'}),
        max_length=16,
        error_messages={'required': 'Please choose a star rating'})
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Voornaam'}),
                                 max_length=30, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achternaam'}),
                                max_length=30)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Vul een geldig emailadres is'}),
        error_messages={'required': 'Please let us know what to call you!'})
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kies een wachtwoord'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Herhaal het wachtwoord'}))

    jobtitle = char_field_200_false
    mobile_number = char_field_100_false
    gender = char_field_100_false

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'mobile_number', 'jobtitle', 'gender'
                  )
