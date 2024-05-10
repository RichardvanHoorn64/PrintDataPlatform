from orders.models import Orders
from index.forms.form_fieldtypes import *


class OrdersForm(forms.ModelForm):
    ordernumber = char_field_200_false
    order_description = char_field_1000_false
    supplier_remarks = char_field_1000_false
    order_volume = integer_field_notreq
    order_value = decimal_field_notreq
    order_morecost = decimal_field_notreq
    order_remarks = char_field_1000_false
    delivery_date_request = date_field
    delivery_date_deliverd = date_field
    printfiles_available = date_field
    deliver_street_number = char_field_200_false
    deliver_postcode = char_field_100_false
    deliver_city = char_field_200_false
    deliver_company = char_field_200_false
    deliver_contactperson = char_field_200_false
    deliver_tel = char_field_100_false

    class Meta:
        model = Orders
        fields = (
            'ordernumber', 'order_description', 'supplier_remarks', 'order_volume', 'order_value', 'order_morecost',
            'order_remarks', 'delivery_date_request', 'delivery_date_deliverd', 'printfiles_available',
            'deliver_street_number', 'deliver_postcode', 'deliver_city', 'deliver_contactperson', 'deliver_tel',)
