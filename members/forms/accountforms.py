from index.forms.form_fieldtypes import *
from profileuseraccount.models import *


class UserUpdateForm(forms.ModelForm):
    first_name = char_field_200_false
    last_name = char_field_200_false
    jobtitle = char_field_200_false
    mobile_number = char_field_200_false
    email = char_field_200_false

    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    url = url_field_false
    linkedin_url = url_field_false
    company_url = url_field_false
    country_code = char_field_100_false

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'mobile_number', 'email', 'jobtitle', 'linkedin_url'
            , 'company', 'tel_general', 'e_mail_general',
            'street_number', 'postal_code', 'city', 'linkedin_url', 'company_url', 'country_code')


class MemberUpdateForm(forms.ModelForm):
    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    url = url_field_false
    linkedin_url = url_field_false
    company_url = url_field_false
    country_code = char_field_100_false

    class Meta:
        model = Members
        fields = ('company', 'tel_general', 'e_mail_general',
                  'street_number', 'postal_code', 'city', 'linkedin_url', 'company_url')


class CreateProducerExclusiveMemberForm(forms.ModelForm):
    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    country_code = char_field_100_false

    class Meta:
        model = Members
        fields = ('company', 'tel_general', 'e_mail_general',
                  'street_number', 'postal_code', 'city', 'country_code')


class CreateNewExclusiveMemberContactForm(forms.ModelForm):
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

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name','jobtitle', 'mobile_number')
