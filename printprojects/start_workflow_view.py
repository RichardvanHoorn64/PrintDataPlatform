from django.shortcuts import redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from members.crm_functions import update_producersmatch, update_printprojectsmatch
from methods.models import *
from printprojects.forms.ProducerMemberSalesPrice import PrintProjectPriceUpdateForm
from printprojects.models import MemberProducerMatch

from printprojects.workflow_functions import *


# Printproject workflow switch
class PrintProjectStartWorkflowView(LoginRequiredMixin, View):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectPriceUpdateForm

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        printproject_id = self.kwargs['printproject_id']

        if not user.is_authenticated:
            return redirect('/home/')

        if not user.member.active:
            return redirect('/wait_for_approval/')

        # retrieve printproject plus check ownership
        try:
            rfq_name = str(user.first_name) + " " + str(user.last_name)
            member_plan_id = user.member_plan_id
            rfq = PrintProjects.objects.get(printproject_id=printproject_id, member_id=user.member_id)
        except PrintProjects.DoesNotExist:
            return redirect('home')

        # start exclusive member workflow
        if member_plan_id in exclusive_memberplans:
            producer_id = user.member.exclusive_producer_id
            calculation_module = Producers.objects.get(producer_id=producer_id).calculation_module
            create_open_calculation_offer(rfq_name, rfq, producer_id, calculation_module)

            # make calculations
            if calculation_module:
                try:
                    auto_calculate_offer(rfq, producer_id)
                except Exception as e:
                    print('auto_calculate_offer failed: (rfq, producer_id)', e)

            offer_id = Offers.objects.get(printproject_id=printproject_id,
                                          producer_id=producer_id).offer_id
            return redirect('/offer_details/' + str(offer_id))

        # start open member workflow
        if member_plan_id in open_memberplans:
            update_producersmatch(self.request)
            update_printprojectsmatch(self.request, printproject_id)
            producer_id_list = MemberProducerMatch.objects.filter(member_id=user.member_id).values_list('producer_id',
                                                                                                        flat=True)

            for producer_id in producer_id_list:
                calculation_module = Producers.objects.get(producer_id=producer_id).calculation_module
                create_open_calculation_offer(rfq_name, rfq, producer_id, calculation_module)

        return redirect('/printproject_details/' + str(printproject_id))
