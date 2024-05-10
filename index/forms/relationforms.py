from index.forms.form_fieldtypes import *
from printprojects.models import *
from producers.models import ProducerContacts


class NewClientForm(forms.ModelForm):
    client = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    manager_first_name = char_field_200_false
    manager_last_name = char_field_200_false
    manager_jobtitle = char_field_200_false
    manager_mobile_number = char_field_100_false
    manager_e_mail = char_field_100_false
    # social media
    linkedin_url = url_field_false
    facebook_url = url_field_false

    class Meta:
        model = Clients
        fields = ('client', 'tel_general', 'e_mail_general', 'street_number', 'postal_code', 'city',
                  'manager_first_name', 'manager_last_name', 'manager_jobtitle', 'manager_mobile_number',
                  'manager_e_mail', 'linkedin_url', 'facebook_url',)


class NewClientContactForm(forms.ModelForm):
    first_name = char_field_200_true
    last_name = char_field_200_true
    e_mail_personal = char_field_100_false
    jobtitle = char_field_200_false
    mobile_number = char_field_100_false
    e_mail = char_field_100_false
    # social media
    linkedin_url = url_field_false
    facebook_url = url_field_false

    class Meta:
        model = ClientContacts
        fields = ('first_name', 'last_name', 'jobtitle', 'mobile_number', 'e_mail_personal',
                  'linkedin_url', 'facebook_url',)


class NewProducerForm(forms.ModelForm):
    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    manager_ = char_field_200_false

    manager_mobile_number = char_field_100_false
    manager_e_mail = char_field_100_false

    class Meta:
        model = Producers
        fields = ('company', 'tel_general', 'e_mail_general', 'street_number', 'postal_code', 'city',
                  'manager',
                  'manager_e_mail')


class NewProducerContactForm(forms.ModelForm):
    first_name = char_field_200_true
    last_name = char_field_200_true
    e_mail_personal = char_field_100_false
    jobtitle = char_field_200_false
    mobile_number = char_field_100_false
    e_mail = char_field_100_false
    # social media
    linkedin_url = url_field_false
    facebook_url = url_field_false

    class Meta:
        model = ProducerContacts
        fields = ('first_name', 'last_name', 'jobtitle', 'mobile_number', 'e_mail_personal',
                  'linkedin_url', 'facebook_url',)
