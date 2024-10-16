from calculations.item_calculations.brochure_calculation import brochure_calculation
from calculations.item_calculations.plano_folder_calculation import plano_folder_calculation
from index.categories_groups import *
from django.utils import timezone
from calculations.models import Calculations
from offers.models import Offers
from profileuseraccount.models import Producers
import random


def create_new_offer(rfq, producer_id):
    offer_key = random.randint(100000, 999999)
    new_offer = Offers(
        printproject_id=rfq.printproject_id,
        offer_date=timezone.now().today().date(),
        producer_id=producer_id,
        member_id=rfq.member_id,
        productcategory_id=rfq.productcategory_id,
        offerstatus_id=1,
        description=rfq.description,
        offer_key=offer_key,
        requester=rfq.user_id,
        offer=0,
        offer1000extra=0,
    )
    new_offer.save()


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
            print('no auto quote printproject producer', rfq.printproject_id, "", producer_id )
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


