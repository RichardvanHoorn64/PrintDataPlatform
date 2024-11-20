from django.shortcuts import redirect
from index.create_context import creatememberplan_context
from index.dq_functions import producer_dq_functions
from members.crm_functions import update_number_of_open_offers, update_producersmatch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from offers.models import *
from orders.models import Orders
from printprojects.models import *
from index.categories_groups import *
from producers.producer_functions import get_offercontext, get_ordercontext


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
        user = self.request.user
        context = super(PrintDataPlatformDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        member_id = user.member_id
        member_plan_id = user.member_plan_id
        update_number_of_open_offers(member_id)

        printprojects = PrintProjects.objects.filter(member_id=member_id, active=True)
        orders = Orders.objects.filter(member_id=member_id, active=True)
        offers = Offers.objects.filter(member_id=member_id, active=True).exclude(offerstatus_id=4)
        # text

        printproject_table_title = 'Laatste 10 printprojecten'
        offer_table_title = 'Laatste 10 aanbiedingen'
        order_table_title = 'Laatste 10 orders'
        dashboard_title = "PrintDataPlatform dashboard"
        start_printproject = 'start printproject'
        start_project_buttontext = 'Start project'

        context['user'] = user
        context['member_plan_id'] = member_plan_id

        # store
        categories_available = categories_all

        # store image location on Azure
        blob_loc = 'https://printdatastorage.blob.core.windows.net/media/'
        store = "/store/"
        context['img_1'] = blob_loc + str(1) + store + 'plano.png'
        context['img_2'] = blob_loc + str(1) + store + 'folders.png'
        context['img_3'] = blob_loc + str(1) + store + 'selfcovers.png'
        context['img_4'] = blob_loc + str(1) + store + 'geniet_met_omslag.png'
        context['img_5'] = blob_loc + str(1) + store + 'brochures.png'

        # dashboard lists and titles
        context['dashboard_title'] = dashboard_title
        context['offer_table_title'] = offer_table_title
        context['categories_available'] = categories_available
        context['start_printproject'] = start_printproject
        context['start_project_buttontext'] = start_project_buttontext
        context['printproject_list'] = printprojects.order_by('-rfq_date')[:10]
        context['order_list'] = orders.order_by('-orderdate')[:10]
        context['offers_list'] = offers.order_by('-offer_date')[:10]

        # text
        context['printproject_table_title'] = printproject_table_title
        context['offer_table_title'] = offer_table_title
        context['order_table_title'] = order_table_title
        context['order_list'] = orders  # .order_by('-rfq_date')

        context['empty_table_text'] = "Geen printprojecten"
        context['empty_table_text_offers'] = "Plaats je eerste offerteaanvraag"
        context['empty_table_text_orders'] = "Plaats je eerste opdracht"
        context['offer_pagination'] = 10
        context['order_pagination'] = 10
        context['dashboard'] = True

        return context


class ProducerSalesDashboard(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_sales_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        elif not user.member.member_plan_id == 4:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        offerstatus_id = kwargs['offerstatus_id']
        user = self.request.user
        producer = Producers.objects.get(producer_id=user.producer_id)

        order_status_id = 0
        update_producersmatch(self.request)
        producer_dq_functions(self.request.user)
        context = super(ProducerSalesDashboard, self).get_context_data(**kwargs)

        context = creatememberplan_context(context, user)
        context = get_offercontext(producer, context, offerstatus_id, dashboard=True)
        context = get_ordercontext(producer, context, order_status_id, dashboard=True)
        context['offer_pagination'] = 10
        context['order_pagination'] = 10
        context['dashboard'] = True
        return context


class PrintprojectDashboard(LoginRequiredMixin, TemplateView):
    template_name = "printprojects/printproject_dashboard.html"
    pk_url_kwarg = 'printprojectstatus_id'
    context_object_name = 'printprojectstatus_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        printprojectstatus_id = kwargs['printprojectstatus_id']
        context = super(PrintprojectDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        member_id = user.member_id

        # printprojects
        printprojects = PrintProjects.objects.filter(member_id=member_id, active=True)

        update_number_of_open_offers(member_id)

        orders = Orders.objects.filter(member_id=member_id, active=True)
        offers = Offers.objects.filter(member_id=member_id, active=True).exclude(offerstatus_id=4)

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
        context['order_list'] = orders.order_by('-order_id')
        context['offers_list'] = offers.order_by('-offer_date')

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
    template_name = "offers/offer_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        offerstatus_id = kwargs['offerstatus_id']
        context = super(OfferDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        member_id = user.member_id

        offers = Offers.objects.filter(member_id=member_id, active=True).order_by('-offer_id')
        if offerstatus_id == 0:
            offer_table_title = 'Alle aanbiedingen'
        else:
            offers = offers.filter(offerstatus=offerstatus_id)
            try:
                offerstatus = Offerstatus.objects.get(offerstatus_id=offerstatus_id).offerstatus
            except Offerstatus.DoesNotExist:
                offerstatus = None
            offer_table_title = 'Aanbiedingen, status ' + str(offerstatus.lower())

        # dashboard lists
        context['offers_list'] = offers
        context['offer_table_title'] = offer_table_title
        # counts
        context['all_offers'] = offers.count()
        context['open_offers'] = offers.filter(offerstatus=1).count()
        context['submitted_offers'] = offers.filter(offerstatus=2).count()
        context['production_offers'] = offers.filter(offerstatus=3).count()
        context['denied_offers'] = offers.filter(offerstatus=4).count()
        return context
