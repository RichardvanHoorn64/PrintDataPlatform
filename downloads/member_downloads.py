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


class MemberDownloadPrintprojects(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        member_id = user.member_id
        language_id = user.language_id
        member_company = Members.objects.get(member_id=member_id).company

        # Feed a buffer to workbook
        export_datum = timezone.now().today().date()
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        bold = workbook.add_format({'bold': True})

        if language_id == 1:
            worksheet_name_projects = 'projecten_'
            worksheet_name_offers = 'offertes_'

        else:
            worksheet_name_projects = 'projects_'
            worksheet_name_offers = 'offers_'

        # worksheet printprojects
        worksheet_printprojects = workbook.add_worksheet(worksheet_name_projects + str(export_datum))
        df_printprojects = pd.DataFrame(PrintProjects.objects.filter(member_id=member_id).values())
        df_printprojects['productcategory'] = df_printprojects.apply(
            lambda row: retrieve_productcategory(row['productcategory_id']), axis=1)
        df_printprojects['printprojectstatus'] = df_printprojects.apply(
            lambda row: retrieve_printprojectstatus(row['printprojectstatus_id']), axis=1)
        df_printprojects['projectmanager'] = df_printprojects.apply(
            lambda row: retrieve_projectmanager(row['user_id']), axis=1)
        df_printprojects['client'] = df_printprojects.apply(
            lambda row: retrieve_client(row['client_id'], member_id), axis=1)
        df_printprojects['clientcontact'] = df_printprojects.apply(
            lambda row: retrieve_clientcontact(row['clientcontact_id'], member_id), axis=1)
        df_printprojects['request_date'] = df_printprojects['rfq_date'].dt.strftime('%d-%m-%Y')

        # iterating the columns
        for col in df_printprojects.columns:
            print(col)

        df_printprojects = df_printprojects[['printproject_id', 'productcategory_id',
                                             'user_id', 'member_id', 'producer_id', 'client_id', 'clientcontact_id',
                                             'printprojectstatus_id',
                                             'project_title', 'description', 'message_extra_work', 'own_quotenumber',
                                             'client_quotenumber', 'rfq_date',
                                             'volume', 'number_of_offers', 'supply_date', 'delivery_date',
                                             'format_selection', 'standard_size',
                                             'height_mm_product', 'papercategory', 'paperbrand', 'paperweight',
                                             'papercolor', 'pressvarnish_front',
                                             'pressvarnish_back', 'pressvarnish_booklet', 'enhance_sided',
                                             'enhance_front', 'enhance_back', 'packaging',
                                             'folding', 'number_of_pages', 'portrait_landscape', 'finishing_brochures',
                                             'printsided',
                                             'number_pms_colors_front', 'number_pms_colors_back',
                                             'number_pms_colors_booklet', 'print_front', 'print_back',
                                             'print_booklet', 'papercategory_cover', 'paperbrand_cover',
                                             'paperweight_cover', 'papercolor_cover',
                                             'salesprice', 'salesprice_1000extra', 'invoiceturnover', 'created',
                                             'modified', 'active', 'productcategory',
                                             'printprojectstatus', 'projectmanager', 'client', 'clientcontact',
                                             'request_date']]

        # if language_id == 1:
        #     df_printprojects.rename(columns={
        #         'client': 'klant', 'clientcontact': 'klant contact', 'productcategory': 'productcategorie',
        #         'project_title': 'projectnaam', 'description': 'omschrijving',
        #         'message_extra_work': 'aanvraag extra werk', 'own_quotenumber': 'eigen ordernummer',
        #         'client_quotenumber': 'ordernummer klant',
        #         'request_date': 'datum', 'volume': 'oplage', 'number_of_offers': 'aantal offertes',
        #         'standard_size': 'standdaardformaat', 'height_mm_product': 'product hoogte mm',
        #         'width_mm_product': 'product breedte mm', 'papercategory': 'papiercategorie',
        #         'paperbrand': 'papiermerk', 'paperweight': 'papiergewicht m2', 'papercolor': 'papierkleur',
        #         'pressvarnish': 'persvernis',
        #         'pressvarnish_back': 'persvernis achterzijde', 'enhance_sided': 'veredeling uitvoering',
        #         'enhance': 'veredeling', 'enhance_back': 'veredeling achterzijde', 'packaging': 'verpakking',
        #         'folding': 'vouwmethode', 'number_of_pages': 'omvang', 'portrait_landscape': 'staand/liggend',
        #         'finishing_brochures': 'nabewerking brochures',
        #         'printsided': 'bedrukking uitvoering', 'print': 'bedrukking', 'print_back': 'bedrukking achterzijde',
        #         'number_pms_colors': 'aantal pms kleuren', 'number_pms_colors_back': 'aantal pms kleuren achterzijde',
        #         'printsided_cover': 'omslag bedrukking uitvoering', 'print_cover': 'omslag bedrukking',
        #         'print_back_cover': 'omslag bedrukking achterzijde',
        #         'number_pms_colors_cover': 'aantal pms kleuren omslag',
        #         'number_pms_colors_back_cover': 'aantal pms kleuren omslag binnenzijde',
        #         'pressvarnish_cover': 'persvernis omslag', 'pressvarnish_back_cover': 'persvernis omslag binnenzijde',
        #         'papercategory_cover': 'papiercategorie omslag',
        #         'paperbrand_cover': 'papiermerk omslag', 'paperweight_cover': 'papiergewicht m2 omslag',
        #         'papercolor_cover': 'papierkleur omslag'}, inplace=True)

        printprojects_columns = df_printprojects.columns.values.tolist()
        excel_fill_worksheet(worksheet_printprojects, df_printprojects, printprojects_columns, bold)

        # worksheet offers
        worksheet_offers = workbook.add_worksheet(worksheet_name_offers + str(export_datum))
        df_offers = pd.DataFrame(Offers.objects.filter(member_id=member_id).values())
        df_offers['offertedate'] = df_offers['offer_date'].dt.strftime('%d-%m-%Y')
        df_offers['project_title'] = df_offers.apply(
            lambda row: retrieve_project_title(row['printproject_id']), axis=1)
        df_offers['productcategory'] = df_offers.apply(
            lambda row: retrieve_productcategory(row['productcategory_id']), axis=1)
        df_offers['offerstatus'] = df_offers.apply(
            lambda row: retrieve_offerstatus(row['offerstatus_id']), axis=1)
        df_offers['producer'] = df_offers.apply(
            lambda row: retrieve_producer(row['producer_id']), axis=1)

        df_offers = df_offers[[
            'offer_id', 'printproject_id', 'project_title', 'requester', 'offertedate', 'producer', 'offerstatus',
            'description',
            'offer', 'offer1000extra', 'producer_contact', 'producer_notes', 'productcategory', ]]

        if language_id == 1:
            df_offers.rename(
                columns={'project_title': 'projectnaam', 'requester': 'aangevraagd door', 'offertedate': 'offertedatum',
                         'producer': 'producent', 'offerstatus': 'offerte status', 'description': 'omschrijving',
                         'offer': 'offerte', 'offer_1000extra': 'offerte 1000 meer',
                         'producer_contact': 'contactpersoon producent', 'producer_notes': 'notitie producent',
                         'productcategory': 'productcategorie'}, inplace=True)

        offers_columns = df_offers.columns.values.tolist()
        excel_fill_worksheet(worksheet_offers, df_offers, offers_columns, bold)

        # worksheet orders
        worksheet_orders = workbook.add_worksheet('orders_' + str(export_datum))
        df_orders = pd.DataFrame(Orders.objects.filter(member_id=member_id).values())
        # df_orders['orderdate'] = pd.to_datetime(df_orders['orderdate']).dt.strftime('%d-%m-%Y')

        # df_orders['productcategory'] = df_orders.apply(
        #     lambda row: retrieve_productcategory(row['productcategory_id']), axis=1)
        # df_orders['client'] = df_orders.apply(
        #     lambda row: retrieve_client(row['client_id'], member_id), axis=1)
        # df_orders['producer'] = df_orders.apply(
        #     lambda row: retrieve_producer(row['producer_id']), axis=1)
        # df_orders['orderstatus'] = df_orders.apply(
        #     lambda row: retrieve_orderstatus(row['order_status_id']), axis=1)
        # df_orders['orderer'] = df_orders.apply(
        #     lambda row: retrieve_orderer(row['orderer_id']), axis=1)

        # df_orders = df_orders[[
        #     'producer', 'order_id', 'printproject_id', 'offer_id', 'orderdate', 'ordernumber', 'client',
        #     'productcategory', 'orderstatus', 'order_description', 'supplier_remarks',
        #     'orderer', 'order_volume', 'order_value', 'order_morecost',
        #     'order_remarks', 'deliver_postcode', 'deliver_city', 'deliver_company',
        #     'deliver_contactperson', 'deliver_tel'
        # ]]

        # if language_id == 1:
        #     df_orders.rename(
        #         columns={
        #             'producer': 'producent', 'orderdate': 'orderdatum', 'ordernumber': 'ordernummer',
        #             'client': 'klant',
        #             'productcategory': 'productcategorie', 'orderstatus': 'order status',
        #             'order_description': 'order omschrijving', 'supplier_remarks': 'producent opmeringen',
        #             'orderer': 'besteller', 'order_volume': 'order oplage', 'order_value': 'order waarde',
        #             'order_morecost': 'meerkosten',
        #             'order_remarks': '', 'deliver_postcode': 'aflever  postcode', 'deliver_city': 'aflever plaats',
        #             'deliver_company': 'afleverer bij:',
        #             'deliver_contactperson': 'contactpersoon aflevering', 'deliver_tel': 'aflevering telefoonnummer'
        #         }, inplace=True)

        orders_columns = df_orders.columns.values.tolist()
        excel_fill_worksheet(worksheet_orders, df_orders, orders_columns, bold)

        # Close workbook for building file
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True,
                            filename='PrintDataPlatform projects' + member_company + " " + str(export_datum) + '.xlsx')


class MemberDownloadClients(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        member_id = user.member_id
        language_id = user.language_id
        member_company = Members.objects.get(member_id=member_id).company

        # Feed a buffer to workbook
        export_datum = timezone.now().today().date()
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        bold = workbook.add_format({'bold': True})

        if language_id == 1:
            worksheet_name_clients = 'klanten_'
            filename = 'Klanten PrintDataHub '

        else:
            worksheet_name_clients = 'projects_'
            filename = 'Clients PrintDataHub '

        # worksheet printprojects
        worksheet_clients = workbook.add_worksheet(worksheet_name_clients + str(export_datum))
        df_clients = pd.DataFrame(ClientContacts.objects.filter(member_id=member_id).values())

        df_clients['client'] = df_clients.apply(
            lambda row: retrieve_client(row['client_id'], member_id), axis=1)

        df_clients = df_clients[
            ['client', 'clientcontact', 'jobtitle', 'e_mail_personal', 'mobile_number', 'linkedin_url',
             'facebook_url'
             ]]

        if language_id == 1:
            df_clients.rename(columns={
                'client': 'klant', 'clientcontact': 'contactpersoon', 'jobtitle': 'functie',
                'e_mail_personal': 'email persoonlijk ', 'mobile_number': 'tel mobiel'}, inplace=True)

        clients_columns = df_clients.columns.values.tolist()
        excel_fill_worksheet(worksheet_clients, df_clients, clients_columns, bold)

        # Close workbook for building file
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True,
                            filename=filename + member_company + " " + str(export_datum) + '.xlsx')
