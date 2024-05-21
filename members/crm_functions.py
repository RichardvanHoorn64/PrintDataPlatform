from django.http import JsonResponse
from offers.models import Offers
from orders.models import Orders
from printprojects.models import *
from producers.models import *


def update_clientdashboard(member_id):
    clients = Clients.objects.filter(member_id=member_id).values_list('client_id', flat=True)
    for client in clients:
        count_open_projects = PrintProjects.objects.filter(member_id=member_id, client_id=client,
                                                           printprojectstatus__in=[1, 2, 3, 4]).count()
        count_open_orders = Orders.objects.filter(member_id=member_id, client_id=client,
                                                  order_status__in=[1, 2, 3, 4]).count()

        update_client = Clients.objects.get(client_id=client)
        update_client.count_printprojects = count_open_projects
        update_client.count_orders = count_open_orders
        update_client.save()


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


def update_producersmatch(request):
    member_id = request.user.member_id
    producers = Producers.objects.filter(active=True).values_list('producer_id', flat=True)
    producers_not_active = Producers.objects.filter(active=False).values_list('producer_id', flat=True)
    matches = MemberProducerMatch.objects.filter(member_id=member_id).values_list('producer_id',
                                                                                  flat=True)

    for producer in producers:
        if producer not in matches:
            MemberProducerMatch.objects.create(producer_id=producer, member_id=member_id)

    for producer_ex in producers_not_active:
        if producer_ex in matches:
            MemberProducerMatch.objects.get(producer_id=producer_ex, member_id=member_id).delete()


def update_printprojectsmatch(request, printproject_id):
    member_id = request.user.member_id
    printproject = PrintProjects.objects.get(printproject_id=printproject_id)
    productcategory_id = printproject.productcategory_id

    projectmatches = PrintProjectMatch.objects.filter(member_id=member_id, printproject_id=printproject_id).values_list(
        'producer_id',
        flat=True)

    producers = ProducerProductOfferings.objects.filter(productcategory_id=productcategory_id).values_list('producer_id',
                                                                                                     flat=True)
    preferred_suppliers = MemberProducerMatch.objects.filter(member_id=member_id).exclude(
        memberproducerstatus=3).values_list('producer_id',
                                            flat=True)  # .exclude(memberproducerstatus=3)

    for producer in producers:
        if producer in preferred_suppliers:
            if producer not in projectmatches:
                try:
                    match = MemberProducerMatch.objects.get(producer_id=producer)
                    memberproducermatch_id = match.memberproducermatch_id
                    if match.memberproducerstatus_id == 1:
                        preferred_supplier = True
                    else:
                        preferred_supplier = False

                except Exception as e:
                    print("update_printprojectsmatch error: ", str(e))
                    memberproducermatch_id = None
                    preferred_supplier = False

                PrintProjectMatch.objects.create(printproject_id=printproject_id, member_id=member_id,
                                                 user_id=request.user.id,
                                                 producer_id=producer,
                                                 memberproducermatch_id=memberproducermatch_id,
                                                 preferred_supplier=preferred_supplier
                                                 )


def update_number_of_open_offers(member_id):
    printprojects = PrintProjects.objects.filter(member_id=member_id, printprojectstatus_id=2)
    offers = Offers.objects.filter(member_id=member_id, offerstatus_id=2)

    for printproject in printprojects:
        printproject.number_of_offers = offers.filter(printproject_id=printproject.printproject_id,
                                                      ).count()
        printproject.save()
