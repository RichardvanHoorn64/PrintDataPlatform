from index.categories_groups import *
from index.display_functions import display_country, display_producercategories
from index.models import DropdownCountries
from index.create_context import creatememberplan_context
from printprojects.forms.ProducerMemberSalesPrice import *
from profileuseraccount.form_invalids import form_invalid_message
from members.crm_functions import *
from api.forms.api_forms import APImanagerForm
from index.forms.note_form import *
from index.forms.relationforms import *
from producers.producer_functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import *
from django.views.generic.edit import FormMixin


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
        context = super(ProducerDetails, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        producer_id = self.kwargs['pk']
        producer = Producers.objects.get(producer_id=producer_id)
        context = creatememberplan_context(context, user)
        # product_categories = get_producercategories(producer_id)
        context['producer'] = producer
        context['order_table_title'] = 'Orders' + " " + str(producer)
        context['empty_table_text_orders'] = "Geen orders geplaaatst bij " + str(producer)
        context['producermatch_list'] = MemberProducerMatch.objects.filter(member_id=member_id, producer_id=producer_id)
        context['producercontact_list'] = ProducerContacts.objects.filter(member_id=member_id, producer_id=producer_id,
                                                                          active=True)
        context['order_list'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id)
        context['producer_notes'] = Notes.objects.filter(member_id=member_id, producer_id=producer_id)
        # context['product_categories'] = product_categories
        context['producer_product_categories'] = display_producercategories(producer_id)

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
        context['producer_country'] = display_country(producer.country_code, user.language_id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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


class ProducerOpenMembers(LoginRequiredMixin, TemplateView):
    template_name = "producers/tables/producer_members.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerOpenMembers, self).get_context_data(**kwargs)
        user = self.request.user
        producer = Producers.objects.get(producer_id=user.producer_id)
        producer_id = user.producer_id
        members = MemberProducerMatch.objects.filter(producer_id=producer_id, member_accept=True,
                                                     member__member_plan__id__in=non_exclusive_memberplans).order_by(
            'member__company')

        context = creatememberplan_context(context, user)
        context['members'] = members
        context['title'] = 'Klanten via PrintDataPlatform'
        context['calculation_module'] = producer.calculation_module
        context['exclusive_module'] = producer.exclusive_module
        context['add_members'] = False
        context['open_members'] = True
        context['exclusive_members'] = False
        return context


class ProducerMemberDetails(LoginRequiredMixin, DetailView):
    template_name = "producers/member_details_contacts.html"
    model = Members
    profile = Members

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

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(ProducerMemberDetails, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        member_id = self.kwargs['pk']

        context['nr_rfq'] = Offers.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['nr_offers'] = Offers.objects.filter(member_id=member_id, producer_id=producer_id,
                                                     offerstatus_id__in=[2, 3, 4]).count()
        context['nr_orders'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['member'] = Members.objects.get(member_id=member_id)
        context['memberaccount_list'] = UserProfile.objects.filter(member_id=member_id, active=True)
        return context


class ProducerCalculationErrors(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_error_dashboard.html"
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
        user = self.request.user
        context = super(ProducerCalculationErrors, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        error_calculations = Calculations.objects.filter(producer_id=producer_id).exclude(error=None).exclude(
            status=4).order_by('-offer_date')

        context['error_calculations'] = error_calculations
        context['offer_pagination'] = 25
        return context


class ProducerOrders(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_order_dashboard.html"
    pk_url_kwarg = 'order_status_id'
    context_object_name = 'order_status_id'

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
        user = self.request.user
        order_status_id = kwargs['order_status_id']
        context = super(ProducerOrders, self).get_context_data(**kwargs)
        producer_id = user.producer_id
        producer = Producers.objects.get(producer_id=producer_id)
        context = creatememberplan_context(context, user)
        context = get_ordercontext(producer, context, order_status_id, dashboard=False)
        context['order_pagination'] = 25
        return context


class CreateNewProducer(CreateView, LoginRequiredMixin):
    model = Producers
    profile = Producers
    form_class = NewProducerForm
    template_name = 'producers/new_producer.html'
    success_url = '/producer_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['e_mail_general']
        country_code = form.cleaned_data['country_code']
        try:
            language_id = DropdownCountries.objects.get(country_code=country_code).language_id
        except DropdownCountries.DoesNotExist:
            language_id = 1
        form.instance.uploaded_by = self.request.user.id
        form.instance.member_plan_id = 5
        form.instance.language_id = language_id
        form.instance.e_mail_rfq = email
        form.instance.e_mail_offers = email
        form.instance.e_mail_orders = email
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        countries = DropdownCountries.objects.all().order_by('country_id')
        context = super(CreateNewProducer, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        context['title'] = "Nieuwe producent aanmaken"
        context['button_text'] = "Producent toevoegen"
        context['countries'] = countries
        return context


class MySuppliers(LoginRequiredMixin, TemplateView):
    template_name = "producers/producers_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(MySuppliers, self).get_context_data(**kwargs)
        member_id = user.member_id
        producers = MemberProducerMatch.objects.filter(member_id=member_id).order_by(
            'memberproducerstatus')
        context = creatememberplan_context(context, user)
        context['user'] = user
        # dashboard lists
        context['preferred_suppliers'] = producers.filter(memberproducerstatus_id=1)
        context['available_suppliers'] = producers.exclude(memberproducerstatus_id=1)

        # counts
        context['suppliers_projects'] = 1  # producers.count()
        context['page_title'] = 'Producenten ' + str(user.company)

        return context


class ProducerPricingUpdateView(UpdateView, LoginRequiredMixin):
    pk_url_kwarg = 'memberproducermatch_id'
    model = MemberProducerMatch
    profile = MemberProducerMatch
    form_class = MemberProducerPricingForm
    template_name = "producers/pricing_per_member_dashboard.html"

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

    def get_success_url(self):
        memberproducermatch_id = self.kwargs['memberproducermatch_id']
        return '/pricing_dashboard/' + str(memberproducermatch_id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        memberproducermatch_id = self.kwargs['memberproducermatch_id']
        match = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        user = self.request.user
        context = super(ProducerPricingUpdateView, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        member = Members.objects.get(member_id=match.member_id)
        products = ProductCategory.objects.filter(language_id=user.language_id)
        context['product_categories'] = get_producercategories(producer_id)
        context['products'] = products.order_by('productcategory_id')
        context['member'] = member
        context['title'] = "Update contact: bij "
        context['button_text'] = "Tarieven updaten"
        return context


class ProducerCloseOrderView(LoginRequiredMixin, View):
    model = Orders
    profile = Orders

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        elif not user.member.member_plan_id == 4:
            return redirect('/wait_for_approval/')
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
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        elif not user.member.member_plan_id == 4:
            return redirect('/wait_for_approval/')
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
