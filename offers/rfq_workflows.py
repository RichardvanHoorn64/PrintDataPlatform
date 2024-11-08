from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View
from offers.models import *
from offers.rfq_functions import *
from printprojects.models import *
from printprojects.workflow_functions import auto_calculate_offer, create_new_offer, create_open_calculation_offer


# send rfq after select suppliers for open calculations
class SendRFQView(LoginRequiredMixin, View):
    template_name = 'printprojects/printproject_details.html'
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

        # Try to make automated calculations
        for producer_id in selected_producers:
            producer = Producers.objects.get(producer_id=producer_id)
            auto_quote = MemberProducerMatch.objects.get(member_id=member_id, producer_id=producer_id).auto_quote

            try:
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)
            except Offers.DoesNotExist:
                create_new_offer(rfq, producer_id)
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)

            if producer.calculation_module:

                if auto_quote:
                    create_open_calculation_offer(rfq, producer_id, True)
                    try:
                        auto_calculate_offer(rfq, producer_id)
                    except Exception as e:
                            print('auto_calculate_offer failed: (rfq, producer_id)', e)
                            send_rfq_mail(producer, member_company, new_offer, printproject)
                else: # Send rfq's
                    send_rfq_mail(producer, member_company, new_offer, printproject)
                    print('no auto quote printproject producer', rfq.printproject_id, "", producer_id)
            else: # Send rfq's
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
