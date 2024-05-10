from index.forms.form_fieldtypes import *
from offers.models import Offers


class OfferProducerForm(forms.ModelForm):
    offer = integer_field
    offer_1000extra = integer_field
    producer_contact = char_field_200_false
    producer_notes = char_field_2500_false
    producer_quote = char_field_200_false

    class Meta:
        model = Offers
        fields = ('offer', 'offer_1000extra', 'producer_contact', 'producer_notes', 'producer_quote',)


class OfferProducerFormAcces(forms.ModelForm):
    offer_key_test = integer_field

    class Meta:
        model = Offers
        fields = ('offer_key_test',)
