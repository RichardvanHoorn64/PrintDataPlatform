from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from datetime import datetime
from members.crm_functions import update_clientdashboard
from index.forms.note_form import *
from index.forms.relationforms import *
from methods.models import Notes
from orders.models import Orders
from profileuseraccount.form_invalids import form_invalid_message
from printprojects.models import *


class ClientDashboard(LoginRequiredMixin, TemplateView):
    template_name = "clients/clients_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        update_clientdashboard(self.request.user.member_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientDashboard, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id

        Clients.objects.filter(member_id=member_id)
        context['clients_list'] = Clients.objects.filter(member_id=member_id)
        context['open_orders'] = Orders.objects.filter(order_status=1).count()
        return context


class ClientDetails(DetailView, LoginRequiredMixin, FormMixin):
    # template_name = 'clients/client_details.html'
    template_name = 'clients/client_details.html'
    model = Clients
    profile = Clients
    form_class = NoteForm

    def get_success_url(self):
        return reverse('client_details', kwargs={'pk': self.object.client_id})

    def get_context_data(self, **kwargs):
        context = super(ClientDetails, self).get_context_data(**kwargs)
        user = self.request.user
        member_id = user.member_id
        client_id = self.kwargs['pk']
        client = Clients.objects.get(member_id=member_id, client_id=client_id)

        printprojects = PrintProjects.objects.filter(member_id=member_id, active=True, client_id=client_id)
        orders = Orders.objects.filter(member_id=member_id, active=True, client_id=client_id)

        context['client'] = client
        context['clientcontact_list'] = ClientContacts.objects.filter(member_id=member_id, client_id=client_id)
        context['printproject_list'] = PrintProjects.objects.filter(member_id=member_id, client_id=client_id)
        context['order_list'] = Orders.objects.filter(member_id=member_id, client_id=client_id)
        context['client_notes'] = Notes.objects.filter(member_id=member_id, client_id=client_id)

        # dashboard lists and titles
        context['printproject_list'] = printprojects.order_by('-rfq_date')[:10][::-1]
        context['order_list'] = orders.order_by('-orderdate')[:10][::-1]
        context['printproject_table_title'] = 'Laatste 10 printprojecten'
        context['order_table_title'] = 'Laatste 10 orders'

        context['printproject_table_title'] = 'Laatste 10 aanvragen van ' + str(client.client)
        context['order_table_title'] = 'Laatste 10 orders voor ' + str(client.client)
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
        note.client_id = self.kwargs['pk']
        note.user_id = user.id
        note.save()
        return super(ClientDetails, self).form_valid(form)



class CreateNewClient(CreateView, LoginRequiredMixin):
    model = Clients
    profile = Clients
    form_class = NewClientForm
    template_name = 'clients/new_client.html'
    success_url = '/client_dashboard/'

    def get_success_url(self):
        client_id = self.object.client_id
        member_id = self.request.user.member_id

        new_client = Clients.objects.get(client_id=client_id)
        manager_first_name = new_client.manager_first_name
        manager_last_name = new_client.manager_last_name
        manager_jobtitle = new_client.manager_jobtitle
        manager_mobile_number = new_client.manager_mobile_number
        manager_e_mail = new_client.manager_e_mail

        ClientContacts.objects.create(
            member_id=member_id,
            client_id=client_id,
            clientcontact=manager_first_name + " " + manager_last_name,
            first_name=manager_first_name,
            last_name=manager_last_name,
            jobtitle=manager_jobtitle,
            e_mail_personal=manager_e_mail,
            mobile_number=manager_mobile_number,
            manager=True
        )
        return '/client_dashboard/'

    def form_valid(self, form):
        form.instance.member_id = self.request.user.member_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateNewClient, self).get_context_data(**kwargs)
        context['title'] = "Nieuwe klant aanmaken"
        context['button_text'] = "Klant toevoegen"
        return context


class UpdateClient(UpdateView, LoginRequiredMixin):
    model = Clients
    profile = Clients
    form_class = NewClientForm
    template_name = 'clients/new_client.html'
    success_url = '/client_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.member_id = self.request.user.member_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateClient, self).get_context_data(**kwargs)
        client_id = self.kwargs['pk']
        client = Clients.objects.get(client_id=client_id)
        context['client'] = client
        context['title'] = "Update " + str(client.client)
        context['button_text'] = "Klant update"
        return context


class DeleteClient(DeleteView, LoginRequiredMixin):
    model = Clients
    success_url = "/"


class DeleteClientContact(DeleteView, LoginRequiredMixin):
    model = ClientContacts
    success_url = "/"


class CreateNewClientContact(CreateView, LoginRequiredMixin):
    model = ClientContacts
    profile = ClientContacts
    form_class = NewClientContactForm
    template_name = 'clients/new_update_clientcontact.html'
    success_url = '/client_dashboard/'

    def dispatch(self, request, *args, **kwargs):
        self.client_id = get_object_or_404(Clients, pk=kwargs['client_id']).client_id
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        form.instance.member_id = user.member_id
        form.instance.client_id = self.client_id
        form.instance.created = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateNewClientContact, self).get_context_data(**kwargs)
        context['title'] = "Nieuw contactpersoon toevoegen"
        context['button_text'] = "Contactpersoon toevoegen"
        return context


class UpdateClientContact(UpdateView, LoginRequiredMixin):
    model = ClientContacts
    profile = ClientContacts
    form_class = NewClientContactForm
    template_name = 'clients/new_update_clientcontact.html'
    success_url = '/client_details/'

    def get_success_url(self):
        client_id = ClientContacts.objects.get(clientcontact_id=self.object.clientcontact_id).client_id
        return reverse('client_details', kwargs={'pk': self.object.client_id})

    def form_valid(self, form):
        user = self.request.user
        form.instance.modified = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateClientContact, self).get_context_data(**kwargs)
        context['title'] = "Contactpersoon bijwerken"
        context['button_text'] = "Bijwerken"
        return context
