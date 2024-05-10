from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from assets.models import *
from producers.models import EnhancementTariffs


class PrinterDelete(LoginRequiredMixin, DeleteView):
    model = Printers
    success_url = '/asset_dashboard/'

    def get(self, request, *args, **kwargs):
        producer_id_user = self.request.user.producer_id
        pk = self.kwargs['pk']
        producer_id = Printers.objects.get(printer_id=pk).producer_id
        if producer_id_user == producer_id:
            return self.post(request, *args, **kwargs)
        else:
            return redirect('/home/')


class CuttingmachineDelete(LoginRequiredMixin, DeleteView):
    model = Cuttingmachines
    success_url = '/asset_dashboard/'


    def get(self, request, *args, **kwargs):
        producer_id_user = self.request.user.producer_id
        pk = self.kwargs['pk']
        producer_id = Cuttingmachines.objects.get(cuttingmachine_id=pk).producer_id
        if producer_id_user == producer_id:
            return self.post(request, *args, **kwargs)
        else:
            return redirect('/home/')


class FoldingmachineDelete(LoginRequiredMixin, DeleteView):
    model = Foldingmachines
    success_url = '/asset_dashboard/'

    def get(self, request, *args, **kwargs):
        producer_id_user = self.request.user.producer_id
        pk = self.kwargs['pk']
        producer_id = Foldingmachines.objects.get(foldingachine_id=pk).producer_id
        if producer_id_user == producer_id:
            return self.post(request, *args, **kwargs)
        else:
            return redirect('/home/')


class BindingmachineDelete(LoginRequiredMixin, DeleteView):
    model = Bindingmachines
    success_url = '/asset_dashboard/'

    def get(self, request, *args, **kwargs):
        producer_id_user = self.request.user.producer_id
        pk = self.kwargs['pk']
        producer_id = Bindingmachines.objects.get(bindingid=pk).producer_id
        if producer_id_user == producer_id:
            return self.post(request, *args, **kwargs)
        else:
            return redirect('/home/')


class ProducerEnhancementDelete(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        enhancementtariff_id = kwargs.get('enhancementtariff_id')
        producer_id = request.user.producer_id
        enhancementoffering = EnhancementTariffs.objects.get(enhancementtariff_id=enhancementtariff_id,
                                                             producer_id=producer_id)
        enhancementoffering.delete()
        return redirect('/producer_tariffs/')
