from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from index.forms.relationforms import NewProducerForm
from profileuseraccount.form_invalids import form_invalid_message
from profileuseraccount.models import Producers


class CreateNewProducer(CreateView, LoginRequiredMixin):
    model = Producers
    profile = Producers
    form_class = NewProducerForm

    def get_success_url(self):
        return self.request.session['previous_page']
    def form_valid(self, form):
        user = self.request.user
        form.instance.language_id = user.language_id
        return super().form_valid(form)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateNewProducer, self).get_context_data(**kwargs)
        context['title'] = "Nieuwe producent aanmaken"
        context['button_text'] = "Producent toevoegen"
        return context


from django.shortcuts import render

# Create your views here.
