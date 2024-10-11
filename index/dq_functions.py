from sqlite3 import IntegrityError

from django.core.exceptions import ObjectDoesNotExist

from assets.models import GeneralCalculationSettings
from producers.models import *
from methods.models import *


def producer_dq_functions(user):
    if user.member_plan_id == 4:
        producer_id = user.producer_id
        update_productcategory_offerings(producer_id)
        update_enhancement_offerings(producer_id)
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
    availeble_producers = ProducerProductOfferings.objects.values_list('producer_id', flat=True)

    productcategories = ProductCategory.objects.values_list('productcategory_id', flat=True)
    producer_productcategories = ProducerProductOfferings.objects.values_list('productcategory_id', flat=True).filter(
        producer_id=producer_id)
    missing_producer_productcategories = [x for x in productcategories if x not in producer_productcategories]
    for productcategory_id in missing_producer_productcategories:
        if producer_id in availeble_producers:
            pass
        else:
            try:
                new_productcategory_id = ProducerProductOfferings(
                    productcategory_id=productcategory_id,
                    producer_id=producer_id,
                    availeble=True
                )
                new_productcategory_id.save()
            except IntegrityError:
                pass


def update_enhancement_offerings(producer_id):
    enhancement_options = EnhancementOptions.objects.values_list('enhancement_id', flat=True)
    producer_enhancement_tariffs = EnhancementTariffs.objects.values_list('enhancement_id', flat=True).filter(
        producer_id=producer_id)

    for tariff in enhancement_options:
        if tariff not in producer_enhancement_tariffs:
            try:
                new_transport = EnhancementTariffs(
                    enhancement_id=tariff,
                    producer_id=producer_id,
                    added_value=True,
                    setup_cost=0,
                    minimum_cost=0,
                    production_cost_1000sheets=0,
                    max_sheet_width=0,
                    max_sheet_height=0,
                )
                new_transport.save()
            except IntegrityError:
                pass

    for tariff in producer_enhancement_tariffs:
        if tariff not in enhancement_options:
            try:
                old_tariff = EnhancementTariffs.objects.get(producer_id=producer_id,
                                                            enhancement_id=tariff)
                old_tariff.delete()
            except ObjectDoesNotExist:
                pass


def update_packaging_tariffs(producer_id):
    packaging_options = PackagingOptions.objects.values_list('packagingoption_id', flat=True)
    producer_packaging_tariffs = PackagingTariffs.objects.values_list('packagingtariff_id', flat=True).filter(
        producer_id=producer_id)

    for tariff in packaging_options:
        if tariff not in producer_packaging_tariffs:
            try:
                new_transport = PackagingTariffs(
                    producer_id=producer_id,
                    packagingoption_id=tariff,
                    availeble=True,
                    setup_cost=0,
                    cost_per_100kg=0,
                    cost_per_unit=0,
                    max_weight_packaging_unit_kg=100,
                )
                new_transport.save()
            except IntegrityError:
                pass

    for tariff in producer_packaging_tariffs:
        if tariff not in packaging_options:
            try:
                old_tariff = PackagingTariffs.objects.get(producer_id=producer_id,
                                                          packagingoption_id=tariff)
                old_tariff.delete()
            except ObjectDoesNotExist:
                pass


def update_transport_tariffs(producer_id):
    transport_options = TransportOptions.objects.values_list('transportoption_id', flat=True)
    producer_transport_tariffs = TransportTariffs.objects.values_list('transportoption_id', flat=True).filter(
        producer_id=producer_id)

    for tariff in transport_options:
        if tariff not in producer_transport_tariffs:
            try:
                new_transport = TransportTariffs(
                    producer_id=producer_id,
                    transportoption_id=tariff,
                    added_value=True,
                    availeble=True,
                    setup_cost=0,
                    cost_per_100kg=0,
                )
                new_transport.save()
            except IntegrityError:
                pass

    for tariff in producer_transport_tariffs:
        if tariff not in transport_options:
            try:
                old_tariff = TransportTariffs.objects.get(producer_id=producer_id,
                                                          transportoption_id=tariff)
                old_tariff.delete()
            except ObjectDoesNotExist:
                pass
