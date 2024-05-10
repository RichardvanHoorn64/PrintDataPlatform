from assets.models import GeneralCalculationSettings
from producers.models import *
from methods.models import *


def producer_dq_functions(user):
    if user.member_plan_id == 4:
        producer_id = user.producer_id
        update_productcategory_offerings(producer_id)
        update_enhencement_offerings(producer_id)
        update_packaging_tariffs(producer_id)
        update_transport_tariffs(producer_id)


# producers
# set General Calculation Settings
def set_calculationsettings(producer_id):
    settings = GeneralCalculationSettings.objects.filter(producer_id=producer_id)
    number_of_instances = len(settings)

    if number_of_instances > 1:
        settings.delete()

    if number_of_instances > 1 or number_of_instances == 0:
        settings.delete()

        general_settings = GeneralCalculationSettings(
            producer_id=producer_id,
            order_startcost=0,
            purchase_paper_perc_added=0,
            overflow_offset_mm=2,
            katernmargin=2,
            headmargin=2,
            pms_offering=True,
        )
        general_settings.save()


def update_productcategory_offerings(producer_id):
    productcategories = ProductCategory.objects.values_list('productcategory_id', flat=True)
    producer_productcategories = ProducerProductOfferings.objects.values_list('productcategory_id', flat=True).filter(
        producer_id=producer_id)
    missing_producer_productcategories = [x for x in productcategories if x not in producer_productcategories]
    for productcategory_id in missing_producer_productcategories:
        new_productcategory_id = ProducerProductOfferings(
            productcategory_id=productcategory_id,
            producer_id=producer_id,
            availeble=True
        )
        new_productcategory_id.save()


def update_enhencement_offerings(producer_id):
    enhancements = EnhancementOptions.objects.values_list('enhancement_id', flat=True)
    producer_enhancements = EnhancementTariffs.objects.values_list('enhancement_id', flat=True).filter(
        producer_id=producer_id)
    missing_producer_enhancements = [x for x in enhancements if x not in producer_enhancements]
    for enhancement_id in missing_producer_enhancements:
        new_enhancement = EnhancementTariffs(
            enhancement_id=enhancement_id,
            producer_id=producer_id,

        )
        new_enhancement.save()


def update_packaging_tariffs(producer_id):
    packaging_options = PackagingOptions.objects.values_list('packagingoption_id', flat=True)
    producer_packaging_tariffs = PackagingTariffs.objects.values_list('packagingtariff_id', flat=True).filter(
        producer_id=producer_id)
    missing_producer_packagingoptions = [x for x in packaging_options if x not in producer_packaging_tariffs]
    for  packagingoption_id in missing_producer_packagingoptions:
        new_packaging = PackagingTariffs(
            producer_id=producer_id,
            packagingoption_id= packagingoption_id,
        )
        new_packaging.save()


def update_transport_tariffs(producer_id):
    transport_options = TransportOptions.objects.values_list('transportoption_id', flat=True)
    producer_transport_tariffs = TransportTariffs.objects.values_list('transportoption_id', flat=True).filter(
        producer_id=producer_id)
    missing_producer_transport_tariffs = [x for x in transport_options if x not in producer_transport_tariffs]
    for transportoption_id in missing_producer_transport_tariffs:
        new_transport = TransportTariffs(
            transportoption_id=transportoption_id,
            producer_id=producer_id,
        )
        new_transport.save()
