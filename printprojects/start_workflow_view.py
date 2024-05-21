from django.shortcuts import redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from calculations.item_calculations.brochure_calculation import brochure_calculation
from calculations.item_calculations.plano_folder_calculation import plano_folder_calculation
from calculations.models import Calculations
from index.exclusive_functions import define_exclusive_producer_id
from members.crm_functions import update_producersmatch, update_printprojectsmatch
from methods.models import *
from offers.models import Offers
from printprojects.forms.PrintprojectSalesPice import PrintProjectPriceUpdateForm
from index.categories_groups import *


# Printproject workflow switch
class PrintProjectStartWorkflowView(LoginRequiredMixin, View):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectPriceUpdateForm

    def get_success_url(self):
        printproject_id = self.kwargs['printproject_id']
        return '/printproject_details/' + str(printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        printproject_id = self.kwargs['printproject_id']
        exclusive_producer_id = define_exclusive_producer_id(user)

        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')

        if exclusive_producer_id:
            calculations = Calculations.objects.filter(printproject_id=printproject_id)
            offers = Offers.objects.filter(printproject_id=printproject_id)

            if len(calculations) ==0:
                rfq = PrintProjects.objects.get(printproject_id=printproject_id)
                new_calculation = Calculations(
                    printproject_id=rfq.printproject_id,
                    producer_id=exclusive_producer_id,
                    member_id=rfq.member_id,
                    assortiment_item=True,
                    productcategory_id=rfq.productcategory_id,
                    volume=rfq.volume,
                    catalog_code=rfq.catalog_code,
                    status='To be calculated',
                    error='--',
                    total_cost=0,
                    total_cost1000extra=0,
                    offer_value=0,
                    offer_value1000extra=0,
                    offerstatus_id=2,
                )
                new_calculation.save()

                if rfq.productcategory_id in categories_plano:
                    plano_folder_calculation(user, rfq)
                if rfq.productcategory_id in categories_brochures_all:
                    brochure_calculation(user, rfq)

            if len(offers) == 0 and len(calculations) ==1:
                rfq = PrintProjects.objects.get(printproject_id=printproject_id)
                calculation = Calculations.objects.get(printproject_id=printproject_id)
                new_offer = Offers(
                    printproject_id=printproject_id,
                    producer_id=exclusive_producer_id,
                    member_id=user.member_id,
                    productcategory_id=rfq.productcategory_id,
                    offerstatus_id=1,
                    description=rfq.description,
                    offer_key=0,
                    requester= str(user.first_name) + " " + str(user.last_name),
                    offer=calculation.offer_value,
                    offer1000extra=calculation.offer_value1000extra,
                )
                new_offer.save()

            return redirect('/printproject_details/' + str(printproject_id))

        if not exclusive_producer_id:
            update_producersmatch(self.request)
            update_printprojectsmatch(self.request, printproject_id)
            return redirect('home')
