# zie: https://www.py4u.net/discuss/152165
# https://blog.devgenius.io/export-docx-file-with-python-docx-in-django-app-527ff5eb7280

# https://pbpython.com/python-word-template.html
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from io import BytesIO
from datetime import date
from index.display_functions import *
from offers.models import Offers
from printprojects.models import *
from django.shortcuts import redirect
import requests
from mailmerge import MailMerge
from django.conf import settings
from django.http import HttpResponse
from azure.storage.blob import BlobServiceClient


class DownloadProducerOfferPDF(LoginRequiredMixin, View):
    from django.conf import settings
    def dispatch(self, request, *args, **kwargs):
        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        blob_name = offer.doc_name
        account_name = settings.AZURE_STORAGE_ACCOUNT_NAME
        account_key = settings.AZURE_STORAGE_ACCOUNT_KEY
        container_name = "produceroffers"

        # Maak een BlobServiceClient aan
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Haal de blob-client op
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Download de PDF-inhoud
        stream = blob_client.download_blob()
        pdf_content = stream.readall()

        # Maak een HTTP-response met de PDF-inhoud
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{blob_name}"'

        return response


class DownloadProducerOffer(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        printproject_id = offer.printproject_id
        producer = Producers.objects.get(producer_id=offer.producer_id)
        producer_company = producer.company
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)

        member_id = printproject.member_id
        requester_name = describe_requester(printproject)

        if member_id is not user.member.member_id and user.member.member_plan_id in open_memberplans:
            return redirect('/no_access/')

        member = Members.objects.get(member_id=member_id)
        productcategory_id = printproject.productcategory_id
        productcategory = ProductCategory.objects.get(productcategory_id=productcategory_id).productcategory

        client = member
        company = member.company
        printproject_number_of_pages_description = printproject_number_of_pages(printproject)
        printproject_quotenumber = printproject_own_quotenumber(printproject)
        printproject_size_description = printproject_size(printproject)
        printproject_paper_description = printproject_paper(printproject.papercategory, printproject.paperbrand,
                                                            printproject.paperweight, printproject.papercolor)

        printproject_paper_description_cover = printproject_paper(printproject.papercategory_cover,
                                                                  printproject.paperbrand_cover,
                                                                  printproject.paperweight_cover,
                                                                  printproject.papercolor_cover)

        printproject_paper_description_booklet = printproject_paper(printproject.papercategory,
                                                                    printproject.paperbrand_cover,
                                                                    printproject.paperweight_cover,
                                                                    printproject.papercolor_cover)

        if productcategory_id in categories_brochures_all:
            printproject_printing_description = printproject_printing_booklet(printproject.print_booklet,
                                                                              printproject.number_pms_colors_booklet,
                                                                              printproject.pressvarnish_booklet)
        else:
            printproject_printing_description = printproject_printing(printproject.printsided, printproject.print_front,
                                                                      printproject.print_back,
                                                                      printproject.number_pms_colors_front,
                                                                      printproject.number_pms_colors_back)

        printproject_printing_cover = printproject_printing(printproject.printsided,
                                                            printproject.print_front,
                                                            printproject.print_back,
                                                            printproject.number_pms_colors_front,
                                                            printproject.number_pms_colors_back)

        printproject_varnish_description = printproject_varnish(printproject.printsided,
                                                                printproject.pressvarnish_front,
                                                                printproject.pressvarnish_back, )

        printproject_enhance_description = printproject_enhance(productcategory_id,
                                                                printproject.enhance_sided, printproject.enhance_front,
                                                                printproject.enhance_back, )

        printproject_finishing_description = printproject_finishing(printproject)

        printproject_packaging_description = printproject_packaging(printproject.packaging)

        producer_id = 1

        doc_template = []
        if productcategory_id in categories_plano:
            doc_template = 'plano'
        if productcategory_id in categories_folders:
            doc_template = 'folders'
        if productcategory_id in categories_selfcovers:
            doc_template = 'selfcovers'
        if productcategory_id in categories_brochures_cover:
            doc_template = 'brochures'

        url = 'https://printdatastorage.blob.core.windows.net/media/' + str(
            producer_id) + '/docs/offers/' + doc_template + '.docx'

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=Aanbieding ' + str(
            company) + ' nr: ' + str(printproject_quotenumber) + " " + str(printproject.project_title) + '.docx'

        template = BytesIO(requests.get(url).content)

        try:
            document = MailMerge(template)
        except Exception as e:
            print('offertemplate not availeble, error: ', str(e))
            return response

        document.merge(
            # general
            producer=producer_company,
            omschrijving=printproject_description(printproject, productcategory),

            offertenummer=str(printproject_quotenumber),
            datum=date.today().strftime('%d-%m-%Y'),
            aanvraag_datum=printproject.rfq_date.strftime('%d-%m-%Y'),
            klant=str(company),
            adres=str(client.street_number),
            pc_plaats=str(client.postal_code) + "" + str(client.city),
            persoonsnaam=requester_name,
            oplage=str(printproject.volume) + " ex.",
            uitvoering=str(printproject_number_of_pages_description),
            bedrukking=printproject_printing_description,
            afgewerkt_formaat=printproject_size_description,
            nabewerking=printproject_finishing_description,
            papier=printproject_paper_description,
            stand=printproject.portrait_landscape,
            productgroep=str(productcategory),
            eigen_ordernummer=printproject_client_quotenumber(printproject.client_quotenumber),
            verpakking=str(printproject_packaging_description),
            extra_werk=printproject_message_extra_work(printproject.message_extra_work),

            extra_persvernis=printproject_varnish_description,
            veredeling=printproject_enhance_description,
            omvang=printproject_number_of_pages(printproject),

            #   Brochures
            papier_omslag=str(printproject_paper_description_cover),
            papier_bw=str(printproject_paper_description_booklet),
            bedrukking_omslag=str(printproject_printing_cover),
            bedrukking_bw=str(printproject_printing_description),
            persvernis_omslag=str(printproject_varnish_description) + " omslag",

            # finance
            aanbieding=str(offer_salesprice(offer)),
            duizend_meer=str(offer_salesprice1000extra(offer)),
            factuurbedrag=str(printproject_invoiceturnover(printproject))
        )

        document.write(response)

        return response
