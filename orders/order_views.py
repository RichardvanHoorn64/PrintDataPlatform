from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from index.categories_groups import *
from index.display_functions import printproject_description, order_delivery_contact, order_delivery_adress
from orders.forms.forms import OrdersForm
from orders.models import Orders
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from index.forms.form_invalids import form_invalid_message_quotes
from offers.models import *
from index.create_context import createprintproject_context, creatememberplan_context
from orders.ordermail_functions import send_ordermail_producer
from profileuseraccount.form_invalids import error_mail_admin


class OrderDashboard(LoginRequiredMixin, TemplateView):
    template_name = "orders/order_dashboard.html"
    pk_url_kwarg = 'order_status_id'
    context_object_name = 'order_status_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        order_status_id = kwargs['order_status_id']
        user = self.request.user
        context = super(OrderDashboard, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        member_id = user.member_id
        orders = Orders.objects.filter(member_id=member_id, active=True)

        if order_status_id == 0:
            empty_table_text = "Plaats je eerste order"
        elif order_status_id == 0:
            empty_table_text = "Geen open orders"
        elif order_status_id == 1:
            empty_table_text = "Geen orders in aanvraag"
        elif order_status_id == 2:
            empty_table_text = "Geen orders in productie"
        elif order_status_id == 3:
            empty_table_text = "Geen geweigerde orders"
        elif order_status_id == 4:
            empty_table_text = "Geen gefactureerde orders"
        elif order_status_id == 5:
            empty_table_text = "Geen gesloten orders"
        else:
            empty_table_text = "Geen orders"

        context['empty_table_text_orders'] = empty_table_text

        # dashboard lists
        if order_status_id == 0:  # All orders
            context['order_list'] = orders.order_by('-orderdate')

        else:  # Filter orders by status
            context['order_list'] = orders.filter(order_status_id=order_status_id).order_by('-created')

        context['order_table_title'] = 'Orders'

        # counts
        context['all_orders'] = orders.count()
        context['requested_orders'] = orders.filter(order_status=1).count()
        context['production_orders'] = orders.filter(order_status=2).count()
        context['deliverd_orders'] = orders.filter(order_status=3).count()
        context['invoiced_orders'] = orders.filter(order_status=4).count()
        context['closed_orders'] = orders.filter(order_status=5).count()
        return context


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Orders
    form_class = OrdersForm
    template_name = 'orders/new_order.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        order_id = self.object.order_id

        # mail orderdata to producer
        try:
            send_ordermail_producer(order_id)
        except Exception as e:
            error_mail_admin('order id: ' + str(self.object.id) + 'doorverwijzing naar orderbevestiging: ,', e)
        return '/order_details/' + str(order_id)

    def form_valid(self, form):
        user = self.request.user
        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)

        order_volume = form.cleaned_data['order_volume']

        if order_volume == printproject.volume:
            order_value = offer.offer
        else:
            volume_difference = float((order_volume - printproject.volume) * 0.001)
            order_value = float(offer.offer) + float(volume_difference * offer.offer1000extra)

        # fill general data
        form.instance.order_value = order_value
        form.instance.order_status_id = 1
        form.instance.orderdate = datetime.now()
        form.instance.orderer_id = user.id
        form.instance.offer_id = offer.offer_id
        form.instance.producer_id = offer.producer_id
        form.instance.printproject_id = offer.printproject_id
        form.instance.client_id = printproject.client_id
        form.instance.member_id = user.member_id
        form.instance.productcategory_id = offer.productcategory_id
        form.instance.client_id = printproject.client_id

        # general updates
        if not form.instance.order_volume:
            form.instance.order_description = printproject.project_title
        if not form.instance.order_volume:
            form.instance.order_volume = printproject.volume
        if not form.instance.ordernumber:
            form.instance.ordernumber = printproject.own_quotenumber

        # planning updates
        if not form.instance.printfiles_available:
            form.instance.printfiles_available = printproject.supply_date
        if not form.instance.delivery_date_request:
            form.instance.delivery_date_request = printproject.delivery_date

        # fill delivery data
        if printproject.client_id:
            delivery_data = Clients.objects.get(client_id=printproject.client_id)
            deliver_company = delivery_data.client
            deliver_street_number = delivery_data.street_number
            deliver_postcode = delivery_data.postal_code
            deliver_city = delivery_data.city
            deliver_contactperson = delivery_data.manager_first_name + "" + delivery_data.manager_last_name
            deliver_tel = delivery_data.tel_general

        else:
            delivery_data = Members.objects.get(member_id=user.member_id)
            deliver_company = delivery_data.company
            deliver_street_number = delivery_data.street_number
            deliver_postcode = delivery_data.postal_code
            deliver_city = delivery_data.city
            deliver_contactperson = user.first_name + "" + user.last_name
            deliver_tel = delivery_data.tel_general

        if not form.instance.deliver_company:
            form.instance.deliver_company = deliver_company
        if not form.instance.deliver_street_number:
            form.instance.deliver_street_number = deliver_street_number
        if not form.instance.deliver_postcode:
            form.instance.deliver_postcode = deliver_postcode
        if not form.instance.deliver_city:
            form.instance.deliver_city = deliver_city
        if not form.instance.deliver_contactperson:
            form.instance.deliver_contactperson = deliver_contactperson
        if not form.instance.deliver_tel:
            form.instance.deliver_tel = deliver_tel

        # update offer
        offer.offerstatus_id = 3
        offer.save()

        # update printproject
        printproject.printprojectstatus_id = 3
        printproject.volume = form.instance.order_volume
        printproject.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        printproject = PrintProjects.objects.get(printproject_id=offer.printproject_id)

        if printproject.client_id:
            delivery_data = Clients.objects.get(client_id=printproject.client_id)
            context['deliver_company'] = delivery_data.client
            context['deliver_street_number'] = delivery_data.street_number
            context['deliver_postcode'] = delivery_data.postal_code
            context['deliver_city'] = delivery_data.city
            context['deliver_contactperson'] = delivery_data.manager_first_name + "" + delivery_data.manager_last_name
            context['deliver_tel'] = delivery_data.tel_general

        else:
            delivery_data = Members.objects.get(member_id=user.member_id)
            context['deliver_company'] = delivery_data.company
            context['deliver_street_number'] = delivery_data.street_number
            context['deliver_postcode'] = delivery_data.postal_code
            context['deliver_city'] = delivery_data.city
            context['deliver_contactperson'] = user.first_name + "" + user.last_name
            context['deliver_tel'] = delivery_data.tel_general

        context['offer'] = offer
        context = createprintproject_context(context, user, printproject)
        return context


class OrderDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_details.html'
    pk_url_kwarg = 'order_id'
    context_object_name = 'order_id'

    def retrieve_order(self):
        order_id = self.kwargs['order_id']
        order = Orders.objects.get(order_id=order_id)
        return order

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        order = self.retrieve_order()

        if not user.is_authenticated:
            return redirect('/home/')
        if not user.member.active:
            return redirect('/wait_for_approval/')
        if user.member.member_plan_id in producer_memberplans:
            if not user.producer_id == order.producer_id:
                return redirect('/no_access/')
        else:
            if not user.member_id == order.member_id:
                return redirect('/no_access/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context = creatememberplan_context(context, user)
        order_id = kwargs['order_id']
        order = Orders.objects.get(order_id=order_id)
        offer = Offers.objects.get(offer_id=order.offer_id)
        printproject_id = order.printproject_id
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)
        context = createprintproject_context(context, user, printproject)
        productcategory = ProductCategory.objects.get(
            productcategory_id=printproject.productcategory_id).productcategory
        delivery_adress = order_delivery_adress(order)
        delivery_contact = order_delivery_contact(order)

        context['order'] = order
        context['offer'] = offer
        context['delivery_adress'] = delivery_adress
        context['delivery_contact'] = delivery_contact
        context['description'] = printproject_description(printproject, productcategory)
        return context


class OrderDeleteView(LoginRequiredMixin, View):
    pk_url_kwarg = 'order_id'
    context_object_name = 'order_id'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            order_id = kwargs['order_id']
            try:
                order_to_delete = Orders.objects.get(order_id=order_id)
                order_to_delete.delete()
            except ValueError:
                pass
        return super().dispatch(request, *args, **kwargs)


class ChangeOrderStatus(View, LoginRequiredMixin):
    pk_url_kwarg = 'order_id'
    context_object_name = 'orderstatus_id'

    def dispatch(self, request, *args, **kwargs):
        referer = request.META.get("HTTP_REFERER")
        order_id = kwargs.get('order_id')
        order_status_id = kwargs.get('order_status_id')
        update_record = Orders.objects.get(order_id=order_id)
        update_record.order_status_id = order_status_id
        update_record.save()
        return HttpResponseRedirect(referer)
