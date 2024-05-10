from index.forms.form_fieldtypes import *
from printprojects.models import MemberProducerMatch


class APImanagerForm(forms.ModelForm):
    api = boolean_field
    producerclient_id = char_field_100_false
    api_password = char_field_100_false
    api_username = char_field_200_false

    class Meta:
        model = MemberProducerMatch
        fields = ('api', 'producerclient_id', 'api_password', 'api_username',)
