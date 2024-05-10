import random
from api.api_views.api_drukwerkmaatwerk import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from offers.models import *
from offers.rfq_functions import *
from printprojects.models import *


class PrintProjectRFQView(LoginRequiredMixin, TemplateView):
    template_name = 'printprojects/new_project.html'


# select suppliers
def select_clientcontact_json(requests, **kwargs):
    client_id = kwargs.get('client_id')
    member_id = requests.user.member_id
    clientcontacts = list(
        ClientContacts.objects.filter(client_id=client_id, member_id=member_id).values().order_by('last_name'))
    return JsonResponse({'data': clientcontacts})


# select suppliers
def select_supplier_switch_json(requests, **kwargs):
    printprojectmatch_id = kwargs.get('printprojectmatch_id')
    member_id = requests.user.member_id
    match = PrintProjectMatch.objects.get(printprojectmatch_id=printprojectmatch_id, member_id=member_id)
    match_status = match.matchprintproject
    if not match_status:
        new_status = True

    else:
        new_status = False

    update_record = match
    update_record.matchprintproject = new_status
    update_record.save()
    return JsonResponse({'data': new_status})


def offer_acceskey_submit(requests, **kwargs):
    offer_id = kwargs.get('offer_id')
    offer_key_test = kwargs.get('offer_key_test')
    member_id = requests.user.member_id
    offer_key = Offers.objects.get(offer_id=offer_id, member_id=member_id).offer_key

    if offer_key == offer_key_test:
        access = True
    else:
        access = False
    return JsonResponse({'data': access})


# send rfq to selected suppliers
class SendRFQView(LoginRequiredMixin, View):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'

    def dispatch(self, request, *args, **kwargs):
        printproject_id = kwargs['printproject_id']
        user = self.request.user
        member_id = user.member_id
        requester = user.first_name + " " + user.last_name
        member_company = user.company
        printprojectsmatch = PrintProjectMatch.objects.filter(printproject_id=printproject_id, member_id=member_id)
        selected_producers = printprojectsmatch.filter(matchprintproject=True)
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)

        # clean offers
        Offers.objects.filter(printproject_id=printproject_id).delete()

        # create offers
        for producer in selected_producers:
            offer_key = random.randint(10000, 99999)
            Offers.objects.create(
                printproject_id=printproject_id,
                producer_id=producer.producer_id,
                member_id=member_id,
                productcategory_id=printproject.productcategory_id,
                offerstatus_id=1,
                description=printproject.description,
                offer_key=offer_key,
                requester=requester,
            )

        # Send rfq's
        new_offers = Offers.objects.filter(printproject_id=printproject_id)
        for new_offer in new_offers:
            error = []

            try:
                producer = Producers.objects.get(producer_id=new_offer.producer_id)
                if producer.api_available:
                    api_function = producer.api_function

                    if api_function == 'api_drukwerkmaatwerk_com' and new_offer.productcategory_id in [3, 4, 5, ]:
                        try:
                            api_drukwerkmaatwerk_com(user, new_offer.offer_id)
                            error = []
                        except Exception as e:
                            send_rfq_mail(producer, member_company, new_offer, printproject)
                            error = "drukwerkmaatwerk api error: " + str(e)
                            print(error)

                else:
                    send_rfq_mail(producer, member_company, new_offer, printproject)
            except Exception as e:
                error = error + str(e)
                print("send rfq error, offer_id: ", str(new_offer.offer_id), error)

        # set printprojectstatus
        printprojects_update = PrintProjects.objects.filter(printproject_id=printproject_id)
        for project_update in printprojects_update:
            project_update.printprojectstatus_id = 2
            project_update.save()

        return redirect('/printproject_details/' + str(printproject_id))
