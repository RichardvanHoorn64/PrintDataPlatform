from sqlite3 import IntegrityError
from django.shortcuts import redirect
from offers.models import Offers
from orders.models import Orders
from printprojects.models import *
from producers.models import *
from producers.producer_functions import get_producercategories


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



def update_producersmatch(request):
    user = request.user
    member_id = user.member_id
    demo_company = user.member.demo_company

    producers_demo = Producers.objects.filter(demo=True, active=True).values_list('producer_id', flat=True)
    producers_open = Producers.objects.filter(demo=False, active=True).values_list('producer_id', flat=True)

    producers_not_active = Producers.objects.filter(active=False).values_list('producer_id', flat=True)
    producers_not_open_for_match = Producers.objects.filter(only_exclusive=True).values_list('producer_id', flat=True)
    matches = MemberProducerMatch.objects.filter(member_id=member_id).values_list('producer_id', flat=True)

    # Matches for demo companies
    if demo_company:
        # create new member producer matches demo
        for producer_id in producers_demo:
            if producer_id not in matches:
                MemberProducerMatch.objects.create(producer_id=producer_id,
                                                   member_id=member_id,
                                                   memberproducerstatus_id=2)
        # delete open production companies for demo members
        for producer_open_match in producers_open:
            if producer_open_match in matches:
                open_matches = MemberProducerMatch.objects.filter(producer_id=producer_open_match,
                                                                      member_id=member_id)
                for no_match in open_matches:
                    no_match.delete()

    # Matches for open production companies
    else:
        # create new member producer matches demo
        for producer_id in producers_open:
            if producer_id not in matches:
                MemberProducerMatch.objects.create(producer_id=producer_id,
                                                   member_id=member_id,
                                                   memberproducerstatus_id=2)
        # delete demo companies for non demo members
        for producer_demo_match in producers_demo:
            if producer_demo_match in matches:
                not_demo_matches = MemberProducerMatch.objects.filter(producer_id=producer_demo_match,
                                                                      member_id=member_id)
                for no_match in not_demo_matches:
                    no_match.delete()

    # delete not active producers
    for producer_not_active in producers_not_active:
        if producer_not_active in matches:
            not_open_matches = MemberProducerMatch.objects.filter(producer_id=producer_not_active,
                                                                  member_id=member_id)
            for no_match in not_open_matches:
                no_match.delete()


    # delete producers not open for match
    for producer_not_open_for_match in producers_not_open_for_match:
        if producer_not_open_for_match in matches:
            not_open_matches = MemberProducerMatch.objects.filter(producer_id=producer_not_open_for_match,
                                                                      member_id=member_id)
            for no_match in not_open_matches:
                no_match.delete()


def update_printprojectsmatch(request, printproject_id):
    member_id = request.user.member_id
    user = request.user

    try:
        printproject = PrintProjects.objects.get(printproject_id=printproject_id,
                                                 member_id=member_id)

        preferred_suppliers = MemberProducerMatch.objects.filter(member_id=member_id,
                                                                 memberproducerstatus=1).values_list(
            'producer_id',
            flat=True)

    except PrintProjects.DoesNotExist:
        return redirect('/no_access/')

    print('preferred_suppliers: ', preferred_suppliers)
    current_matchers = PrintProjectMatch.objects.filter(printproject_id=printproject_id)
    for current_match in current_matchers:
        current_match.delete()

    # preferred suppliers projectmatch
    for producer_id in preferred_suppliers:
        producer_product_categories = get_producercategories(producer_id)
        if printproject.productcategory_id in producer_product_categories:
            memberproducermatch = MemberProducerMatch.objects.get(producer_id=producer_id, member_id=member_id)
            if producer_id in preferred_suppliers:
                try:
                    PrintProjectMatch.objects.create(printproject_id=printproject_id,
                                                     memberproducermatch_id=memberproducermatch.memberproducermatch_id,
                                                     member_id=member_id,
                                                     user_id=user.id,
                                                     producer_id=producer_id,
                                                     ranking=memberproducermatch.ranking,
                                                     member_block=False,
                                                     preferred_supplier=True,
                                                     active=True
                                                     )
                except IntegrityError:
                    pass


def update_number_of_open_offers(member_id):
    printprojects = PrintProjects.objects.filter(member_id=member_id, printprojectstatus_id=2)
    offers = Offers.objects.filter(member_id=member_id, offerstatus_id=2)

    for printproject in printprojects:
        printproject.number_of_offers = offers.filter(printproject_id=printproject.printproject_id,
                                                      ).count()
        printproject.save()
