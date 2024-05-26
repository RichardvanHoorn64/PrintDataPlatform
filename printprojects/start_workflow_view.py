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
from django.utils import timezone


# Printproject workflow switch
class PrintProjectStartWorkflowView(LoginRequiredMixin, View):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectPriceUpdateForm

    def exclusive_producer(self):
        exclusive_producer_id = define_exclusive_producer_id(self.request.user)
        return exclusive_producer_id



    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        member_plan_id = user.member_plan_id
        printproject_id = self.kwargs['printproject_id']

        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')

        producer_id_list = [1,2]
        if member_plan_id in exclusive_memberplans:
            exclusive_producer_id = define_exclusive_producer_id(user)
            producer_id_list = [exclusive_producer_id]

        for producer_id in producer_id_list:
            calculations = Calculations.objects.filter(printproject_id=printproject_id,producer_id=producer_id)
            offers = Offers.objects.filter(printproject_id=printproject_id)
            calculations.delete()
            offers.delete()

            rfq = PrintProjects.objects.get(printproject_id=printproject_id)
            open_calculation = Calculations(
                printproject_id=rfq.printproject_id,
                producer_id=producer_id,
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
                )
            open_calculation.save()

            # make calculations
            if rfq.productcategory_id in categories_plano:
                plano_folder_calculation(producer_id, rfq)
            if rfq.productcategory_id in categories_brochures_all:
                brochure_calculation(producer_id, rfq)

            new_calculation = Calculations.objects.get(printproject_id=printproject_id, producer_id=producer_id)
            new_offer = Offers(
                    printproject_id=printproject_id,
                    offer_date=timezone.now().today().date(),
                    producer_id=producer_id,
                    member_id=user.member_id,
                    productcategory_id=rfq.productcategory_id,
                    offerstatus_id=1,
                    description=rfq.description,
                    offer_key=0,
                    requester= str(user.first_name) + " " + str(user.last_name),
                    offer=new_calculation.offer_value,
                    offer1000extra=new_calculation.offer_value1000extra,
                )
            new_offer.save()

        if user.member_plan_id not in exclusive_memberplans:
            update_producersmatch(self.request)
            update_printprojectsmatch(self.request, printproject_id)
            return redirect('home')

        # return detail page
        if user.member_plan_id in exclusive_memberplans:
            offer_id = Offers.objects.get(printproject_id=printproject_id,
                                                  producer_id=self.exclusive_producer()).offer_id
            return redirect('/offer_details/' + str(offer_id))
        else:
            return redirect('/printproject_details/' + str(printproject_id))


