from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from profileuseraccount.form_invalids import form_invalid_message
from profileuseraccount.forms.registratie_userprofile import *
from profileuseraccount.models import *
from django.shortcuts import render, redirect
from django.contrib import messages


class CoWorkerUserProfileCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('users:login')
    form_class = CoWorkerUserProfileCreateForm
    success_message = 'Een nieuw collega user profiel is aangemaakt'
    pk_url_kwarg = 'member_id'
    template_name = 'members/create_coworker.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        success_url = '/my_account/' + str(self.request.user.member_id)
        return success_url

    def form_valid(self, form):
        new_user_profile = form.save(commit=False)
        password = form.cleaned_data['password1']
        repeat_password = form.cleaned_data['password2']
        user = self.request.user

        if password != repeat_password:
            messages.error(self.request, "De ingevoerde wachtwoorden zijn niet hetzelfde",
                           extra_tags='alert alert-danger')
            return render(self.request, self.template_name, form)

        member_id = user.member_id
        member = Members.objects.get(member_id=member_id)

        new_user_profile.username = form.cleaned_data['username']
        new_user_profile.e_mail_general = member.e_mail_general
        new_user_profile.first_name = form.cleaned_data['first_name']
        new_user_profile.last_name = form.cleaned_data['first_name']
        new_user_profile.tel_general = member.tel_general
        new_user_profile.mobile_number = form.cleaned_data['mobile_number']
        new_user_profile.jobtitle = form.cleaned_data['jobtitle']
        new_user_profile.member_id = member.member_id
        new_user_profile.producer_id = user.producer_id
        new_user_profile.company = member.company
        new_user_profile.street_number = member.street_number
        new_user_profile.postal_code = member.postal_code
        new_user_profile.city = member.city
        new_user_profile.is_active = True
        new_user_profile.first_user = False
        new_user_profile.set_password(password)
        new_user_profile.save()
        return super(CoWorkerUserProfileCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super(CoWorkerUserProfileCreateView, self).get_context_data(**kwargs)
        return context


class CoWorkerUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = UserProfileUpdateForm
    pk_url_kwarg = 'id'
    template_name = 'members/update_coworker.html'
    model = UserProfile

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        success_url = '/my_account/' + str(self.request.user.member_id)
        return success_url

    def form_valid(self, form):
        return super(CoWorkerUserProfileUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super(CoWorkerUserProfileUpdateView, self).get_context_data(**kwargs)
        return context


class ProducerCollegaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('users:login')
    template_name = 'registration/../../templates/members/create_coworker.html'
    form_class = CoWorkerUserProfileCreateForm
    success_message = 'Een nieuw user profiel is aangemaakt'
    pk_url_kwarg = 'member_id'

    def get_success_url(self):
        return '/mijn_productiebedrijf/' + str(self.request.user.producer_id)

    def form_valid(self, form):
        new_user_profile = form.save(commit=False)
        password = form.cleaned_data['password1']
        repeat_password = form.cleaned_data['password2']
        user = self.request.user

        if password != repeat_password:
            messages.error(self.request, "De ingevoerde wachtwoorden zijn niet hetzelfde",
                           extra_tags='alert alert-danger')
            return render(self.request, self.template_name, form)

        member_id = user.member_id
        member = Members.objects.get(member_id=member_id)
        new_user_profile.username = form.cleaned_data['username']
        new_user_profile.e_mail_algemeen = form.cleaned_data['email']
        new_user_profile.first_name = form.cleaned_data['first_name']
        new_user_profile.last_name = form.cleaned_data['last_name']
        new_user_profile.man_vrouw = form.cleaned_data['man_vrouw']
        new_user_profile.tel_general = form.cleaned_data['tel_general']
        new_user_profile.mobile_number = form.cleaned_data['mobile_number']
        new_user_profile.jobtitle = form.cleaned_data['jobtitle']
        new_user_profile.member_id = member.member_id
        new_user_profile.producer_id = user.producer_id
        new_user_profile.company = member.company
        new_user_profile.street_number = member.street_number
        new_user_profile.postal_code = member.postal_code
        new_user_profile.city = member.city
        new_user_profile.user_type = user.user_type
        new_user_profile.is_active = True
        new_user_profile.is_welkom = True
        new_user_profile.set_password(password)
        new_user_profile.save()
        return super(ProducerCollegaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerCollegaCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        # context['skin_template_name'] = get_skin_template_name(user)
        context['user_type'] = user.user_type
        # context['productaanbod'] = productaanbod_vaststellen(user)
        return context


class MedewerkerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('users:login')
    form_class = CoWorkerUserProfileCreateForm
    template_name = 'registration/medewerker_aanmaken.html'
    success_message = 'Een nieuwe medewerker is aangemaakt'
    pk_url_kwarg = 'member_id'
    success_url = '/mijn_klanten/'

    def form_valid(self, form):
        new_user_profile = form.save(commit=False)
        password = form.cleaned_data['password1']
        repeat_password = form.cleaned_data['password2']

        if password != repeat_password:
            messages.error(self.request, "De ingevoerde wachtwoorden zijn niet hetzelfde",
                           extra_tags='alert alert-danger')
            return render(self.request, self.template_name, form)

        member_id = self.kwargs['member_id']
        member = Members.objects.get(member_id=member_id)
        new_user_profile.username = form.cleaned_data['username']
        new_user_profile.e_mail_algemeen = form.cleaned_data['email']
        new_user_profile.first_name = form.cleaned_data['first_name']
        new_user_profile.last_name = form.cleaned_data['last_name']
        new_user_profile.man_vrouw = form.cleaned_data['man_vrouw']
        new_user_profile.mobile_number = form.cleaned_data['mobile_number']
        new_user_profile.jobtitle = form.cleaned_data['jobtitle']
        new_user_profile.producer_id = member.producer_id
        new_user_profile.member_id = member_id
        new_user_profile.company = member.company
        new_user_profile.street_number = member.street_number
        new_user_profile.postal_code = member.postal_code
        new_user_profile.city = member.city
        new_user_profile.set_password(password)
        new_user_profile.save()
        return super(MedewerkerCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super(MedewerkerCreateView, self).get_context_data(**kwargs)
        context['user_type'] = self.request.user.user_type
        return context


def deactiveer_collega(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/home/')

    collega_id = kwargs['id']
    member_id = request.user.member_id
    collega = UserProfile.objects.get(member_id=member_id, id=collega_id)
    collega.is_active = False
    collega.save(update_fields=['is_active'])
    return redirect('/mijn_bedrijf/' + str(request.user.member_id))


def activeer_collega(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/home/')

    collega_id = kwargs['id']
    member_id = request.user.member_id
    collega = UserProfile.objects.get(member_id=member_id, id=collega_id)
    collega.is_active = True
    collega.save(update_fields=['is_active'])
    return redirect('/mijn_bedrijf/' + str(request.user.member_id))


def deactiveer_medewerker(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/home/')

    medewerker_id = kwargs['id']
    medewerker = UserProfile.objects.get(id=medewerker_id)
    medewerker.is_active = False
    medewerker.save(update_fields=['is_active'])

    return redirect('/mijn_klantdetails/' + str(medewerker.member_id))


def activeer_medewerker(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/home/')

    medewerker_id = kwargs['id']
    medewerker = UserProfile.objects.get(id=medewerker_id)
    medewerker.is_active = True
    medewerker.save(update_fields=['is_active'])

    return redirect('/mijn_klantdetails/' + str(medewerker.member_id))
