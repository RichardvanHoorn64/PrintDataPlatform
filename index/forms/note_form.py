from methods.models import Notes
from index.forms.form_fieldtypes import *


class NoteForm(forms.ModelForm):
    client_id = integer_field_notreq
    member_id = integer_field_notreq
    producer_id = integer_field_notreq
    printproject_id = integer_field_notreq
    offer_id = integer_field_notreq
    order_id = integer_field_notreq
    note = char_field_2500_req

    class Meta:
        model = Notes
        fields = (
            'client_id', 'member_id', 'producer_id', 'printproject_id', 'offer_id', 'order_id', 'note')
