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
            member_plan_id = user.member_plan_id
            rfq = PrintProjects.objects.get(printproject_id=printproject_id, member_id=user.member_id)
        except PrintProjects.DoesNotExist:
            return redirect('home')

        # start exclusive member workflow
        if member_plan_id in exclusive_memberplans:
            producer_id = user.member.exclusive_producer_id
            calculation_module = Producers.objects.get(producer_id=producer_id).calculation_module
            # create open calculations
            create_open_calculation_offer(rfq, producer_id, True)

            # make calculations
            if calculation_module:
                try:
                    auto_calculate_offer(rfq, producer_id)
                except Exception as e:
                    print('auto_calculate_offer failed: (rfq, producer_id)', e)

            offer_id = Offers.objects.get(printproject_id=printproject_id,
                                          producer_id=producer_id).offer_id
            return redirect('/offer_details/' + str(offer_id))

        # start open workflow: step 1. workflow select suppliers
        if member_plan_id in open_memberplans:
            update_producersmatch(self.request)
            update_printprojectsmatch(self.request, printproject_id)

        return redirect('/printproject_details/' + str(printproject_id))


# Open workflow step 2: send rfq after select suppliers for open calculations
class SendRFQView(LoginRequiredMixin, View):
    pk_url_kwarg = 'printproject_id'

    def dispatch(self, request, *args, **kwargs):
        printproject_id = self.kwargs['printproject_id']
        user = self.request.user
        member_id = user.member_id
        member_company = user.company
        printprojectsmatch = PrintProjectMatch.objects.filter(printproject_id=printproject_id, member_id=member_id)
        selected_producers = printprojectsmatch.filter(matchprintproject=True).values_list('producer_id', flat=True)
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)

        try:
            rfq = PrintProjects.objects.get(printproject_id=printproject_id, member_id=user.member_id)
        except PrintProjects.DoesNotExist:
            return redirect('no_access')

        # create open offers
        for producer_id in selected_producers:
            producer = Producers.objects.get(producer_id=producer_id)
            auto_quote = MemberProducerMatch.objects.get(member_id=member_id, producer_id=producer_id).auto_quote

            try:
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)
            except Offers.DoesNotExist:
                create_new_offer(rfq, producer_id)
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)

            # Try to make automated calculations
            if producer.calculation_module:
                if auto_quote:
                    create_open_calculation_offer(rfq, producer_id, True)
                    try:
                        auto_calculate_offer(rfq, producer_id)
                        # Send calculation update mail
                        calculation = Calculations.objects.get(producer_id, new_offer.printproject_id)
                        send_calculationupdate_mail(producer, member_company, new_offer, calculation)
                    except Exception as e: # Send rfq's
                        print('auto_calculate_offer failed: (rfq, producer_id)', e)
                        send_rfq_mail(producer, member_company, new_offer, printproject)
                else:  # Send rfq's
                    send_rfq_mail(producer, member_company, new_offer, printproject)
                    print('no auto quote printproject producer', rfq.printproject_id, "", producer_id)
            else:  # Send rfq's
                send_rfq_mail(producer, member_company, new_offer, printproject)
                print('no calculation_module printproject producer', rfq.printproject_id, "", producer_id)

        # set printprojectstatus
        printprojects_update = PrintProjects.objects.filter(printproject_id=printproject_id)
        for project_update in printprojects_update:
            project_update.printprojectstatus_id = 2
            project_update.save()

        # delete printprojectmatch records
        completed_rfqs = PrintProjectMatch.objects.filter(printproject_id=printproject_id)
        for completed_rfq in completed_rfqs:
            completed_rfq.delete()

        return redirect('/printproject_details/' + str(printproject_id))
