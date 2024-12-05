from index.forms.form_fieldtypes import *
from producers.models import ProducerProductOfferings


class ProducerProductOfferingForm(forms.ModelForm):
    min_product_size = integer_field_notreq
    max_product_size = integer_field_notreq
    min_product_volume = integer_field_notreq
    max_product_volume = integer_field_notreq

    class Meta:
        model = ProducerProductOfferings
        fields = ('min_product_size', 'max_product_size', 'min_product_volume', 'max_product_volume')
