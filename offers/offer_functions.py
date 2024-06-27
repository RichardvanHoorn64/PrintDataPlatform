from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from offers.models import *
from offers.rfq_functions import *
from printprojects.models import *


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
