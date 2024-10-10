from orders.models import *
from producers.models import *


def get_offercontext(producer, context, offerstatus_id, dashboard):
    all_offers = Offers.objects.filter(producer_id=producer.producer_id, active=True)
    offer_table_title = "Aanbiedingen van " + str(producer.company)
    try:
        if offerstatus_id == 0:
            if dashboard:
                all_offers = all_offers.exclude(offerstatus_id=4)
                offers = all_offers.order_by('-offer_date')[:100]
                offer_table_title = "Laatste 100 aanbiedingen van " + str(producer.company)
            else:
                offers = all_offers.order_by('-offer_date')
            context['offers'] = offers

        else:
            context['offers'] = all_offers.filter(offerstatus=offerstatus_id).order_by('-offer_date')
    except Exception as e:
        print('offer context error: ', str(e))

    # counts
    context['all_offers'] = all_offers.count()
    context['open_offers'] = all_offers.filter(offerstatus=1).count()
    context['offered_offers'] = all_offers.filter(offerstatus=2).count()
    context['prod_offers'] = all_offers.filter(offerstatus=3).count()
    context['closed_offers'] = all_offers.filter(offerstatus=4).count()
    context['denied_offers'] = all_offers.filter(offerstatus=5).count()
    context['offer_table_title'] = offer_table_title
    return context


def get_ordercontext(producer, context, order_status_id, dashboard):
    all_orders = Orders.objects.filter(producer_id=producer.producer_id, active=True)
    orders = all_orders.order_by('-orderdate')

    order_table_title = "Orders voor " + str(producer.company)

    # dashboard lists
    try:
        if order_status_id == 0:
            if dashboard:
                orders = all_orders.order_by('-orderdate')[:100]
                order_table_title = "Laatste 100 orders voorn " + str(producer.company)
            else:
                context['orderstatus'] = 'Open'
        else:
            context['orders'] = all_orders.filter(order_status_id=order_status_id).order_by(
                '-orderdate')
            orderstatus = OrderStatus.objects.get(orderstatus_id=order_status_id).orderstatus

            context['orderstatus'] = orderstatus
    except Exception as e:
        print('order context error: ', str(e))

    context['orders'] = orders
    context['all_orders'] = all_orders.count()
    context['req_orders'] = all_orders.filter(order_status_id=1).count()
    context['prod_orders'] = all_orders.filter(order_status_id=2).count()
    context['denied_orders'] = all_orders.filter(order_status_id=3).count()
    context['inv_orders'] = all_orders.filter(order_status_id=4).count()
    context['closed_orders'] = all_orders.filter(order_status_id=5).count()
    context['order_table_title'] = order_table_title

    return context


def get_producercategories(producer_id):
    all_productcategories = ProductCategory.objects.all().values_list(
        'productcategory_id', flat=True)

    current_producer_categories = ProducerProductOfferings.objects.filter(producer_id=producer_id, availeble=True).values_list(
        'productcategory_id', flat=True)

    for productcategory_id in all_productcategories:
        if productcategory_id not in current_producer_categories:
            new_producer_category = ProducerProductOfferings.objects.create(
                productcategory_id=productcategory_id,
                producer_id=producer_id,
                availeble=True
            )
            new_producer_category.save()

    producer_categories = ProducerProductOfferings.objects.filter(producer_id=producer_id, availeble=True).values_list(
        'productcategory_id', flat=True)

    return producer_categories
