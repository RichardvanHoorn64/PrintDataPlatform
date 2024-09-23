from orders.models import *
from producers.models import *

def get_offercontext(producer_id, context, offerstatus_id):
    offers = Offers.objects.filter(producer_id=producer_id, active=True).exclude(offerstatus_id=4)
    try:
        if offerstatus_id == 0:
            context['offers'] = offers.order_by('-offer_date')

        else:
            context['offers'] = offers.filter(offerstatus=offerstatus_id).order_by('-offer_date')
    except Exception as e:
        print(str(e))
        context['offers'] = offers.order_by('-offer_date')

    # counts
    context['all_offers'] = offers.count()
    context['open_offers'] = offers.filter(offerstatus=1).count()
    context['offered_offers'] = offers.filter(offerstatus=2).count()
    context['prod_offers'] = offers.filter(offerstatus=3).count()
    context['denied_offers'] = offers.filter(offerstatus=5).count()
    return context


def get_ordercontext(producer_id, context, orderstatus_id):
    orders = Orders.objects.filter(producer_id=producer_id, active=True)

    # dashboard lists
    try:
        if orderstatus_id == 0:
            context['orders'] = orders.order_by('-orderdate').exclude(order_status_id__gt=3)
            context['orderstatus'] = 'Open'
        else:
            context['orders'] = orders.filter(order_status_id=orderstatus_id).order_by(
                '-orderdate')
            orderstatus = OrderStatus.objects.get(orderstatus_id=orderstatus_id).orderstatus
            context['orderstatus'] = orderstatus
    finally:
        context['orders'] = orders.order_by('-orderdate').exclude(order_status_id__gt=3)

    # counts
    context['all_orders'] = orders.count()
    context['req_orders'] = orders.filter(order_status_id=1).count()
    context['prod_orders'] = orders.filter(order_status_id=2).count()
    context['denied_orders'] = orders.filter(order_status_id=3).count()
    context['inv_orders'] = orders.filter(order_status_id=4).count()
    context['closed_orders'] = orders.filter(order_status_id=5).count()

    return context


def get_producercategories(producer_id):
    product_categories = ProducerProductOfferings.objects.filter(producer_id=producer_id, availeble=True).values_list(
        'productcategory_id', flat=True)
    return product_categories
