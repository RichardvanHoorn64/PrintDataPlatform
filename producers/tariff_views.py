from django.http import HttpResponseRedirect
from assets.asset_forms import *
from index.create_context import creatememberplan_context
from index.dq_functions import *
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
from django.views.generic import *
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
            update_enhancement_offerings(user.producer_id)
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
    model = TransportTariffs
    form_class = ProducerUpdateTransportForm
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
        context['form_title'] = 'Transport - Tarief update'
        transporttariff_id = self.kwargs['transporttariff_id']

        try:
            context['transport'] = TransportTariffs.objects.get(transporttariff_id=transporttariff_id,
                                                                producer_id=producer_id)
            context = context
        finally:
            pass

        return context


class ChangeMemberProducerStatus(View, LoginRequiredMixin):
    pk_url_kwarg = 'printprojectmatch_id'
    context_object_name = 'memberproducermatch_id'

    def dispatch(self, request, *args, **kwargs):
        referer = request.META.get("HTTP_REFERER")
        user = self.request.user
        memberproducermatch_id = kwargs.get('memberproducermatch_id')
        memberproducerstatus_id = kwargs.get('memberproducerstatus_id')

        # Update MemberProducerMatch
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        memberproducermatch.memberproducerstatus_id = memberproducerstatus_id
        memberproducermatch.save()

        # Update  PrintProjectMatches
        update_projectmatches = PrintProjectMatch.objects.filter(member_id=user.member_id,
                                                                 producer_id=memberproducermatch.producer_id)
        for projectmatch in update_projectmatches:
            projectmatch.memberproducerstatus_id = memberproducerstatus_id
            projectmatch.save()

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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        memberproducermatch_id = self.kwargs['pk']
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        context['memberproducermatch'] = memberproducermatch

        return context


class ProducerMemberAccept(LoginRequiredMixin, View):
    success_url = '/member_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        memberproducermatch_id = self.kwargs['pk']
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        if memberproducermatch.producer_accept:
            memberproducermatch.producer_accept = False
        else:
            memberproducermatch.producer_accept = True
        memberproducermatch.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProducerMemberAutoQuote(LoginRequiredMixin, View):
    success_url = '/member_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        memberproducermatch_id = self.kwargs['pk']
        memberproducermatch = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
        if memberproducermatch.auto_quote:
            memberproducermatch.auto_quote = False
        else:
            memberproducermatch.auto_quote = True
        memberproducermatch.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ChangeTransportAddedValue(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        transporttariff_id = kwargs.get('transporttariff_id')
        producer_id = request.user.producer_id
        try:
            transportoffering = TransportTariffs.objects.get(transporttariff_id=transporttariff_id,
                                                                 producer_id=producer_id)

            if transportoffering:
                offering_status = transportoffering.added_value
                if not offering_status:
                    new_status = True
                else:
                    new_status = False
                transportoffering.added_value = new_status
                transportoffering.save()
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
