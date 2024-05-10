from printprojects.models import PrintProjects
from index.forms.form_fieldtypes import *


class PrintProjectPriceUpdateForm(forms.ModelForm):
    salesprice = decimal_field_notreq
    salesprice_1000extra = decimal_field_notreq
    invoiceturnover = decimal_field_notreq

    class Meta:
        model = PrintProjects
        fields = (
            'salesprice', 'salesprice_1000extra', 'invoiceturnover'
        )
