# zie: https://www.py4u.net/discuss/152165
# https://blog.devgenius.io/export-docx-file-with-python-docx-in-django-app-527ff5eb7280

# https://pbpython.com/python-word-template.html
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from io import BytesIO
from mailmerge import MailMerge
from datetime import date
from index.display_functions import *
from printprojects.models import *
import requests


class DownloadClientOfferInvoice(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        member_id = user.member_id
        member = Members.objects.get(member_id=member_id)
        printproject_id = self.kwargs['printproject_id']
        doc_id = self.kwargs['doc_id']
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)
        productcategory_id = printproject.productcategory_id
        productcategory = ProductCategory.objects.get(productcategory_id=productcategory_id).productcategory

        loc = 'https://printdataplatform.blob.core.windows.net/docs/'

        if member.doc_templates:
            docgroup_id = str(member_id)
        else:
            docgroup_id = str(1)

        doc_url = loc # + blob_folder + "/" + docgroup_id + "_" + templatecategory + '.docx'

        try:
            template = BytesIO(requests.get(doc_url).content)
        except Exception as e:
            # doc_url = loc + blob_folder + "/" + str(1) + "_" + templatecategory + '.docx'
            template = BytesIO(requests.get(doc_url).content)
          # print("No template availeble: member_id/template: ", member_id, templatecategory, e)

        docx = MailMerge(template)

        if printproject.client_id:
            client = Clients.objects.get(client_id=printproject.client_id)
            company = client.client
        else:
            client = member
            company = member.company

        printproject_quotenumber = printproject_own_quotenumber(printproject)
        printproject_size_description = printproject_size(printproject)
        printproject_paper_description = printproject_paper(printproject.papercategory, printproject.paperbrand,
                                                            printproject.paperweight, printproject.papercolor)

        printproject_paper_description_cover = printproject_paper(printproject.papercategory, printproject.paperbrand,
                                                                  printproject.paperweight, printproject.papercolor)

        printproject_printing_description = printproject_printing(printproject.printsided, printproject.print,
                                                                  printproject.print_back,
                                                                  printproject.number_pms_colors,
                                                                  printproject.number_pms_colors_back)

        printproject_printing_description_cover = printproject_printing(printproject.printsided_cover,
                                                                        printproject.print_cover,
                                                                        printproject.print_back_cover,
                                                                        printproject.number_pms_colors_cover,
                                                                        printproject.number_pms_colors_back_cover)

        printproject_varnish_description = printproject_varnish(printproject.printsided, printproject.pressvarnish,
                                                                printproject.pressvarnish_back, )

        printproject_varnish_description_cover = printproject_varnish(printproject.printsided_cover,
                                                                      printproject.pressvarnish_cover,
                                                                      printproject.pressvarnish_back_cover, )

        printproject_enhance_description = printproject_enhance(productcategory_id,
                                                                printproject.enhance_sided, printproject.enhance,
                                                                printproject.enhance_back, )

        printproject_finishing_description = printproject_finishing(printproject)

        if doc_id == 2:
            btw = str(round(float(printproject.invoiceturnover) * 0.21, 2))
            total = str(round(float(printproject.invoiceturnover) * 1.21, 2))
        else:
            btw = 0
            total = 0

        docx.merge(
            # general
            omschrijving=printproject_description(printproject, productcategory),

            offertenummer=printproject_quotenumber,
            datum=date.today().strftime('%d-%m-%Y'),
            aanvraag_datum=printproject.rfq_date.strftime('%d-%m-%Y'),
            klant=str(company),
            adres=str(client.street_number),
            pc_plaats=str(client.postal_code) + "" + str(client.city),
            persoonsnaam=str(user.first_name) + " " + str(user.last_name),
            oplage=str(printproject.volume) + " ex.",
            bedrukking=printproject_printing_description,
            afgewerkt_formaat=printproject_size_description,
            nabewerking=printproject_finishing_description,
            papier=printproject_paper_description,
            stand=printproject.portrait_landscape,
            productgroep=str(productcategory),
            eigen_ordernummer=printproject_client_quotenumber(printproject.client_quotenumber),
            verpakking=str(printproject.packaging),
            extra_werk=printproject_message_extra_work(printproject.message_extra_work),

            extra_persvernis=printproject_varnish_description,
            veredeling=printproject_enhance_description,
            omvang=printproject_number_of_pages(printproject),

            #   Brochures
            extra_persvernis_omslag=str(printproject_varnish_description_cover) + " omslag",
            papier_omslag=str(printproject_paper_description_cover),
            bedrukking_omslag=str(printproject_printing_description_cover),

            # finance
            aanbieding=printproject_salesprice(printproject),
            duizend_meer=printproject_salesprice1000extra(printproject),
            factuurbedrag=printproject_invoiceturnover(printproject),
            btw=btw,
            total=total
        )

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=Aanbieding ' + str(
            company) + ' nr: ' + printproject_quotenumber + " " + printproject.project_title + '.docx'
        docx.write(response)

        return response
