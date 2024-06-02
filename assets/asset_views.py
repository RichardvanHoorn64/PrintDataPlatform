# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from index.create_context import creatememberplan_context
from profileuseraccount.form_invalids import form_invalid_message
from assets.asset_forms import *


def context_create(self, context):
    user = self.request.user
    context = creatememberplan_context(context, user)
    context['asset_form_title'] = str(self.asset_category) + ' toevoegen'
    context['text'] = "Hier regristreer je een nieuwe " + str(self.asset_category)
    context['button_text'] = str(self.asset_category) + ' toevoegen'
    context['update'] = False
    return context


def context_update(self, context):
    user = self.request.user
    context = creatememberplan_context(context, user)
    context['asset_form_title'] = "Instellingen wijzigen "
    context['text'] = "Hier pas je de instelingen aan van je " + str(self.asset_category)
    context['button_text'] = str(self.asset_category) + ' instellingen wijzigen'
    context['update'] = True
    return context


# Asset dashboard
class AssetDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'assets/asset_dashboard.html'
    asset = 'Printer'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(AssetDashboardView, self).get_context_data(**kwargs)
        context = creatememberplan_context(context, user)

        context['asset_dashboard_title'] = "Productiemiddelen dashboard"
        context['assets_printers'] = Printers.objects.filter(producer_id=self.request.user.producer_id).order_by(
            'printer_id')
        context['assets_foldingmachines'] = Foldingmachines.objects.filter(
            producer_id=self.request.user.producer_id).order_by(
            'foldingmachine_id')
        context['assets_cuttingmachines'] = Cuttingmachines.objects.filter(
            producer_id=self.request.user.producer_id).order_by(
            'cuttingmachine_id')
        context['assets_bindingmachines'] = Bindingmachines.objects.filter(
            producer_id=self.request.user.producer_id).order_by('bindingmachine_id')

        return context


class CreatePrinter(LoginRequiredMixin, CreateView):
    model = Printers
    form_class = CreateUpdatePrinterForm
    profile = Printers
    success_url = '/asset_dashboard/'
    asset_category = "Printer"

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreatePrinter, self).get_context_data(**kwargs)
        context = context_create(self, context)
        return context


class UpdatePrinter(LoginRequiredMixin, UpdateView):
    model = Printers
    form_class = CreateUpdatePrinterForm
    pk_url_kwarg = 'printer_id'
    context_object_name = 'printer_id'
    asset_category = "Printer"

    def get_success_url(self):
        printer_id = self.object.printer_id
        return reverse_lazy('update_printer', kwargs={'printer_id': printer_id})

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        printer_id = self.kwargs['printer_id']
        context = super(UpdatePrinter, self).get_context_data(**kwargs)
        context = context_update(self, context)
        context['asset'] = Printers.objects.get(printer_id=printer_id)
        return context


class CreateFoldingmachine(LoginRequiredMixin, CreateView):
    model = Foldingmachines
    form_class = CreateUpdateFoldingMachinesForm
    success_url = '/asset_dashboard/'
    pk_url_kwarg = 'foldingtype_id'
    asset_category = "foldingmachine"

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id

        if form.cleaned_data['sheet_input'] == 'drukvel_breedte':
            form.instance.sheet_input = 1
        else:
            form.instance.sheet_input = 2

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateFoldingmachine, self).get_context_data(**kwargs)
        context = context_create(self, context)
        context['foldingtype_id'] = self.kwargs['foldingtype_id']
        return context


class UpdateFoldingmachine(LoginRequiredMixin, UpdateView):
    model = Foldingmachines
    form_class = CreateUpdateFoldingMachinesForm
    pk_url_kwarg = 'foldingmachine_id'
    asset_category = "Vouwmachine"

    def get_success_url(self):
        foldingmachine_id = self.object.foldingmachine_id
        return reverse_lazy('update_foldingmachine', kwargs={'foldingmachine_id': foldingmachine_id})

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        foldingmachine_id = self.kwargs['foldingmachine_id']
        asset = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id)
        context = super(UpdateFoldingmachine, self).get_context_data(**kwargs)
        context = context_update(self, context)
        context['asset'] = asset
        context['foldingtype_id'] = asset.foldingtype_id
        return context


class CreateCuttingmachine(LoginRequiredMixin, CreateView):
    model = Cuttingmachines
    form_class = CreateUpdateCuttingmachinesForm
    success_url = '/asset_dashboard/'
    asset_category = 'Snijmachine'

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateCuttingmachine, self).get_context_data(**kwargs)
        context = context_create(self, context)
        return context


class UpdateCuttingmachine(LoginRequiredMixin, UpdateView):
    model = Cuttingmachines
    form_class = CreateUpdateCuttingmachinesForm
    pk_url_kwarg = 'cuttingmachine_id'
    asset_category = 'Snijmachine'

    def get_success_url(self):
        cuttingmachine_id = self.object.cuttingmachine_id
        return reverse_lazy('update_cuttingmachine', kwargs={'cuttingmachine_id': cuttingmachine_id})

    def get_context_data(self, **kwargs):
        cuttingmachine_id = self.kwargs['cuttingmachine_id']
        context = super(UpdateCuttingmachine, self).get_context_data(**kwargs)
        context = context_update(self, context)
        context['asset'] = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id,
                                                       producer_id=self.request.user.producer_id)
        return context

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        return super().form_valid(form)


class CreateBindingmachine(LoginRequiredMixin, CreateView):
    template = 'produceren/Bindingmachines_aanmaken_update.html'
    model = Bindingmachines
    form_class = CreateUpdateBindingMachineForm
    success_url = '/asset_dashboard/'
    context_object_name = 'Bindingmachines'
    asset_category = 'Bindmachine'

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateBindingmachine, self).get_context_data(**kwargs)
        context = context_create(self, context)
        return context


class UpdateBindingmachine(LoginRequiredMixin, UpdateView):
    template = 'produceren/Bindingmachines_aanmaken_update.html'
    model = Bindingmachines
    form_class = CreateUpdateBindingMachineForm
    pk_url_kwarg = 'bindingmachine_id'
    asset_category = 'Brocheermachine'

    def get_success_url(self):
        bindingmachine_id = self.object.bindingmachine_id
        return reverse_lazy('update_bindingmachine', kwargs={'bindingmachine_id': bindingmachine_id})

    def form_valid(self, form):
        form.instance.producer_id = self.request.user.producer_id
        form.instance.finishingmethod_id = form.cleaned_data['finishingmethod_id']
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateBindingmachine, self).get_context_data(**kwargs)
        bindingmachine_id = self.kwargs['bindingmachine_id']
        context = context_update(self, context)
        asset = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id,
                                            producer_id=self.request.user.producer_id)
        context['brochure_finishingmethods'] = BrochureFinishingMethods.objects.filter(
            language_id=self.request.user.language_id).exclude(finishingmethod_id=asset.finishingmethod_id)
        context['asset'] = asset

        return context

# Enhancement


# Update enhancement
