import io
import pandas as pd
import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.utils import timezone
from django.views.generic import View
from downloads.download_functions import *
from offers.models import Offers
from orders.models import Orders
from printprojects.models import *
from profileuseraccount.models import *


class ProducerDownloadOffers(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        producer_id = user.producer.producer_id
        language_id = user.language_id
        producer_company = Producers.objects.get(producer_id=producer_id).company

        # Feed a buffer to workbook
        export_datum = timezone.now().today().date()
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        bold = workbook.add_format({'bold': True})

        if language_id == 1:
            worksheet_name_offers = 'offertes_'

        else:
            worksheet_name_offers = 'offers_'

        # worksheet offers
        worksheet_offers = workbook.add_worksheet(worksheet_name_offers + str(export_datum))
        df_offers = pd.DataFrame(Offers.objects.filter(producer_id=producer_id).values())

        # df_offers.replace(enhance_rear.nan, None)
        df_offers = df_offers.where(df_offers.notnull(), 0)

        df_offers['offertedate'] = df_offers['offer_date'].dt.strftime('%d-%m-%Y')
        df_offers['project_title'] = df_offers.apply(
            lambda row: retrieve_project_title(row['printproject_id']), axis=1)
        df_offers['productcategory'] = df_offers.apply(
            lambda row: retrieve_productcategory(row['productcategory_id']), axis=1)
        df_offers['offerstatus'] = df_offers.apply(
            lambda row: retrieve_offerstatus(row['offerstatus_id']), axis=1)
        df_offers['producer'] = df_offers.apply(
            lambda row: retrieve_producer(row['producer_id']), axis=1)
        df_offers['rfq_company'] = df_offers.apply(
            lambda row: retrieve_company(row['member_id']), axis=1)

        df_printprojects = pd.DataFrame(PrintProjects.objects.all().values())
        df_offers = df_offers.merge(df_printprojects, how='left', on='printproject_id')

        df_offers = df_offers[[
            'offer_id', 'printproject_id', 'calculation_id', 'offer_date', 'requester', 'offer', 'offer1000extra',
            'offertedate', 'project_title_x', 'productcategory', 'offerstatus', 'producer', 'volume',
            'height_mm_product', 'width_mm_product', 'papercategory', 'paperbrand', 'paperweight', 'papercolor',
            'pressvarnish_front', 'pressvarnish_rear', 'pressvarnish_booklet', 'enhance_sided', 'enhance_front',
            'enhance_rear', 'packaging', 'folding', 'number_of_pages', 'portrait_landscape', 'finishing_brochures',
            'printsided', 'number_pms_colors_front', 'number_pms_colors_rear', 'number_pms_colors_booklet',
            'print_front', 'print_rear', 'print_booklet', 'papercategory_cover', 'paperbrand_cover',
            'paperweight_cover', 'papercolor_cover'
        ]]

        if language_id == 1:
            df_offers.rename(
                columns={'project_title_x': 'projectnaam', 'requester': 'aangevraagd door',
                         'offertedate': 'offertedatum',
                         'producer': 'producent', 'offerstatus': 'offerte status', 'description': 'omschrijving',
                         'offer': 'offerte', 'offer_1000extra': 'offerte 1000 meer',
                         'producer_contact': 'contactpersoon producent', 'producer_notes': 'notitie producent',
                         'productcategory': 'productcategorie'}, inplace=True)

        offers_columns = df_offers.columns.values.tolist()
        excel_fill_worksheet(worksheet_offers, df_offers, offers_columns, bold)

        # Close workbook for building file
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True,
                            filename='PrintDataPlatform ' + producer_company + " " + str(export_datum) + '.xlsx')


class ProducerDownloadOrders(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        producer_id = user.producer.producer_id
        language_id = user.language_id
        producer_company = Producers.objects.get(producer_id=producer_id).company

        # Feed a buffer to workbook
        export_datum = timezone.now().today().date()
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        bold = workbook.add_format({'bold': True})

        worksheet_name_orders = 'orders_'

        # worksheet orders
        worksheet_orders = workbook.add_worksheet('orders_' + str(export_datum))
        df_orders = pd.DataFrame(Orders.objects.filter(producer_id=producer_id).values())
        df_orders['order_date'] = pd.to_datetime(df_orders['orderdate']).dt.strftime('%d-%m-%Y')

        df_orders['productcategory'] = df_orders.apply(
            lambda row: retrieve_productcategory(row['productcategory_id']), axis=1)
        df_orders['rfq_company'] = df_orders.apply(
            lambda row: retrieve_company(row['member_id']), axis=1)
        df_orders['producer'] = df_orders.apply(
            lambda row: retrieve_producer(row['producer_id']), axis=1)
        df_orders['orderstatus'] = df_orders.apply(
            lambda row: retrieve_orderstatus(row['order_status_id']), axis=1)
        df_orders['orderer'] = df_orders.apply(
            lambda row: retrieve_orderer(row['orderer_id']), axis=1)

        if language_id == 1:
            df_orders.rename(
                columns={
                    'producer': 'producent', 'order_date': 'orderdatum', 'ordernumber': 'ordernummer',
                    'client': 'klant',
                    'productcategory': 'productcategorie', 'orderstatus': 'order status',
                    'order_description': 'order omschrijving', 'supplier_remarks': 'producent opmerkingen',
                    'orderer': 'besteller', 'order_volume': 'order oplage', 'order_value': 'order waarde',
                    'order_morecost': 'meerkosten',
                    'order_remarks': '', 'deliver_postcode': 'aflever  postcode', 'deliver_city': 'aflever plaats',
                    'deliver_company': 'afleverer bij:',
                    'deliver_contactperson': 'contactpersoon aflevering', 'deliver_tel': 'aflevering telefoonnummer'
                }, inplace=True)

            df_orders = df_orders[
                ['ordernummer', 'printproject_id', 'besteller', 'offer_id', 'order omschrijving',
                 'producent opmerkingen',
                 'order oplage', 'order waarde', 'meerkosten', 'delivery_date_request', 'delivery_date_deliverd',
                 'printfiles_available', 'deliver_street_number', 'aflever  postcode', 'aflever plaats',
                 'afleverer bij:', 'contactpersoon aflevering', 'aflevering telefoonnummer', 'orderdatum',
                 'productcategorie', 'rfq_company', 'producent', 'order status']]

        orders_columns = df_orders.columns.values.tolist()
        excel_filf_worksheet(worksheet_orders, df_orders, orders_columns, bold)

        orders_columns = df_orders.columns.values.tolist()
        excel_fill_worksheet(worksheet_orders, df_orders, orders_columns, bold)

        # Close workbook for building file
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True,
                            filename='PrintDataPlatform ' + producer_company + " " + str(export_datum) + '.xlsx')
