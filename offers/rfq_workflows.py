from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View
from offers.models import *
from offers.rfq_functions import *
from printprojects.models import *
from printprojects.workflow_functions import auto_calculate_offer, create_new_offer


# send rfq to selected suppliers
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

            try:
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)
            except Offers.DoesNotExist:
                create_new_offer(rfq, producer_id)
                new_offer = Offers.objects.get(printproject_id=printproject_id, producer_id=producer_id)

            if producer.calculation_module:
                try:
                    auto_calculate_offer(rfq, producer_id)
                except Exception as e:
                    print('auto_calculate_offer failed: (rfq, producer_id)', e)
                    send_rfq_mail(producer, member_company, new_offer, printproject)

            else:  # Send rfq's
                send_rfq_mail(producer, member_company, new_offer, printproject)

        # set printprojectstatus
        printprojects_update = PrintProjects.objects.filter(printproject_id=printproject_id)
        for project_update in printprojects_update:
            project_update.printprojectstatus_id = 2
            project_update.save()

        return redirect('/printproject_details/' + str(printproject_id))
