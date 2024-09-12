from index.forms.form_fieldtypes import *
from profileuseraccount.models import Members, Producers


class MemberUpdateForm(forms.ModelForm):
    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    url = url_field_false
    linkedin_url = url_field_false

    class Meta:
        model = Members
        fields = ('company', 'tel_general', 'e_mail_general', 'street_number', 'postal_code', 'city',
                  'url', 'linkedin_url')


class ProducerCommunicationForm(forms.ModelForm):
    e_mail_rfq = char_field_100_false
    e_mail_offers = char_field_100_false
    e_mail_orders= char_field_100_false

    class Meta:
        model = Producers
        fields = ('e_mail_rfq', 'e_mail_offers', 'e_mail_orders',)
