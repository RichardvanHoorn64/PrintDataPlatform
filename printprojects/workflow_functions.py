from calculations.item_calculations.brochure_calculation import brochure_calculation
from calculations.item_calculations.plano_folder_calculation import plano_folder_calculation
from index.categories_groups import *
from django.utils import timezone
from django.http import JsonResponse
from calculations.models import Calculations
from offers.models import Offers
from printprojects.models import PrintProjectMatch
from profileuseraccount.models import *
import random
from index.mail.email_function import send_printdataplatform_mail
from django.template.loader import render_to_string
from profileuseraccount.form_invalids import error_mail_admin

try:
    from printdataplatform.settings import *
finally:
    pass


def create_new_offer(rfq, producer_id):
    offer_key = random.randint(100000, 999999)
    requester = UserProfile.objects.get(id=rfq.user_id)
    requester_name = requester.first_name + " " + requester.last_name

    new_offer = Offers(
        printproject_id=rfq.printproject_id,
        offer_date=timezone.now().today().date(),
        producer_id=producer_id,
        member_id=rfq.member_id,
        productcategory_id=rfq.productcategory_id,
        offerstatus_id=1,
        description=rfq.description,
        offer_key=offer_key,
        requester=requester_name,
        offer=0,
        offer1000extra=0,
    )
    new_offer.save()


def select_supplier_switch_json(request, **kwargs):
    printprojectmatch_id = kwargs.get('printprojectmatch_id')
    member_id = request.user.member_id
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


def create_open_calculation_offer(rfq, producer_id, auto_quote):
    calculation_module = Producers.objects.get(producer_id=producer_id).calculation_module
    Calculations.objects.filter(producer_id=producer_id, printproject_id=rfq.printproject_id).delete()
    Offers.objects.filter(producer_id=producer_id, printproject_id=rfq.printproject_id).delete()

    if calculation_module:
        if auto_quote:
            open_calculation = Calculations(
                printproject_id=rfq.printproject_id,
                producer_id=producer_id,
                member_id=rfq.member_id,
                productcategory_id=rfq.productcategory_id,
                volume=rfq.volume,
                catalog_code=rfq.catalog_code,
                status='To be calculated',
                error=None,
                total_cost=0,
                total_cost1000extra=0,
                offer_value=0,
                offer_value1000extra=0,
                assortiment_item=False,
            )
            try:
                open_calculation.save()
            except Exception as e:
                print('open_calculation.save error: ', e)
        else:
            print('no auto quote printproject producer', rfq.printproject_id, "", producer_id)
    else:
        print('no calculation_module printproject producer', rfq.printproject_id, "", producer_id)

    # create offer
    create_new_offer(rfq, producer_id)


def auto_calculate_offer(rfq, producer_id):
    if rfq.productcategory_id in categories_plano:
        try:
            plano_folder_calculation(producer_id, rfq)
        except Exception as e:
            print('plano calculation failed', rfq.printproject_id, e)
    if rfq.productcategory_id in categories_brochures_all:
        try:
            brochure_calculation(producer_id, rfq)
        except Exception as e:
            print('brochure calculation failed', rfq.printproject_id, e)

    # update offer
    calculation = Calculations.objects.get(producer_id=producer_id, printproject_id=rfq.printproject_id)
    if not calculation.error:
        offer = Offers.objects.get(producer_id=producer_id, printproject_id=rfq.printproject_id)
        offer.offerstatus_id = 2
        offer.calculation_id = calculation.calculation_id
        offer.offer_date = calculation.offer_date
        offer.modified = calculation.offer_date
        offer.offer = calculation.offer_value
        offer.offer1000extra = calculation.offer_value1000extra
        offer.save()


# send rfq to selected producers
def send_rfq_mail(producer, member_company, offer, printproject):
    merge_data = {
        'producer': producer,
        'member_company': member_company,
        'member_requester': offer.requester,
        'offer': offer,
        'offer_key': str(offer.offer_key),
        'printproject': printproject,
    }

    # select email template
    if producer.member_plan_id in producer_memberplans:
        email_template = 'emails/rfq_mailbody_pro.html'
    else:
        email_template = 'emails/rfq_mailbody_open.html'
    subject = render_to_string("emails/rfq_subject.txt", merge_data)

    html_body = render_to_string(email_template, merge_data)
    address = producer.e_mail_rfq

    try:
        send_printdataplatform_mail(subject, address, html_body)
    except Exception as e:
        error_mail_admin('rfq_mail.send() error: ', e)


def send_calculationupdate_mail(producer, member_company, offer, calculation):
    if calculation.error:
        result = 'calculatie error: ' + str(calculation.error)
    else:
        result = 'Offerte uitgebracht'

    merge_data = {
        'producer': producer,
        'member_company': member_company,
        'member_requester': offer.requester,
        'offer': offer,
        'error': calculation.error,
        'result': result
    }

    # select email template
    email_template = 'emails/calculationupdate_mailbody.html'
    subject = render_to_string("emails/calculationupdate_subject.txt", merge_data)
    html_body = render_to_string(email_template, merge_data)
    address = producer.e_mail_rfq

    try:
        send_printdataplatform_mail(subject, address, html_body)
    except Exception as e:
        error_mail_admin('calculationupdate_mail.send() error: ', e)
