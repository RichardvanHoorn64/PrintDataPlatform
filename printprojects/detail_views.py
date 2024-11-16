from django.shortcuts import redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from index.categories_groups import *
from index.forms.form_invalids import form_invalid_message_quotes
from offers.models import *
from methods.models import *
from printprojects.forms.ProducerMemberSalesPrice import PrintProjectPriceUpdateForm
from index.create_context import createprintproject_context
from django.http import HttpResponseRedirect


# Pricing update included
class PrintProjectDetailsView(LoginRequiredMixin, UpdateView):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectPriceUpdateForm

    def get_success_url(self):
        printproject_id = self.kwargs['printproject_id']
        return '/printproject_details/' + str(printproject_id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        printproject_id = self.kwargs['printproject_id']
        printproject = PrintProjects.objects.get(member_id=user.member_id, printproject_id=printproject_id)
        context = createprintproject_context(context, user, printproject)
        member_plan_id = user.member.member_plan_id

        if member_plan_id in pro_memberplans:
            try:
                client = Clients.objects.get(client_id=printproject.client_id, member_id=user.member_id).client
            except Clients.DoesNotExist:
                client = 'Geen opgave'
        else:
            client = 'Alleen voor pro accounts'

        context['client'] = client

        printproject_subtitle = []
        if printproject.printprojectstatus_id == 1:
            printproject_subtitle = '  Kies leveranciers en verstuur offerteaanvragen'

        if printproject.printprojectstatus_id == 2:
            printproject_subtitle = 'Beoordeel aanbiedingen, plaats opdracht'

        context['printproject_subtitle'] = printproject_subtitle
        context['member_plan_id'] = member_plan_id

        # for select suppliers
        context['match_suppliers'] = (PrintProjectMatch.objects.filter(printproject_id=printproject_id,
                                                                       member_id=user.member_id).order_by(
            'memberproducermatch_id__memberproducerstatus_id__memberproducerstatus', '-matchprintproject'))
        context['offers_list'] = Offers.objects.filter(printproject_id=printproject_id,
                                                       member_id=self.request.user.member_id)

        return context


class PrintProjectDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'printprojects/printproject_details.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            try:
                printproject = PrintProjects.objects.get(printproject_id=self.kwargs['printproject_id'])
                printproject.active = False
                printproject.save()
            finally:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
