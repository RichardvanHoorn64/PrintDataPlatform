from django.shortcuts import redirect
from members.crm_functions import update_number_of_open_offers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from offers.models import Offers
from orders.models import Orders
from producers.models import ProducerProductOfferings
from printprojects.models import *


class PrintDataPlatformDashboard(LoginRequiredMixin, TemplateView):
    template_name = "homepage/member_dashboard.html"
    pk_url_kwarg = 'printprojectstatus_id'
    context_object_name = 'printprojectstatus_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrintDataPlatformDashboard, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        update_number_of_open_offers(member_id)

        printprojects = PrintProjects.objects.filter(member_id=member_id, active=True)
        orders = Orders.objects.filter(member_id=member_id, active=True)
        offers = Offers.objects.filter(member_id=member_id, active=True)

        context['user'] =user

        # store
        categories_available = [1,2,3,4,5]

        if user.member.member_plan_id == 3:
            excl_producer_id = user.member.exclusive_producer_id
            categories_available = ProducerProductOfferings.objects.filter(producer_id=excl_producer_id)

        context['categories_available'] = categories_available


        src_loc = 'drukwerkmaatwerkopslag.blob.core.windows.net/media/brandportal/producent'
        media_loc = str(1)

        context['src_loc'] = src_loc
        context['media_loc'] = media_loc

        # dashboard lists and titles
        context['printproject_list'] = printprojects.order_by('-rfq_date')[:10][::-1]
        context['order_list'] = orders.order_by('-orderdate')[:10][::-1]
        context['offers_list'] = offers.order_by('-offer_date')[:10][::-1]
        context['printproject_table_title'] = 'Laatste 10 printprojecten'
        context['offer_table_title'] = 'Laatste 10 aanbiedingen'
        context['order_table_title'] = 'Laatste 10 orders'

        # counts
        context['all_projects'] = printprojects.count()
        context['open_projects'] = printprojects.filter(printprojectstatus=1).count()
        context['rfq_projects'] = printprojects.filter(printprojectstatus=2).count()
        context['prod_projects'] = printprojects.filter(printprojectstatus=3).count()
        context['closed_projects'] = printprojects.filter(printprojectstatus=4).count()

        context['order_list'] = orders  # .order_by('-rfq_date')

        context['empty_table_text'] = "Geen printprojecten"
        context['empty_table_text_offers'] = "Plaats je eerste offerteaanvraag"
        context['empty_table_text_orders'] = "Plaats je eerste opdracht"

        return context


class PrintprojectDashboard(LoginRequiredMixin, TemplateView):
    template_name = "printprojects/printproject_dashboard.html"
    pk_url_kwarg = 'printprojectstatus_id'
    context_object_name = 'printprojectstatus_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        printprojectstatus_id = kwargs['printprojectstatus_id']
        context = super(PrintprojectDashboard, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        printprojects = PrintProjects.objects.filter(member_id=member_id, active=True)

        update_number_of_open_offers(member_id)

        orders = Orders.objects.filter(member_id=member_id, active=True)
        offers = Offers.objects.filter(member_id=member_id, active=True)

        if printprojectstatus_id == 0:
            empty_table_text = "Start je eerste printproject"
        elif printprojectstatus_id == 1:
            empty_table_text = "Geen open printprojecten"
        elif printprojectstatus_id == 2:
            empty_table_text = "Geen printprojecten in aanvraag"
        elif printprojectstatus_id == 3:
            empty_table_text = "Geen printprojecten in productie"
        elif printprojectstatus_id == 4:
            empty_table_text = "Geen gesloten printprojecten"
        else:
            empty_table_text = "Geen printprojecten"

        context['empty_table_text'] = empty_table_text


        # dashboard lists
        if printprojectstatus_id == 0:
            context['printproject_list'] = printprojects.order_by('-rfq_date')

        else:
            context['printproject_list'] = printprojects.filter(printprojectstatus=printprojectstatus_id).order_by(
                '-rfq_date')
        context['order_list'] = orders  # .order_by('-rfq_date')
        context['offers_list'] = offers  # .order_by('-rfq_date')

        # counts
        context['all_projects'] = printprojects.count()
        context['open_projects'] = printprojects.filter(printprojectstatus=1).count()
        context['rfq_projects'] = printprojects.filter(printprojectstatus=2).count()
        context['prod_projects'] = printprojects.filter(printprojectstatus=3).count()
        context['closed_projects'] = printprojects.filter(printprojectstatus=4).count()

        context['order_list'] = orders  # .order_by('-rfq_date')

        context['printproject_table_title'] = 'Printprojecten'

        return context


class OfferDashboard(LoginRequiredMixin, TemplateView):
    template_name = "orders/order_dashboard.html"
    pk_url_kwarg = 'offer_id'
    context_object_name = 'offer_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        offer_id = kwargs['offer_id']
        context = super(OfferDashboard, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        offers = Offers.objects.filter(member_id=member_id, active=True)

        # dashboard lists
        if offer_id == 0:
            context['offer_list'] = offers  # .order_by('-rfq_date')

        else:
            context['offer_list'] = offers.filter(offer_id=offer_id)  # .order_by('-rfq_date')
        # counts
        context['all_offers'] = offers.count()
        context['open_offers'] = offers.filter(order_status=1).count()
        context['rfq_offers'] = offers.filter(order_status=2).count()
        context['prod_offers'] = offers.filter(order_status=3).count()
        context['closed_offers'] = offers.filter(order_status=4).count()
        return context
