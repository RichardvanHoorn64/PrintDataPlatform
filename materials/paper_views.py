from io import BytesIO
import pandas as pd
import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from index.exclusive_functions import define_exclusive_producer_id
from materials.models import *



class PaperBrandsDisplay(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_brands.html"
    pk_url_kwarg = 'papercategory'

    def get_context_data(self, **kwargs):
        context = super(PaperBrandsDisplay, self).get_context_data(**kwargs)
        papercategory = self.kwargs['papercategory']
        user = self.request.user

        exclusive_producer_id = define_exclusive_producer_id(user)

        paperbrand_references = PaperBrandReference.objects.filter(producer_id=exclusive_producer_id)
        if exclusive_producer_id == 1:
            paperbrand_references = PaperBrandReference.objects.all()

        papercategory_list = paperbrand_references.distinct('papercategory').order_by('papercategory')

        paperbrand_list = paperbrand_references.order_by('paperbrand')
        if not papercategory == 'All':
            paperbrand_list = paperbrand_references.filter(papercategory=papercategory).order_by('paperbrand')


        context['papercategory_list'] = papercategory_list
        context['paperbrand_list'] = paperbrand_list
        return context


class ProducerPaperCatalog(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_producer_catalog.html"

    def get_context_data(self, **kwargs):
        context = super(ProducerPaperCatalog, self).get_context_data(**kwargs)
        context['papercatalog'] = PaperCatalog.objects.filter(producer_id=self.request.user.producer_id)
        return context


class DownloadProducerPaperCatalog(LoginRequiredMixin, View):
    def get(self, request):
        producer_id = self.request.user.producer_id
        name = "paper_catalog_"
        export_datum = timezone.now().today().date()
        output = BytesIO()
        # Feed a buffer to workbook
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet(name + str(export_datum))

        objs = PaperCatalog.objects.filter(producer_id=producer_id)
        df = pd.DataFrame(objs.values())
        bold = workbook.add_format({'bold': True})
        # columns = [f.name for f in model._meta.get_fields()]
        columns = ['supplier', 'supplier_number', 'papercategory', 'paperbrand', 'papercolor',
                   'paperweight_m2', 'paper_height_mm', 'paper_width_mm', 'fiber_direction', 'paper_thickening',
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
