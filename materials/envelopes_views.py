from io import BytesIO
import pandas as pd
import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.utils import timezone
from django.http import HttpResponse
from index.create_context import creatememberplan_context
from materials.models import EnvelopeCategory, EnvelopeCatalog


class ProducerEnvelopesCatalog(LoginRequiredMixin, TemplateView):
    template_name = "materials/envelopes_producer_catalog.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerEnvelopesCatalog, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        context['EnvelopeCatalog'] = EnvelopeCatalog.objects.filter(producer_id=self.request.user.producer_id)
        return context


class DownloadProducerEnvelopesCatalog(LoginRequiredMixin, View):
    def get(self, request):
        producer_id = self.request.user.producer_id
        name = "Envelopes_catalog_"
        export_datum = timezone.now().today().date()
        output = BytesIO()
        # Feed a buffer to workbook
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet(name + str(export_datum))

        objs = EnvelopeCatalog.objects.filter(producer_id=producer_id)
        df = pd.DataFrame(objs.values())
        bold = workbook.add_format({'bold': True})
        # columns = [f.name for f in model._meta.get_fields()]
        columns = ['supplier', 'supplier_number', 'Envelopescategory', 'Envelopesbrand', 'Envelopescolor',
                   'Envelopesweight_m2', 'Envelopes_height_mm', 'Envelopes_width_mm', 'fiber_direction', 'Envelopes_thickening',
                   'sheets_per_pack', 'price_1000sheets', 'upload_date']
        print('columns:', columns)
        # Fill first row with header in bold
        row = 0
        for i, elem in enumerate(columns):
            worksheet.write(row, i, elem, bold)
        row += 1
        # Now fill other rows with columns
        index = 0
        while index < len(df):
            for i, elem in enumerate(columns):
                try:
                    fieldvalue = df.iloc[index][elem]
                    if isinstance(fieldvalue, (list, tuple)):
                        return str(fieldvalue)[1:-1]
                except KeyError:
                    fieldvalue = []

                try:
                    worksheet.write(row, i, fieldvalue)
                except Exception as e:
                    print("no value written for: ", elem, e)
            index = index + 1
            row += 1

        # Close workbook for building file
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response
