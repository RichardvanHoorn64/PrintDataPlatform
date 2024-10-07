from io import BytesIO
import io
import pandas as pd
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View, TemplateView
from downloads.download_functions import *
from calculations.assortiment_uploadform import *
from calculations.item_calculations.brochure_calculation import brochure_calculation
from calculations.item_calculations.plano_folder_calculation import plano_folder_calculation
from index.create_context import creatememberplan_context
from index.translate_functions import *
from index.categories_groups import *


class AssortimentView(LoginRequiredMixin, TemplateView):
    model = Calculations
    template_name = 'producers/assortiment_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AssortimentView, self).get_context_data(**kwargs)
        user = self.request.user
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        catalog = Calculations.objects.filter(producer_id=producer_id, assortiment_item=True).order_by('calculation_id')

        last_calculation = catalog[0].offer_date
        if not last_calculation:
            last_calculation = '--'
        context['catalog'] = catalog
        context['last_calculation'] = last_calculation
        return context


class CalculateAssortiment(View):
    success_url = '/producer_assortiment/'

    def get(self, request):
        user = self.request.user
        producer_id = user.producer_id
        assortiment = PrintProjects.objects.filter(producer_id=producer_id, assortiment_item=True).order_by()

        for rfq in assortiment:
            if rfq.productcategory_id in categories_plano:
                plano_folder_calculation(producer_id, rfq)
            if rfq.productcategory_id in categories_brochures_all:
                brochure_calculation(producer_id, rfq)
        return redirect('producer_assortiment')


class DownloadAssortiment(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        producer_id = user.producer_id
        calculations = Calculations
        export_datum = timezone.now().today().date()
        output = BytesIO()

        # Feed a buffer to workbook
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)

        worksheet_name = 'Listcalculations '
        worksheet_listcalculations = workbook.add_worksheet(worksheet_name + str(export_datum))

        objs_calculations = calculations.objects.filter(producer_id=producer_id, assortiment_item=True).order_by(
            "calculation_id")
        df_calculations = pd.DataFrame(objs_calculations.values())
        bold = workbook.add_format({'bold': True})

        calculations_columns = ['calculation_id', 'productcategory', 'producer', 'printproject', 'catalog_code',
                                'status', 'error',
                                'volume', 'printer_booklet', 'printer_cover', 'cuttingmachine_booklet',
                                'foldingmachine',
                                'foldingmachines_booklet', 'bindingmachine', 'paperspec_id_booklet',
                                'paperspec_id_cover',
                                'pages_per_sheet_booklet', 'pages_per_katern_booklet', 'number_of_printruns_booklet',
                                'book_thickness', 'waste_printing', 'waste_printing1000extra', 'waste_folding',
                                'waste_folding1000extra', 'waste_binding', 'waste_binding1000extra',
                                'waste_printing_cover',
                                'waste_printing1000extra_cover', 'waste_folding_cover', 'waste_folding1000extra_cover',
                                'waste_binding_cover', 'waste_binding1000extra_cover', 'order_startcost',
                                'printingcost', 'printingcost_booklet', 'printingcost_cover', 'printingcost1000extra',
                                'printingcost_booklet1000extra', 'printing_cost_cover1000extra', 'inkcost',
                                'inkcost_booklet',
                                'inkcost_cover', 'inkcost1000extra', 'inkcost_booklet1000extra',
                                'inkcost_cover1000extra',
                                'foldingcost', 'foldingcost1000extra', 'foldingcost_booklet',
                                'foldingcost_booklet1000extra', 'cuttingcost', 'cuttingcost1000extra',
                                'cuttingcost_booklet', 'cuttingcost_booklet1000extra', 'bindingcost',
                                'bindingcost1000extra',
                                'enhancecost_cover', 'enhancecost_cover1000extra', 'purchase_plates',
                                'purchase_plates_booklet', 'margin_plates_booklet', 'platecost_cover',
                                'platecost_booklet', 'purchase_plates_cover', 'margin_plates_cover',
                                'papercost1000extra', 'papercost_booklet', 'papercost_booklet1000extra',
                                'papercost_cover', 'papercost_cover1000extra', 'number_of_printruns_cover',
                                'cover_starttime', 'printing_runtime_cover', 'add_value_purchase_paper_cover',
                                'paper1000extra_cost', 'paper1000extra_cost_cover',
                                'add_value_purchase_paper1000extra_cover', 'printing_cover', 'paper_quantity',
                                'paper_quantity1000extra', 'paper_quantity_booklet',
                                'paper_quantity_booklet1000extra', 'paper_quantity_cover',
                                'paper_quantity_cover1000extra', 'papercost_total', 'papercost_booklet_total',
                                'papercost_cover_total', 'papercost_total1000extra',
                                'papercost_booklet_total1000extra', 'papercost_cover_total1000extra',
                                'packagingcost', 'packagingcost1000extra', 'orderweight_kg',
                                'transportcost', 'transportcost1000extra', 'total_cost', 'total_cost1000extra',
                                'added_value', 'perc_added_value', 'added_value1000extra', 'perc_added_value1000extra']

        excel_fill_worksheet(worksheet_listcalculations, df_calculations, calculations_columns, bold)

        # Close workbook for building file
        workbook.close()
        buffer.seek(0)

        # Close workbook for building file
        workbook.close()
        output.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='PrintDataPlatform ' + str(worksheet_name) + ' ' + str(user.company) + ' ' + str(export_datum)+'.xlsx')


class UploadAssortimentCSV(LoginRequiredMixin, View):
    template = 'producers/assortiment_upload.html'
    form_class = UploadAssortimentCSVForm
    success_url = '/producer_assortiment/'
    instruction = 'Gebruik de voorgeschreven CSV file met header en de seperator ;'
    upload_date = timezone.now().today().date()

    def get(self, request, *args, **kwargs):
        form = self.form_class
        producer_id = self.request.user.producer_id
        catalog = PrintProjects.objects.filter(producer_id=producer_id, printprojectstatus_id=5)

        if catalog:
            catalog_size = catalog.count()
            upload_date = catalog[0].upload_date
        else:
            catalog_size = 0
            upload_date = None

        return render(request, self.template, {'form': form,
                                               'instruction': self.instruction,
                                               'catalog': catalog,
                                               'catalog_size': catalog_size,
                                               'last_upload': upload_date,
                                               'Productcategories': ProductCategory.objects.all().order_by(
                                                   'productcategory_id'),
                                               'error': self.kwargs['error']
                                               })

    def post(self, request, *args, **kwargs):
        form = self.form_class
        user = self.request.user
        producer_id = user.producer_id
        user_id = user.id
        catalog = PrintProjects.objects.filter(producer_id=producer_id, printprojectstatus_id=5)
        new_catalog = []

        if catalog:
            catalog_size = catalog.count()
            upload_date = catalog[0].upload_date
        else:
            catalog_size = 0
            upload_date = None

        error = []
        csv_file = []

        if not error:
            try:
                csv_file = self.request.FILES['assortiment_file']

            except Exception as e:
                error = 'Alleen een CSV file toegestaan: ' + str(e)
                print("error: ", error)

        if not error:
            try:
                if not csv_file.name.endswith('.csv'):
                    messages.error(request,
                                   'Error:  Your file is not Excel .xlsx type, please refresh page and try again')
                    error = 'Alleen een CSV file toegestaan'
                    print("error: ", error)
                else:
                    error = []
            except Exception as e:
                error = 'File load error: ' + str(e)
                print("error: ", error)

            # if file is too large, return
            if not error:
                try:
                    if csv_file.multiple_chunks():
                        messages.error(request,
                                       "Error: Your uploaded file is too big (%.10f MB), please refresh page and try again" % (
                                           csv_file.size / (1000 * 1000),))
                        error = "Your uploaded file is too big (%.10f MB), please refresh page and try again"

                except Exception as e:
                    error = 'Your uploaded file is too big (%.10f MB), please refresh page and try again: ' + str(e)
                    print("error: ", error)

        # oud assortiment verwijderen en nieuwe opslaan
        if not error:
            try:
                new_catalog = pd.read_csv(csv_file, delimiter=';', header=0, encoding="utf-8")
            except Exception as e:
                error = 'File read error: ' + str(e)
                print("error: ", error)
            try:
                new_catalog = translate_dataframe(new_catalog)
            except Exception as e:
                error = 'File translation error: ' + str(e)
                print("error: ", error)

        if not error:
            try:
                old_catalog = catalog
                for item in old_catalog:
                    item.delete()

                new_catalog = new_catalog[new_catalog['volume'] > 0]
                new_catalog['volume'] = new_catalog['volume'].astype(int)

            except Exception as e:
                error = 'fieldconversion error:' + str(e)
                print("error: ", error)
        if not error:
            try:
                # delete old assortiment calculations
                old_assortiment_calculations = Calculations.objects.filter(producer_id=producer_id,
                                                                           assortiment_item=True)
                for calculation in old_assortiment_calculations:
                    calculation.delete()

                for index, row in new_catalog.iterrows():
                    new_item = PrintProjects(
                        user_id=user_id,
                        producer_id=producer_id,
                        member_id=user.member_id,
                        productcategory_id=row['productcategory_id'],
                        project_title=row['project_title'],
                        catalog_code=row['catalog_code'],
                        volume=row['volume'],
                        height_mm_product=row['height_mm_product'],
                        width_mm_product=row['width_mm_product'],
                        paperbrand=row['paperbrand'],
                        paperweight=row['paperweight'],
                        papercolor=row['papercolor'],
                        printsided=modify_printsided(row['printsided']),
                        pressvarnish_front=modify_boleaninput(row['pressvarnish_front']),
                        pressvarnish_rear=modify_boleaninput(row['pressvarnish_rear']),
                        pressvarnish_booklet=modify_boleaninput(row['pressvarnish_booklet']),
                        enhance_sided=modify_printsided(row['enhance_sided']),
                        enhance_front=find_enhancement_id(row['enhance_front']),
                        enhance_rear=find_enhancement_id(row['enhance_rear']),
                        packaging=find_packaging_id(row['packaging']),
                        folding=find_foldingspecs(row['folding']),
                        number_of_pages=row['number_of_pages'],
                        portrait_landscape=find_orientation(row['portrait_landscape']),
                        finishing_brochures=find_brochure_finishingmethod_id(row['finishing_brochures']),
                        print_front=modify_printcolors(row['print_front']),
                        print_rear=modify_printcolors(row['print_rear']),
                        print_booklet=modify_printcolors(row['print_booklet']),
                        number_pms_colors_front=row['number_pms_colors_front'],
                        number_pms_colors_rear=row['number_pms_colors_rear'],
                        number_pms_colors_booklet=row['number_pms_colors_booklet'],
                        paperbrand_cover=row['paperbrand_cover'],
                        paperweight_cover=row['paperweight_cover'],
                        papercolor_cover=row['papercolor_cover'],
                        upload_date=timezone.now().today().date(),
                        assortiment_item=True,
                        printprojectstatus_id=5,
                    )
                    new_item.save()

                    # upload new assortiment calculations
                    new_calculation = Calculations(
                        printproject_id=new_item.printproject_id,
                        producer_id=producer_id,
                        member_id=new_item.member_id,
                        assortiment_item=True,
                        productcategory_id=new_item.productcategory_id,
                        volume=new_item.volume,
                        catalog_code=new_item.catalog_code,
                        status='To be calculated',
                        error='--',
                        total_cost=0,
                        total_cost1000extra=0,
                        offer_value=0,
                        offer_value1000extra=0,
                    )
                    new_calculation.save()

            except Exception as e:
                error = 'File not loaded, error:' + str(e)
                print("error: ", error)

        if not error:
            return redirect('/producer_assortiment/',
                            {'form': form,
                             'catalog': catalog,
                             'catalog_size': catalog_size,
                             'last_upload': upload_date,
                             'messages': messages,
                             'instruction': 'File succesfull stored',
                             })

        else:
            return redirect('/producer_assortiment_upload/' + str(error),
                            {'form': form,
                             'catalog': catalog,
                             'catalog_size': catalog_size,
                             'last_upload': upload_date,
                             'messages': messages,
                             'instruction': 'File succesfull stored',
                             'error': error
                             })
