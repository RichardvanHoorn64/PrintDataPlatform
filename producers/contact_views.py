from index.forms.accountforms import ProducerCommunicationForm
from profileuseraccount.form_invalids import form_invalid_message
from index.forms.note_form import *
from index.forms.relationforms import *
from index.create_context import creatememberplan_context
from producers.producer_functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
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
        context = super(UpdateProducerContact, self).get_context_data(**kwargs)
        producercontact_id = self.kwargs['producercontact_id']
        producer_id = ProducerContacts.objects.get(producercontact_id=producercontact_id).producer_id
        producer_company = Producers.objects.get(producer_id=producer_id).company
        context['title'] = "Update contact: bij " + producer_company
        context['button_text'] = "Contact bijwerken"
        return context


class DeleteProducerContact(TemplateView, LoginRequiredMixin):
    pk_url_kwarg = 'producercontact_id'

    def dispatch(self, request, *args, **kwargs):
        producercontact_id = kwargs.get('producercontact_id')
        producercontact = ProducerContacts.objects.get(producercontact_id=producercontact_id)
        producercontact_deactive = producercontact
        producercontact_deactive.active = False
        producercontact_deactive.save()

        return redirect('/producer_details/' + str(producercontact.producer_id))


class UpdateProducerCommunication(UpdateView, LoginRequiredMixin):
    pk_url_kwarg = 'producer_id'
    model = Producers
    profile = Producers
    form_class = ProducerCommunicationForm
    template_name = 'producers/producer_communications_update.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        producer_id = self.request.user.producer_id
        return '/my_account/' + str(producer_id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateProducerCommunication, self).get_context_data(**kwargs)
        producer_id = self.request.user.producer_id
        producer_company = Producers.objects.get(producer_id=producer_id).company
        context['form_title'] = "Update email communicatie: bij " + producer_company
        context['title'] = "Update contact: bij " + producer_company
        context['button_text'] = "Communicatie bijwerken"
        return context
