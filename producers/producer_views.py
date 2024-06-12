from django.http import HttpResponseRedirect
from calculations.models import Calculations
from index.categories_groups import open_memberplans
from index.exclusive_functions import define_exclusive_producer_id
from members.crm_functions import *
from api.forms.api_forms import APImanagerForm
from index.forms.note_form import *
from index.forms.relationforms import *
from methods.models import *
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
from index.dq_functions import producer_dq_functions


class ProducerSalesDashboard(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_sales_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def get_context_data(self, **kwargs):
        offerstatus_id = kwargs['offerstatus_id']
        user = self.request.user

        producer_id = user.producer_id
        order_status_id = 0
        update_producersmatch(self.request)
        producer_dq_functions(self.request.user)
        context = super(ProducerSalesDashboard, self).get_context_data(**kwargs)

        context = creatememberplan_context(context, user)
        context = get_offercontext(producer_id, context, offerstatus_id)
        context = get_ordercontext(producer_id, context, order_status_id)
        context['offer_pagination'] = 10
        context['order_pagination'] = 10

        return context


class ProducersDashboard(LoginRequiredMixin, TemplateView):
    template_name = "producers/producers_dashboard.html"
    pk_url_kwarg = 'producerstatus_id'
    context_object_name = 'producerstatus_id'

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(ProducersDashboard, self).get_context_data(**kwargs)
        member_id = user.member_id
        producers = MemberProducerMatch.objects.filter(member_id=member_id).order_by('memberproducerstatus')
        context = creatememberplan_context(context, user)
        context['user'] = user
        # dashboard lists
        context['producers_list'] = producers  # .filter(printprojectstatus=1).order_by('-rfq_date')

        # counts
        context['suppliers_projects'] = 1  # producers.count()

        return context


class ProducerExclusiveClients(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_open_members.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerExclusiveClients, self).get_context_data(**kwargs)
        user = self.request.user
        exclusive_producer_id = define_exclusive_producer_id(self.request.user)
        members = Members.objects.filter(exclusive_producer_id=exclusive_producer_id)
        context = creatememberplan_context(context, user)
        context['user'] = user
        # dashboard lists
        context['members_list'] = members

        # counts
        context['suppliers_projects'] = 1  # producers.count()
        return context


class ProducerOpenMembers(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_open_members.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerOpenMembers, self).get_context_data(**kwargs)
        user = self.request.user
        producer_id = user.producer_id
        open_members = Members.objects.filter(member_plan_id__in=open_memberplans).order_by('company')
        context = creatememberplan_context(context, user)
        context['user'] = user
        # dashboard lists
        context['open_members'] = open_members  # .filter(printprojectstatus=1).order_by('-rfq_date')

        # counts
        context['suppliers_projects'] = 1  # producers.count()

        return context


class ProducerMemberDetails(LoginRequiredMixin, DetailView):
    template_name = "producers/member_datails.html"
    model = Members
    profile = Members

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(ProducerMemberDetails, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        member_id = self.kwargs['pk']
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



class ProducerCalculationErrors(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_error_dashboard.html"
    pk_url_kwarg = 'offerstatus_id'
    context_object_name = 'offerstatus_id'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerCalculationErrors, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        error_calculations = Calculations.objects.filter(producer_id=producer_id).exclude(error=None).exclude(status=4).order_by('calculation_id')

        context['error_calculations'] = error_calculations
        context['offer_pagination'] = 25
        return context


class ProducerOrders(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_order_dashboard.html"
    pk_url_kwarg = 'order_status_id'
    context_object_name = 'order_status_id'

    def get_context_data(self, **kwargs):
        user = self.request.user
        order_status_id = kwargs['order_status_id']
        context = super(ProducerOrders, self).get_context_data(**kwargs)
        producer_id = user.producer_id
        context = creatememberplan_context(context, user)
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
    user = self.request.user
    context = super(CreateNewProducer, self).get_context_data(**kwargs)
    context = creatememberplan_context(context, user)
    context['title'] = "Nieuwe producent aanmaken"
    context['button_text'] = "Producent toevoegen"
    return context


class ProducerDetails(DetailView, LoginRequiredMixin, FormMixin):
    template_name = 'producers/producer_details.html'
    model = Producers
    profile = Producers
    form_class = NoteForm

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.object = None

    def get_success_url(self):
        return reverse('producer_details', kwargs={'pk': self.object.producer_id})

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerDetails, self).get_context_data(**kwargs)
        member_id = user.member_id
        producer_id = self.kwargs['pk']
        producer = Producers.objects.get(producer_id=producer_id)
        context = creatememberplan_context(context, user)
        context['producer'] = producer
        context['order_table_title'] = 'Orders' + " " + str(producer)
        context['empty_table_text_orders'] = "Geen orders geplaaatst bij " + str(producer)
        context['producermatch_list'] = MemberProducerMatch.objects.filter(member_id=member_id, producer_id=producer_id)
        context['producercontact_list'] = ProducerContacts.objects.filter(member_id=member_id, producer_id=producer_id,                                                        active=True)
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

class DeleteProducerContact(TemplateView, LoginRequiredMixin):
    pk_url_kwarg = 'producercontact_id'

    def dispatch(self, request, *args, **kwargs):
        producercontact_id = kwargs.get('producercontact_id')
        producercontact = ProducerContacts.objects.get(producercontact_id=producercontact_id)
        producercontact_deactive = producercontact
        producercontact_deactive.active = False
        producercontact_deactive.save()

        return redirect('/producer_details/' + str(producercontact.producer_id))


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


class CreateNewProducerContact(CreateView, LoginRequiredMixin):
    model = ProducerContacts
    profile = ProducerContacts
    form_class = NewProducerContactForm
    template_name = 'producers/new_producercontact.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        producer_id = self.kwargs['producer_id']
        return '/producer_details/' + str(producer_id)

    def form_valid(self, form):
        producercontact = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
        form.instance.member_id = self.request.user.member_id
        form.instance.producer_id = self.kwargs['producer_id']
        form.instance.producercontact = producercontact
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateNewProducerContact, self).get_context_data(**kwargs)
        producer_id = self.kwargs['producer_id']
        producer_company = Producers.objects.get(producer_id=producer_id).company
        context['title'] = "Nieuw contact: bij " + producer_company
        context['button_text'] = "Contact toevoegen"
        return context


class UpdateProducerContact(UpdateView, LoginRequiredMixin):
    pk_url_kwarg = 'producercontact_id'
    model = ProducerContacts
    profile = ProducerContacts
    form_class = NewProducerContactForm
    template_name = 'producers/new_producercontact.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        producercontact_id = self.kwargs['producercontact_id']
        producer_id = ProducerContacts.objects.get(producercontact_id=producercontact_id).producer_id
        return '/producer_details/' + str(producer_id)

    def form_valid(self, form):
        if form.cleaned_data['first_name'] or form.cleaned_data['last_name']:
            producercontact = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            form.instance.producercontact = producercontact
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateProducerContact, self).get_context_data(**kwargs)
        producercontact_id = self.kwargs['producercontact_id']
        producer_id = ProducerContacts.objects.get(producercontact_id=producercontact_id).producer_id
        producer_company = Producers.objects.get(producer_id=producer_id).company
        context['title'] = "Update contact: bij " + producer_company
        context['button_text'] = "Contact bijwerken"
        return context


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
                productoffering_status = productoffering.availeble
                if not productoffering_status:
                    new_status = True
                else:
                    new_status = False

                update_record = productoffering
                update_record.availeble = new_status
                update_record.save()
        finally:
            pass

        return redirect('/my_account/' + str(self.request.user.member_id))
