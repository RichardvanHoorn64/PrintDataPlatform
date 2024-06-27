from django.shortcuts import redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from index.categories_groups import *
from index.forms.form_invalids import form_invalid_message_quotes
from index.models import DropdownChoices
from offers.models import *
from methods.models import *
from printprojects.forms.NewPrintProject import PrintProjectsForm
from printprojects.forms.PrintprojectSalesPice import PrintProjectPriceUpdateForm
from index.create_context import createprintproject_context


# Princing update included
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

        printproject_subtitle = []
        if printproject.printprojectstatus_id == 1:
            printproject_subtitle = '  Kies leveranciers en verstuur offerteaanvragen'

        if printproject.printprojectstatus_id == 2:
            printproject_subtitle = 'Beoordeel aanbiedingen, plaats opdracht'

        if member_plan_id in exclusive_memberplans:
            exclusive_producer = Producers.objects.get(producer_id=user.member.exclusive_producer_id)
            context['exclusive_producer'] = exclusive_producer.company
            printproject_subtitle = 'Aanbieding van: ' + str(exclusive_producer.company)
            context['offer'] = Offers.objects.get(printproject_id=printproject_id)

        context['printproject_subtitle'] = printproject_subtitle
        context['member_plan_id'] = member_plan_id

        # for select suppliers
        context['match_suppliers'] = (PrintProjectMatch.objects.filter(printproject_id=printproject_id,
                                                                       member_id=self.request.user.member_id).exclude(
            memberproducermatch_id__memberproducerstatus_id=3).order_by(
            'memberproducermatch_id__memberproducerstatus_id__memberproducerstatus', '-matchprintproject'))
        context['offers_list'] = Offers.objects.filter(printproject_id=printproject_id,
                                                       member_id=self.request.user.member_id)

        return context


# Creating a clone of a printproject
class PrintProjectCloneView(LoginRequiredMixin, RedirectView):
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')

        clone_printproject = PrintProjects.objects.get(printproject_id=self.kwargs['printproject_id'])
        clone_printproject.printproject_id = None
        clone_printproject.printprojectstatus_id = 1
        clone_printproject.project_title = "Kopie: " + clone_printproject.project_title
        clone_printproject.save()
        new_printproject_id = clone_printproject.printproject_id
        return '/printproject_update/' + str(new_printproject_id)


# Updating a (clone) printproject
class PrintProjectCloneUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'printprojects/new_project.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectsForm

    def get_success_url(self):
        printproject_id = self.object.printproject_id
        return '/printproject_details/' + str(printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = PrintProjects.objects.get(printproject_id=self.kwargs['printproject_id'])
        if not form.cleaned_data['salesprice']:
            form.instance.salesprice = item.salesprice
        if not form.cleaned_data['salesprice_1000extra']:
            form.instance.salesprice_1000extra = item.salesprice_1000extra
        if not form.cleaned_data['invoiceturnover']:
            form.instance.invoiceturnover = item.invoiceturnover

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        printproject_id = self.kwargs['printproject_id']
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)
        user = self.request.user
        language_id = user.language_id
        dropdowns = DropdownChoices.objects.filter(language_id=language_id)
        context = createprintproject_context(context, user, printproject)
        context['update'] = True
        context['button_text'] = "Update Project"
        context['form_title'] = "Printproject aanpassen"
        context['productcategories'] = ProductCategory.objects.all()
        context['member_id'] = user.member_id
        context['clients'] = Clients.objects.filter(member_id=user.member_id).order_by('client')
        context['standardsizes'] = StandardSize.objects.filter(productcategory_id=1)
        context['printsided_choices'] = dropdowns.filter(dropdown="printsided_choices")
        # context['print_choices'] = print_choices
        # context['portrait_landscape_choices'] = portrait_landscape_choices
        # context['pressvarnish_choices'] = pressvarnish_choices
        # context['enhance_sided_choices'] = enhance_sided_choices
        # context['enhance_choices'] = enhance_choices
        # context['packaging_choices'] = packaging_choices
        # context['foldingmethods'] = FoldingMethods.objects.all().order_by('foldingmethod_id')
        #
        # context['papercategories_general'] = PaperCategory.objects.all()
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
                return redirect('/printproject_dashboard/' + str(1))
