from django.http import HttpResponseRedirect
from assets.asset_forms import *
from index.create_context import creatememberplan_context
from index.dq_functions import *
from members.crm_functions import *
from api.forms.api_forms import APImanagerForm
from index.forms.note_form import *
from index.forms.relationforms import *
from methods.models import *
from producers.models import ProducerContacts
from producers.producer_functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, View
from django.views.generic.edit import FormMixin
from profileuseraccount.form_invalids import form_invalid_message


class ProducerTariffs(LoginRequiredMixin, TemplateView):
    template_name = 'producers/producer_tariffs.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerTariffs, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)

        try:
            general_settings = GeneralCalculationSettings.objects.get(producer_id=user.producer_id)
        except GeneralCalculationSettings.DoesNotExist:
            set_calculationsettings(user.producer_id)
            general_settings = GeneralCalculationSettings.objects.get(producer_id=user.producer_id)

        enhancement_tariffs = EnhancementTariffs.objects.filter(producer_id=user.producer_id)
        packaging_tariffs = PackagingTariffs.objects.filter(producer_id=user.producer_id).order_by('packagingoption_id')
        transport_tariffs = TransportTariffs.objects.filter(producer_id=user.producer_id)

        if not enhancement_tariffs:
            update_enhencement_offerings(user.producer_id)
            enhancement_tariffs = EnhancementTariffs.objects.filter(producer_id=user.producer_id)
        enhancement_tariffs = enhancement_tariffs

        if not packaging_tariffs:
            update_packaging_tariffs(user.producer_id)
            packaging_tariffs = PackagingTariffs.objects.filter(producer_id=user.producer_id)
        packaging_tariffs = packaging_tariffs

        if not transport_tariffs:
            update_transport_tariffs(user.producer_id)
            transport_tariffs = TransportTariffs.objects.filter(producer_id=user.producer_id)
        transport_tariffs = transport_tariffs

        context['general_settings'] = general_settings
        context['enhancement_tariffs'] = enhancement_tariffs.order_by('enhancement_id', 'max_sheet_height')
        context['packaging_tariffs'] = packaging_tariffs
        context['transport_tariffs'] = transport_tariffs
        return context


class ProducerTariffsUpdate(LoginRequiredMixin, UpdateView):
    model = GeneralCalculationSettings
    form_class = ProducerUpdateGeneralTariffForm
    pk_url_kwarg = 'settings_id'
    context_object_name = 'settings_id'
    success_url = '/producer_tariffs/'
    template_name = 'producers/producer_tariffs_update.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerTariffsUpdate, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        context['form_title'] = 'Tarieven update '
        context['general_settings'] = GeneralCalculationSettings.objects.get(producer_id=user.producer_id)
        return context


class ProducerEnhancementUpdate(LoginRequiredMixin, UpdateView):
    model = EnhancementTariffs
    form_class = ProducerCreateUpdateEnhancementForm
    pk_url_kwarg = 'enhancementtariff_id'
    context_object_name = 'enhancementtariff_id'
    success_url = '/producer_tariffs/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerEnhancementUpdate, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = self.request.user.producer_id
        enhancementtariff_id = self.kwargs['enhancementtariff_id']
        enhancement = EnhancementTariffs.objects.get(
            enhancementtariff_id=enhancementtariff_id, producer_id=producer_id)
        context['enhancement'] = enhancement
        context['form_title'] = "Veredelingstarief update"
        context['form_header'] = str(enhancement.enhancement) + "- update"
        context['action'] = "update"
        return context


class ProducerEnhancementCreate(LoginRequiredMixin, CreateView):
    model = EnhancementTariffs
    form_class = ProducerCreateUpdateEnhancementForm
    success_url = '/producer_tariffs/'

    def form_valid(self, form):
        producer_id = self.request.user.producer_id
        form.instance.enhancement_id = form.cleaned_data['enhancement_id']
        form.instance.producer_id = producer_id
        form.instance.availeble = True
        form.instance.added_value = True
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerEnhancementCreate, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        context['enhance_choices'] = EnhancementOptions.objects.filter(language_id=user.language_id)
        context['form_title'] = "Veredelingstarief toevoegen"
        context['form_header'] = "Nieuw veredelingstarief toevoegen"
        context['action'] = "create"
        return context


class ProducerPackagingUpdate(LoginRequiredMixin, UpdateView):
    model = PackagingTariffs
    form_class = ProducerUpdatePackagingForm
    pk_url_kwarg = 'packagingtariff_id'
    success_url = '/producer_tariffs/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ProducerPackagingUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        context = creatememberplan_context(context, user)
        producer_id = user.producer_id
        packagingtariff_id = self.kwargs['packagingtariff_id']

        packaging = PackagingTariffs.objects.get(packagingtariff_id=packagingtariff_id,
                                                 producer_id=producer_id)

        packaging_option = PackagingOptions.objects.get(packagingoption_id=packaging.packagingoption_id,
                                                        language_id=user.language_id)
        context['packaging'] = packaging
        context['packaging_option'] = packaging_option
        context['action'] = "Tarief update"
        context['form_title'] = "Verpakkingstarief update"
        context = context
        return context


class ProducerTransportUpdate(LoginRequiredMixin, UpdateView):
    model = PackagingTariffs
    form_class = ProducerUpdatePackagingForm
    pk_url_kwarg = 'transporttariff_id'
    success_url = '/producer_tariffs/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProducerTransportUpdate, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        producer_id = self.request.user.producer_id
        transporttariff_id = self.kwargs['transporttariff_id']

        try:
            context['transport'] = TransportTariffs.objects.get(transporttariff_id=transporttariff_id,
                                                                producer_id=producer_id)
            context = context
        finally:
            pass

        return context


class ProducerMemberDetails(LoginRequiredMixin, DetailView):
    template_name = "producers/member_datails.html"
    model = Members
    profile = Members

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerMemberDetails, self).get_context_data(**kwargs)
        user = self.request.user
        producer_id = user.producer_id
        member_id = self.kwargs['pk']
        turnover = Orders.objects.filter(member_id=member_id, producer_id=producer_id).aggregate(Sum('order_value'))[
            'order_value__sum']
        if turnover:
            turnover = round(turnover, 0)
        else:
            turnover = 0
        context = creatememberplan_context(context, user)
        context['nr_offers'] = Offers.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['nr_offers'] = Orders.objects.filter(member_id=member_id, producer_id=producer_id).count()
        context['turnover'] = turnover
        context['member'] = Members.objects.get(member_id=member_id)
        context['memberaccount_list'] = UserProfile.objects.filter(member_id=user.member_id, active=True)
        return context



class ProducerOrders(LoginRequiredMixin, TemplateView):
    template_name = "producers/producer_order_dashboard.html"
    pk_url_kwarg = 'order_status_id'
    context_object_name = 'order_status_id'

    def get_context_data(self, **kwargs):
        order_status_id = kwargs['order_status_id']
        context = super(ProducerOrders, self).get_context_data(**kwargs)
        user = self.request.user
        producer_id = user.producer_id

        context = get_ordercontext(producer_id, context, order_status_id)
        context['order_pagination'] = 25
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
        context = super(ProducerDetails, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        producer_id = self.kwargs['pk']
        producer = Producers.objects.get(producer_id=producer_id)
        context = creatememberplan_context(context, user)
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
        user = self.request.user
        context = super(CreateNewProducerContact, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
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
        user = self.request.user
        context = super(UpdateProducerContact, self).get_context_data(**kwargs)
        producercontact_id = self.kwargs['producercontact_id']
        producer_id = ProducerContacts.objects.get(producercontact_id=producercontact_id).producer_id
        producer_company = Producers.objects.get(producer_id=producer_id).company
        context = creatememberplan_context(context, user)
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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
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


class ChangeEnhancementAvailability(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        enhancementtariff_id = kwargs.get('enhancementtariff_id')
        producer_id = request.user.producer_id
        try:
            enhancementoffering = EnhancementTariffs.objects.get(enhancementtariff_id=enhancementtariff_id,
                                                                 producer_id=producer_id)
            if enhancementoffering:
                offering_status = enhancementoffering.availeble
                if not offering_status:
                    new_status = True
                else:
                    new_status = False
                enhancementoffering.availeble = new_status
                enhancementoffering.save()
        finally:
            pass
        return redirect('/producer_tariffs/')


class ChangeEnhancementAddedValue(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        enhancementtariff_id = kwargs.get('enhancementtariff_id')
        producer_id = request.user.producer_id
        try:
            enhancementoffering = EnhancementTariffs.objects.get(enhancementtariff_id=enhancementtariff_id,
                                                                 producer_id=producer_id)

            if enhancementoffering:
                offering_status = enhancementoffering.added_value
                if not offering_status:
                    new_status = True
                else:
                    new_status = False
                enhancementoffering.added_value = new_status
                enhancementoffering.save()
        finally:
            pass
        return redirect('/producer_tariffs/')


class ChangePackagingAvailability(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        packagingtariff_id = kwargs.get('packagingtariff_id')
        producer_id = request.user.producer_id
        try:
            packagingoffering = PackagingTariffs.objects.get(packagingtariff_id=packagingtariff_id,
                                                             producer_id=producer_id)

            if packagingoffering:
                offering_status = packagingoffering.availeble
                if not offering_status:
                    new_status = True
                else:
                    new_status = False

                packagingoffering.availeble = new_status
                packagingoffering.save()
        finally:
            pass

        return redirect('/producer_tariffs/')


class ChangeTransportAvailability(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        transporttariff_id = kwargs.get('transporttariff_id')
        producer_id = request.user.producer_id
        try:
            transportoffering = TransportTariffs.objects.get(transporttariff_id=transporttariff_id,
                                                             producer_id=producer_id)

            if transportoffering:
                offering_status = transportoffering.availeble
                if not offering_status:
                    new_status = True
                else:
                    new_status = False

                transportoffering.availeble = new_status
                transportoffering.save()
        finally:
            pass

        return redirect('/producer_tariffs/')


class ChangePMSAvailability(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        setting_id = kwargs.get('setting_id')
        producer_id = request.user.producer_id
        try:
            setting = GeneralCalculationSettings.objects.get(setting_id=setting_id,
                                                             producer_id=producer_id)

            if setting:
                offering_status = setting.pms_offering
                if not offering_status:
                    new_status = True
                else:
                    new_status = False

                setting.pms_offering = new_status
                setting.save()
        finally:
            pass

        return redirect('/producer_tariffs_update/' + str(setting_id))
