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
from materials.papercatalog_uploadform import UploadProducerPaperCatalogCSVForm


class PaperBrandsDisplay(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_brands.html"
    pk_url_kwarg = 'papercategory_id'

    def get_context_data(self, **kwargs):
        context = super(PaperBrandsDisplay, self).get_context_data(**kwargs)
        papercategory_id = self.kwargs['papercategory_id']
        user = self.request.user

        exclusive_producer_id = define_exclusive_producer_id(user)

        if papercategory_id == 0:
            paperbrand_list = PaperBrands.objects.filter(producer_id=exclusive_producer_id)
        else:
            papercategory = PaperCategories.objects.get(papercategory_id=papercategory_id).papercategory
            paperbrand_list = PaperBrands.objects.filter(papercategory=papercategory, producer_id=exclusive_producer_id)
        context['paperbrand_list'] = paperbrand_list
        context['papercategory_list'] = PaperCategories.objects.filter(producer_id=exclusive_producer_id)
        return context


class ProducerPaperCatalog(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_producer_catalog.html"

    def get_context_data(self, **kwargs):
        context = super(ProducerPaperCatalog, self).get_context_data(**kwargs)
        context['papercatalog'] = PaperCatalog.objects.filter(producer_id=self.request.user.producer_id)
        return context


class UploadProducerPaperCatalog(LoginRequiredMixin, View):
    template = "materials/paper_producer_catalog_upload.html"
    form_class = UploadProducerPaperCatalogCSVForm
    success_url = '/paper_catalog/'
    instruction = 'Use CSV file UTF-8 with header and comma separated'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        user = self.request.user
        producer_id = user.producer_id
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)

        if paper_catalog:
            count_paper_catalog = paper_catalog.count()
            latest_upload = paper_catalog[1].upload_date
        else:
            count_paper_catalog = 0
            latest_upload = 'Nu papercatalog loaded'

        return render(request, self.template, {'form': form,
                                               'instruction': self.instruction,
                                               'count_paper_catalog': count_paper_catalog,
                                               'latest_upload': latest_upload,
                                               })

    def post(self, request, *args, **kwargs):
        form = self.form_class
        producer_id = self.request.user.producer_id
        name = self.request.user.first_name + " " + self.request.user.last_name
        upload_date = timezone.now().today().date()
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)
        error = []

        if paper_catalog:
            count_paper_catalog = paper_catalog.count()
            latest_upload = paper_catalog[1].upload_date
        else:
            count_paper_catalog = 0
            latest_upload = 'Load papercatalog using a csv file'

        try:
            csv_file = self.request.FILES['paper_catalog_file']  # .read().decode("utf-8")

            # if file is not csv file, return
            if not csv_file.name.endswith('.csv'):
                error = 'Error: Your file is not CSV type'

            # if file is too large, return
            if csv_file.multiple_chunks():
                error = 'Error: Your uploaded file is too big (> MB)'

            if error:
                return render(request, self.template, {'form': form,
                                                       'instruction': 'Please refresh page and try again',
                                                       'count_paper_catalog': count_paper_catalog,
                                                       'latest_upload': latest_upload,
                                                       'error': error,
                                                       })

        except Exception as e:
            print('error e: ' + str(e))
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Your file is not CSV type, please refresh page and try again',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error + str(e),
                                                   })

        # delete old papercatalog and save new papercatalog
        try:
            old_catalog = paper_catalog
            for old_item in old_catalog:
                old_item.delete()

            new_catalog = pd.read_csv(csv_file, delimiter=';', header=0, encoding='latin-1')
            new_catalog['producer_id'] = producer_id

            # lookup papercategory by brand uploaded
            paperbrand_list = new_catalog['paperbrand'].tolist()
            papercategory = []
            for paperbrand in paperbrand_list:

                try:
                    papercategory = PaperBrandReference.objects.get(paperbrand=paperbrand).papercategory
                except PaperBrandReference.DoesNotExist:
                    papercategory = "No papercategory reference"

            new_catalog['papercategory'] = papercategory

            decimal_columns = ['paper_thickening', 'price_1000sheets']
            integer_columns = ['paperweight_m2', 'paper_height_mm', 'paper_width_mm']

            for col in decimal_columns:
                new_catalog[col] = round(new_catalog[col].replace(',', '.', regex=True).astype(float), 2)

            for col in integer_columns:
                new_catalog[col] = new_catalog[col].astype(int)

            for index, row in new_catalog.iterrows():
                new_paperspecs = PaperCatalog(
                    producer_id=producer_id,
                    uploaded_by=name,
                    upload_date=upload_date,
                    supplier=row['supplier'],
                    supplier_number=row['supplier_number'],
                    papercategory=row['papercategory'],
                    paperbrand=row['paperbrand'],
                    papercolor=row['papercolor'],
                    paperweight_m2=row['paperweight_m2'],
                    paper_height_mm=row['paper_height_mm'],
                    paper_width_mm=row['paper_width_mm'],
                    paper_surface=row['paper_height_mm'] * row['paper_width_mm'],
                    fiber_direction=row['fiber_direction'],
                    paper_thickening=row['paper_thickening'],
                    sheets_per_pack=row['sheets_per_pack'],
                    price_1000sheets=row['price_1000sheets'],

                )
                new_paperspecs.save()
        except Exception as e:
            error = 'papercatalog not loaded, error:' + str(e)
            print(error)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Contact site administrator for help',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # papercategory dropdown
        try:
            old_papercategories = PaperCategories.objects.filter(producer_id=producer_id)
            for old_papercategory in old_papercategories:
                old_papercategory.delete()

            new_papercategorylist = pd.DataFrame(
                new_catalog[['producer_id', 'papercategory']].drop_duplicates())

            for index, row in new_papercategorylist.iterrows():
                if len(PaperCategories.objects.filter(papercategory=row['papercategory'],producer_id=producer_id)) == 0:
                    new_papercategory = PaperCategories(
                        papercategory=row['papercategory'],
                        producer_id=row['producer_id'],
                    )
                    new_papercategory.save()

            for index, row in new_papercategorylist.iterrows():
                if len(PaperCategories.objects.filter(papercategory=row['papercategory'],producer_id=None)) == 0:
                    new_general_papercategory = PaperCategories(
                        papercategory=row['papercategory'],
                    )
                    new_general_papercategory.save()

        except Exception as e:
            error = 'Papercategories not loaded:' + str(e)
            print(error)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Correct file, please refresh page and try again',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # paperbrand dropdown
        try:
            old_paperbands = PaperBrands.objects.filter(producer_id=producer_id)
            for old_paperband in old_paperbands:
                old_paperband.delete()

            new_paperbandlist = pd.DataFrame(
                new_catalog[['producer_id', 'papercategory', 'paperbrand']].drop_duplicates())

            for index, row in new_paperbandlist.iterrows():
                new_paperbands = PaperBrands(
                    producer_id=row['producer_id'],
                    upload_date=upload_date,
                    papercategory=row['papercategory'],
                    paperbrand=row['paperbrand'],
                )
                new_paperbands.save()

            for index, row in new_paperbandlist.iterrows():
                if len(PaperBrands.objects.filter(papercategory=row['papercategory'],paperbrand=row['paperbrand'], producer_id=None)) == 0:
                    new_general_paperbrand = PaperBrands(
                        upload_date=upload_date,
                        papercategory=row['papercategory'],
                        paperbrand=row['paperbrand'],
                    )
                    new_general_paperbrand.save()

        except Exception as e:
            error = 'Paperbrands not loaded:' + str(e)
            print(error)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Correct file, please refresh page and try again',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

            # paperweights dropdown
        try:
            old_paperweights = PaperWeights.objects.filter(producer_id=producer_id)
            for old_paperweight in old_paperweights:
                old_paperweight.delete()

            new_paperweightslist = pd.DataFrame(
                new_catalog[['producer_id', 'papercategory', 'paperbrand', 'paperweight_m2']].drop_duplicates())

            for index, row in new_paperweightslist.iterrows():
                new_paperweights = PaperWeights(
                    producer_id=row['producer_id'],
                    upload_date=upload_date,
                    papercategory=row['papercategory'],
                    paperbrand=row['paperbrand'],
                    paperweight_m2=row['paperweight_m2'],
                )
                new_paperweights.save()

            for index, row in new_paperweightslist.iterrows():
                if len(PaperWeights.objects.filter(papercategory=row['papercategory'],paperbrand=row['paperbrand'], paperweight_m2=row['paperweight_m2'], producer_id=None)) == 0:
                    new_general_paperweight = PaperWeights(
                        upload_date=upload_date,
                        papercategory=row['papercategory'],
                        paperbrand=row['paperbrand'],
                        paperweight_m2=row['paperweight_m2'],
                    )
                    new_general_paperweight.save()

        except Exception as e:
            error = 'New_paperweights not loaded:' + str(e)
            print('error new_paperweights not loaded:', e)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Contact site administrator for help',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # end procedure
        return redirect('/paper_catalog/',
                        {'form': form,
                         'last_upload': upload_date,
                         'success_message': 'File succesfull stored',
                         })


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
