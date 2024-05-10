from index.forms.form_fieldtypes import *
from profileuseraccount.models import Members


class MemberUpdateForm(forms.ModelForm):
    company = char_field_200_false
    tel_general = char_field_100_false
    e_mail_general = char_field_100_false
    street_number = char_field_200_false
    postal_code = char_field_100_false
    city = char_field_200_false
    url = url_field_false
    linkedin_url = url_field_false
    facebook_url = url_field_false

    class Meta:
        model = Members
        fields = ('company', 'tel_general', 'e_mail_general', 'street_number', 'postal_code', 'city',
                  'url', 'linkedin_url', 'facebook_url',)
