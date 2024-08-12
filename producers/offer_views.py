from django.http import HttpResponseRedirect
from materials.models import *
from members.crm_functions import *
from api.forms.api_forms import APImanagerForm
from index.forms.note_form import *
from index.forms.relationforms import *
from index.categories_groups import *
from methods.models import *
from printprojects.forms.PrintprojectSalesPice import PrintProjectPriceUpdateForm
from index.create_context import createprintproject_context, creatememberplan_context
from producers.models import ProducerContacts
from producers.producer_functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, View
from django.views.generic.edit import FormMixin
from profileuseraccount.form_invalids import form_invalid_message


class ProducerOfferDetails(UpdateView, LoginRequiredMixin):
    template_name = 'producers/producer_offer_details.html'
    pk_url_kwarg = 'offer_id'
    model = Offers
    form_class = PrintProjectPriceUpdateForm

    def get_success_url(self):
        offer_id = self.kwargs['offer_id']
        return '/printproject_details/' + str(offer_id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        offer_id = self.kwargs['offer_id']
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        offer = Offers.objects.get(offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context['offer'] = offer
        context['printproject'] = printproject
        context = createprintproject_context(context, user, printproject)
        return context


class ProducerErrorDetails(TemplateView, LoginRequiredMixin):
    template_name = 'producers/producer_error_details.html'
    pk_url_kwarg = 'offer_id'
    model = Calculations
    form_class = PrintProjectPriceUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        calculation_id = self.kwargs['calculation_id']
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        calculation = Calculations.objects.get(calculation_id=calculation_id)
        printproject = PrintProjects.objects.get(printproject_id=calculation.printproject_id)
        context['printproject'] = printproject
        context['calculation'] = calculation
        context = createprintproject_context(context, user, printproject)
        return context


class ProducerCalculationDetails(LoginRequiredMixin, TemplateView):
    template_name = 'producers/producer_calculation_details.html'
    pk_url_kwarg = 'calculation_id'
    context_object_name = 'calculation_id'
    model = PrintProjects
    form_class = PrintProjectPriceUpdateForm

    def dispatch(self, request, *args, **kwargs):
        calculation_id = self.kwargs['calculation_id']
        user = self.request.user
        try:
            Calculations.objects.get(calculation_id=calculation_id, producer_id=user.producer_id)
            return super().dispatch(request, *args, **kwargs)
        except Calculations.DoesNotExist:
            return redirect('/no_access/')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        calculation_id = self.kwargs['calculation_id']
        calculation = Calculations.objects.get(calculation_id=calculation_id, producer_id=user.producer_id)
        printproject = PrintProjects.objects.get(printproject_id=calculation.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['calculation'] = calculation
        context['assortiment_item'] = calculation.assortiment_item
        context['printproject'] = printproject

        if calculation.productcategory_id in categories_brochures_all:
            try:
                paper_booklet = PaperCatalog.objects.get(paperspec_id=calculation.paperspec_id_booklet)
                context['paper_booklet'] = paper_booklet
            except PaperCatalog.DoesNotExist:
                context['paper_booklet'] = []

        if calculation.productcategory_id in categories_brochures_cover:
            try:
                paper_cover = PaperCatalog.objects.get(paperspec_id=calculation.paperspec_id_cover)
                context['paper_cover'] = paper_cover
            except PaperCatalog.DoesNotExist:
                context['paper_cover'] = 0


        return context


class ProducerMemberDashboard(LoginRequiredMixin, TemplateView):
    template_name = "producers/tables/producer_members.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(ProducerMemberDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        members = MemberProducerMatch.objects.filter(producer_id=producer_id).order_by('memberproducerstatus')

        context['user'] = user
        # dashboard lists
        context['members_list'] = members  # .filter(printprojectstatus=1).order_by('-rfq_date')

        # counts
        context['suppliers_projects'] = 1  # producers.count()

        return context


class ProducerMemberDetails(LoginRequiredMixin, DetailView):
    template_name = "producers/member_details_contacts.html"
    model = Members
    profile = Members

    def get_context_data(self, *args, **kwargs):
        member_id = self.kwargs['pk']
        user = self.request.user
        context = super(ProducerMemberDetails, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id

        turnover = Orders.objects.filter(member_id=member_id, producer_id=producer_id).aggregate(Sum('order_value'))[
            'order_value__sum']
        if turnover:
            turnover = round(turnover, 0)
        else:
            turnover = 0

        context['nr_offers'] = Offers.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['nr_offers'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id).count()

        context['turnover'] = turnover

        context['member'] = Members.objects.get(member_id=member_id)
        context['memberaccount_list'] = UserProfile.objects.filter(member_id=user.member_id, active=True)
        return context


class ProducerSalesDashboard(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_sales_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def get_context_data(self, **kwargs):
        offerstatus_id = kwargs['offerstatus_id']
        user = self.request.user
        context = super(ProducerSalesDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        order_status_id = 0

        context = get_offercontext(producer_id, context, offerstatus_id)
        context = get_ordercontext(producer_id, context, order_status_id)
        context['offer_pagination'] = 10
        context['order_pagination'] = 10

        return context


class ProducerOffers(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_offer_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def get_context_data(self, **kwargs):
        offerstatus_id = kwargs['offerstatus_id']
        user = self.request.user
        context = super(ProducerOffers, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        context = get_offercontext(user.producer_id, context, offerstatus_id)
        context['offer_pagination'] = 25
        return context


class ProducerOrders(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_order_dashboard.html"
    pk_url_kwarg = 'order_status_id'
    context_object_name = 'order_status_id'

    def get_context_data(self, **kwargs):
        order_status_id = kwargs['order_status_id']
        user = self.request.user
        context = super(ProducerOrders, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        user = self.request.user
        producer_id = user.producer_id

        context = get_ordercontext(producer_id, context, order_status_id)
        context['order_pagination'] = 25
        return context


class CreateNewProducer(CreateView, LoginRequiredMixin):
    model = Producers
    profile = Producers
    form_class = NewProducerForm
    template_name = 'producers/new_producer.html'
    success_url = '/producer_dashboard/0'

    def form_valid(self, form):
        user = self.request.user
        form.instance.language_id = user.language_id
        return super().form_valid(form)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))


def get_context_data(self, **kwargs):
    context = super(CreateNewProducer, self).get_context_data(**kwargs)
    context['title'] = "Nieuwe producent aanmaken"
    context['button_text'] = "Producent toevoegen"
    return context


class ProducerDetails(DetailView, LoginRequiredMixin, FormMixin):
    template_name = 'producers/producer_details.html'
    model = Producers
    profile = Producers
    form_class = NoteForm

    def get_success_url(self):
        return reverse('producer_details', kwargs={'pk': self.object.producer_id})

    def get_context_data(self, **kwargs):
        context = super(ProducerDetails, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        producer_id = self.kwargs['pk']
        producer = Producers.objects.get(producer_id=producer_id)
        context['producer'] = producer
        context['order_table_title'] = 'Orders' + " " + str(producer)
        context['empty_table_text_orders'] = "Geen orders geplaaatst bij " + str(producer)
        context['producermatch_list'] = MemberProducerMatch.objects.filter(member_id=member_id, producer_id=producer_id)
        context['producercontact_list'] = ProducerContacts.objects.filter(member_id=member_id, producer_id=producer_id,
                                                                          active=True)
        context['order_list'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id)
        context['producer_notes'] = Notes.objects.filter(member_id=member_id, producer_id=producer_id)
        context['product_categories'] = get_producercategories(producer_id)

        number_of_orders = Orders.objects.filter(member_id=member_id, producer_id=producer_id).count()
        if number_of_orders > 0:
            order_value = \
                Orders.objects.filter(member_id=member_id, producer_id=producer_id).aggregate(Sum('order_value'))[
                    'order_value__sum']
        else:
            order_value = 0

        # counts
        context['count_offers_by_member'] = Offers.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['count_orders_by_member'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['order_value_by_member'] = order_value
        return context

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        note = form.save(commit=False)
        note.member_id = user.member_id
        note.producer_id = self.kwargs['pk']
        note.user_id = user.id
        note.save()
        return super(ProducerDetails, self).form_valid(form)


class ChangeMemberProducerStatus(View, LoginRequiredMixin):
    pk_url_kwarg = 'memberproducerstatus_id'
    context_object_name = 'memberproducerstatus_id'

    def dispatch(self, request, *args, **kwargs):
        referer = request.META.get("HTTP_REFERER")
        memberproducermatch_id = kwargs.get('memberproducermatch_id')
        memberproducerstatus_id = kwargs.get('memberproducerstatus_id')
        update_record = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        update_record.memberproducerstatus_id = memberproducerstatus_id
        update_record.save()
        return HttpResponseRedirect(referer)




class ProducerCloseOrderView(LoginRequiredMixin, View):
    model = Orders
    profile = Orders

    def dispatch(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Orders.objects.get(order_id=order_id)

        if order.order_status_id == 1:
            order.order_status_id = 3
        else:
            order.order_status_id = 5
        order.save()
        return redirect('/producer_sales_dashboard/0')


class ProducerAcceptOrderView(LoginRequiredMixin, View):
    model = Orders
    profile = Orders

    def dispatch(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Orders.objects.get(order_id=order_id)
        order.order_status_id = 2
        order.save()
        return redirect('/producer_sales_dashboard/0')


class APIproducerManager(LoginRequiredMixin, UpdateView):
    model = MemberProducerMatch
    profile = MemberProducerMatch
    template_name = 'producers/api_manager.html'
    form_class = APImanagerForm
    success_url = '/member_dashboard/'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memberproducermatch_id = self.kwargs['pk']
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        context['memberproducermatch'] = memberproducermatch

        return context


class APIproducerAccept(LoginRequiredMixin, View):
    success_url = '/member_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        memberproducermatch_id = self.kwargs['pk']
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        if memberproducermatch.producer_accept:
            memberproducermatch.producer_accept = False
        else:
            memberproducermatch.producer_accept = True
        memberproducermatch.save()
        return redirect('/member_dashboard/')


class ProducerProductofferingSwitch(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        setting_id = kwargs.get('setting_id')
        producer_id = request.user.producer_id
        try:
            productoffering = ProducerProductOfferings.objects.get(setting_id=setting_id, producer_id=producer_id)

            if productoffering:
                offering_status = productoffering.availeble
                if not offering_status:
                    new_status = True
                else:
                    new_status = False

                productoffering.availeble = new_status
                productoffering.save()
        finally:
            pass

        return redirect('/my_account/' + str(self.request.user.member_id))
