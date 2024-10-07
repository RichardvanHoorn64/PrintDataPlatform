from printprojects.models import PrintProjects, MemberProducerMatch
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


class MemberProducerPricingForm(forms.ModelForm):
    perc_salesallowance_1 = decimal_field_notreq_negative
    perc_salesallowance_2 = decimal_field_notreq_negative
    perc_salesallowance_3 = decimal_field_notreq_negative
    perc_salesallowance_4 = decimal_field_notreq_negative
    perc_salesallowance_5 = decimal_field_notreq_negative
    perc_salesallowance_6 = decimal_field_notreq_negative
    perc_salesallowance_7 = decimal_field_notreq_negative
    perc_salesallowance_8 = decimal_field_notreq_negative
    perc_salesallowance_9 = decimal_field_notreq_negative
    perc_salesallowance_10 = decimal_field_notreq_negative

    class Meta:
        model = MemberProducerMatch
        fields = (
            'perc_salesallowance_1', 'perc_salesallowance_2', 'perc_salesallowance_3', 'perc_salesallowance_4',
            'perc_salesallowance_5', 'perc_salesallowance_6', 'perc_salesallowance_7', 'perc_salesallowance_8',
            'perc_salesallowance_9', 'perc_salesallowance_10'
        )
