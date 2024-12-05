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
from django.http import HttpResponse
from fileupload.storage_functions import *


class DownloadProducerOfferPDF(LoginRequiredMixin, View):
    from django.conf import settings

    def dispatch(self, request, *args, **kwargs):
        STORAGE_ACCOUNT_NAME = AZURE_STORAGE_ACCOUNT_NAME
        CONTAINER_NAME = "produceroffers"

        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        FILE_NAME = offer.doc_name
        BLOB_NAME = str(offer_id) + '_' + FILE_NAME

        # Create BlobServiceClient
        # if DEBUG:
        #     blob_service_client = get_blob_service_client_local()
        # else:
        blob_service_client = get_blob_service_client_azure()
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        # Download the blob
        download_stream = blob_client.download_blob()
        pdf_content = download_stream.readall()
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{FILE_NAME}"'
        print(f"Blob '{BLOB_NAME}' downloaded successfully downloaded.")

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
        if productcategory_id in categories_envelopes:
            doc_template = 'envelopes'

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

        if printproject.productcategory_id in categories_envelopes:
            printproject_env_size_close_cut = str(display_env_size_close_cut(printproject))
            printproject_env_material_color = str(display_env_material_color(printproject))
            printproject_env_window = str(display_env_window(printproject))
        else:
            printproject_env_size_close_cut = []
            printproject_env_material_color = []
            printproject_env_window = []

        if productcategory_id in categories_brochures_all:
            papier_bw = str(printproject_paper_description_booklet)
            bedrukking_bw = str(printproject_printing_description)
        else:
            papier_bw = []
            bedrukking_bw = []

        if productcategory_id in categories_brochures_cover:
            papier_omslag = str(printproject_paper_description_cover),
            bedrukking_omslag = str(printproject_printing_cover) + " omslag",
            persvernis_omslag = str(printproject_varnish_description) + " omslag",
        else:
            papier_omslag = []
            bedrukking_omslag = []
            persvernis_omslag = []

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
            papier_omslag=papier_omslag,
            papier_bw=papier_bw,
            bedrukking_omslag=bedrukking_omslag,
            bedrukking_bw=bedrukking_bw,
            persvernis_omslag=persvernis_omslag,

            # Envelopes
            env_uitvoering=printproject_env_size_close_cut,
            env_materiaaal=printproject_env_material_color,
            env_venster=printproject_env_window,

            # finance
            aanbieding=str(offer_salesprice(offer)),
            duizend_meer=str(offer_salesprice1000extra(offer)),
            factuurbedrag=str(printproject_invoiceturnover(printproject))
        )

        document.write(response)

        return response
