import random
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from index.forms.form_invalids import form_invalid_message_quotes
from offers.form.offer_forms import *
from offers.models import Offers
from printprojects.models import PrintProjects
from printprojects.printproject_context import createprintproject_context


# Create your views here.
class OfferDetailsMembersView(LoginRequiredMixin, DetailView):
    template_name = 'offers/offer_member.html'
    model = Offers
    profile = Offers

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_id = self.kwargs['pk']
        user = self.request.user
        offer = Offers.objects.get(member_id=user.member_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['offer'] = offer
        return context


class OfferProducersFormCheckView(LoginRequiredMixin, UpdateView):
    template_name = 'offers/offer_producucer.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerFormAcces

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        offer_id = self.kwargs['pk']
        offer = Offers.objects.get(offer_id=offer_id)
        if offer.offer_key_test == offer.offer_key:
            return reverse_lazy('offer_producers_update_form', args=(self.object.offer_id, self.object.reference_key))
        else:
            return reverse_lazy('offer_producers_form', args=(self.object.offer_id,))

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
        context['display'] = 0
        context['display_access'] = 1

        user = self.request.user
        offer = Offers.objects.get(member_id=user.member_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['offer'] = offer
        context['printproject'] = printproject

        return context


class OfferProducersUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'offers/offer_producucer.html'
    model = Offers
    profile = Offers
    form_class = OfferProducerForm
    success_url = reverse_lazy('thanks_submit_offer')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
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
        user = self.request.user
        offer_id = self.kwargs['pk']

        offer = Offers.objects.get(producer_id=user.producer_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['key'] = False
        context['offer'] = offer
        context['printproject'] = printproject
        context['display_access'] = 0
        context['display'] = 1

        return context


class OfferProducersOpenUpdateView(UpdateView):
    template_name = 'offers/offer_producucer.html'
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
            context['display'] = 1
        else:
            context['display'] = 0
        context['display_access'] = 0
        user = self.request.user
        offer = Offers.objects.get(member_id=user.member_id, offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)
        context = createprintproject_context(context, user, printproject)
        context['key'] = True
        context['offer'] = offer
        context['printproject'] = printproject
        return context


class DenyOfferView(View):
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def dispatch(self, request, *args, **kwargs):
        try:
            offer_id = self.kwargs['pk']
            offer = Offers.objects.get(offer_id=offer_id)
            offer.offerstatus_id = 3
            offer.offer_date = datetime.now()
            offer.save()
        finally:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CloseOfferView(View):
    model = Offers
    profile = Offers
    form_class = OfferProducerForm

    def dispatch(self, request, *args, **kwargs):
        try:
            offer_id = self.kwargs['pk']
            offer = Offers.objects.get(offer_id=offer_id)
            offer.offerstatus_id = 4  # closed
            offer.offer_date = datetime.now()
            offer.save()
        finally:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class HandleOfferView(LoginRequiredMixin, TemplateView):
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
