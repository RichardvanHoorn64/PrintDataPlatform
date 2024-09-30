from index.categories_groups import *
from index.models import DropdownCountries
from members.crm_functions import *
from api.forms.api_forms import APImanagerForm
from index.forms.relationforms import *
from index.create_context import creatememberplan_context
from printprojects.forms.PrintprojectSalesPice import *
from producers.producer_functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, View
from profileuseraccount.form_invalids import form_invalid_message
from index.dq_functions import producer_dq_functions


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
            status=4).order_by('calculation_id')

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
        context = creatememberplan_context(context, user)
        context = get_ordercontext(producer_id, context, order_status_id)
        context['order_pagination'] = 25
        return context


class CreateNewProducer(CreateView, LoginRequiredMixin):
    model = Producers
    profile = Producers
    form_class = NewProducerForm
    template_name = 'producers/new_producer.html'
    success_url = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

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


class ProducersDashboard(LoginRequiredMixin, TemplateView):
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
