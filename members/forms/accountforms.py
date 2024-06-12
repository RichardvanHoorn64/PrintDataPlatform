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
    # country_code = integer_field_notreq

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'mobile_number', 'email', 'jobtitle', 'linkedin_url'
            , 'company', 'tel_general', 'e_mail_general',
            'street_number', 'postal_code', 'city', 'linkedin_url', 'company_url')


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
    # country_code = integer_field_notreq

    class Meta:
        model = Members
        fields = ('company', 'tel_general', 'e_mail_general',
                  'street_number', 'postal_code', 'city', 'linkedin_url', 'company_url')
