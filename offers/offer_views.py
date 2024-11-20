import random
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from calculations.models import Calculations
from index.forms.form_invalids import form_invalid_message_quotes
from offers.form.offer_forms import *
from offers.models import Offers
from printprojects.models import PrintProjects
from index.create_context import createprintproject_context, creatememberplan_context
from profileuseraccount.models import UserProfile


# Create your views here.
class OfferDetailsMembersView(LoginRequiredMixin, DetailView):
    template_name = 'offers/member_offerdetails.html'
    model = Offers
    profile = Offers
    success_url = reverse_lazy('offers:member_offerdetails')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs['pk']
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        try:
            Offers.objects.get(member_id=user.member_id, offer_id=offer_id)
            return super().dispatch(request, *args, **kwargs)
        except Offers.DoesNotExist:
            return redirect('/no_access/')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        offer_id = self.kwargs['pk']
        user = self.request.user
        offer = Offers.objects.get(member_id=user.member_id, offer_id=offer_id)
        printproject_id = offer.printproject_id

        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)

        producer_id = offer.producer_id
        try:
            calculation = Calculations.objects.get(producer_id=producer_id, printproject_id=printproject_id)
        except Calculations.DoesNotExist:
            calculation = []

        try:
            submit_user = UserProfile.objects.get(id=offer.submit_by_id)
            submit_by = submit_user.first_name + " " + submit_user.last_name + ", " + str(submit_user.member.company)
        except UserProfile.DoesNotExist:
            submit_by = str(offer.producer.company)

        createprintproject_context(context, user, printproject)
        context['calculation'] = calculation
        context['offer'] = offer
        context['printproject'] = printproject
        context['submit_by'] = submit_by
        return context


class OfferProducersFormCheckView(UpdateView):
    template_name = 'offers/offer_producer.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerFormAccess


    def get_success_url(self):
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)
        if offer.offer_key_test == offer.offer_key:
            return reverse_lazy('offer_producers_update_form', args=(self.object.offer_id, self.object.reference_key))
        else:
            return reverse_lazy('offer_producers_form', args=(self.object.offer_id,))

    def dispatch(self, request, *args, **kwargs):
        try:
            offer_id = self.kwargs['pk']
            Offers.objects.get(offer_id=offer_id)
            return super().dispatch(request, *args, **kwargs)
        except Offers.DoesNotExist:
            return redirect('/no_access/')

    def form_valid(self, form):
        form.instance.reference_key = random.randint(10000, 99999)
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_id = self.kwargs['pk']
        context['display_printdetails'] = 0

        user = self.request.user
        offer = Offers.objects.get(offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context['offer'] = offer
        context['explanation_header'] = 'Uitleg'
        context['printproject'] = printproject
        context['title'] = 'Offerte uitbrengen namens ' + str(offer.producer.company)
        context['rfq_project'] = str(printproject.volume) + ' ex' + str(printproject.project_title)
        context['header'] = 'Offerteaanvraag van ' + str(offer.requester) + ' namens ' + str(
            printproject.member.company) + ' uit ' + str(printproject.member.city)
        context['project_summary'] = 'Offerteaanvraag. Productcategorie: ' + str(
            offer.productcategory) + '. Project ' + str(printproject.volume) + ' ex. ' + str(printproject.project_title)
        return context


class OfferMembersUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'offers/offer_member_update.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def get_success_url(self):
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)
        printproject_id = PrintProjects.objects.get(printproject_id=offer.printproject_id).printproject_id
        return '/printproject_details/' + str(printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs['pk']

        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        elif not Offers.objects.filter(member_id=user.member_id, offer_id=offer_id).exists():
            return redirect('/no_access/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.offerstatus_id = 2
        form.instance.submit_date = datetime.now()
        form.instance.submit_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("member offer update form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        user = self.request.user
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)

        try:
            submit_user = UserProfile.objects.get(id=offer.submit_by_id)
            submit_by = submit_user.first_name + " " + submit_user.last_name + ", " + str(submit_user.member.company)
        except UserProfile.DoesNotExist:
            submit_by = str(offer.producer.company)

        offer = Offers.objects.get(producer_id=user.producer_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['title'] = "Invoer / update aanbieding van: " + str(offer.producer.company)
        context['offer'] = offer
        context['printproject'] = printproject
        context['submit_by'] = submit_by
        return context


class OfferProducersOpenUpdate(UpdateView):
    template_name = 'offers/offer_producer.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerForm
    success_url = reverse_lazy('thanks_submit_offer')

    def dispatch(self, request, *args, **kwargs):
        # check reference key
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)
        reference_key = self.kwargs['reference_key']
        if offer.reference_key != reference_key:
            return redirect('/no_access/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.offerstatus_id = 2
        form.instance.offer_date = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)
        if offer.offer_key_test == offer.offer_key:
            context['display_printdetails'] = 1
        else:
            context['display_printdetails'] = 0

        offer = Offers.objects.get(offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        user = UserProfile.objects.get(id=printproject.user.id)
        context = createprintproject_context(context, user, printproject)
        context['title'] = "Invoer / update aanbieding aan: " + str(offer.member.company)
        context['key'] = True
        context['offer'] = offer
        context['printproject'] = printproject
        return context


class OfferProducersUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'offers/offer_producer.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            return reverse_lazy('home')
        else:
            return reverse_lazy('thanks_submit_offer')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs['pk']

        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        # check access
        elif not Offers.objects.filter(producer_id=user.producer_id, offer_id=offer_id).exists():
            return redirect('/no_access/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.offerstatus_id = 2
        form.instance.submit_date = datetime.now()
        form.instance.submit_by = self.request.user.id
        form.instance.offer_date = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        user = self.request.user
        offer_id = self.kwargs['pk']

        offer = Offers.objects.get(producer_id=user.producer_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['title'] = "Invoer / update aanbieding aan: " + str(offer.member.company)
        context['key'] = False
        context['offer'] = offer
        context['printproject'] = printproject
        context['display_printdetails'] = 1

        return context


class DenyOfferView(View):
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def dispatch(self, request, *args, **kwargs):
        try:
            offer_id = self.kwargs['pk']
            offer = Offers.objects.get(offer_id=offer_id)
            offer.offerstatus_id = 4  # denied
            offer.offer_date = datetime.now()
            offer.save()
        finally:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CloseOfferView(View):
    model = Offers
    profile = Offers

    def dispatch(self, request, *args, **kwargs):
        try:
            offer_id = self.kwargs['pk']
            offer = Offers.objects.get(offer_id=offer_id)
            offer.delete()
        finally:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CloseErrorCalculationView(View):
    model = Calculations
    profile = Calculations

    def dispatch(self, request, *args, **kwargs):
        try:
            calculation_id = self.kwargs['pk']
            calculation = Calculations.objects.get(calculation_id=calculation_id)
            calculation.status = 4  # closed
            calculation.save()
        finally:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class HandleOfferView(LoginRequiredMixin, View):
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def dispatch(self, request, *args, **kwargs):
        offerstatus_id = self.kwargs['offerstatus_id']
        try:
            offer_id = self.kwargs['pk']
            offer = Offers.objects.get(offer_id=offer_id)
            offer.offerstatus_id = offerstatus_id
            offer.active = False
            offer.offer_date = None
            offer.save()
        finally:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ThanksSubmitOffer(TemplateView):
    template_name = 'thanks_submit_offer.html'

