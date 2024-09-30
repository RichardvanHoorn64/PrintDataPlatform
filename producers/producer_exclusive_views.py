from allauth.account.views import RedirectAuthenticatedUserMixin, CloseableSignupMixin, AjaxCapableProcessFormViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Max
from django.urls import reverse
from django.views.generic import View, CreateView, TemplateView
from django.shortcuts import render, redirect

from index.categories_groups import exclusive_memberplans
from index.create_context import creatememberplan_context
from index.exclusive_functions import define_site_name, update_exclusive_members
from index.models import *
from members.crm_functions import update_producersmatch
from members.forms.accountforms import CreateNewExclusiveMemberForm
from printprojects.models import MemberProducerMatch
from profileuseraccount.form_invalids import form_invalid_message
from profileuseraccount.forms.registration_userprofile import UserProfileCreationForm
from profileuseraccount.models import UserProfile, Members
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.utils import get_request_param
from allauth.account.utils import (
    complete_signup,
    passthrough_next_redirect_url,
)

class ProducerExclusiveMembers(LoginRequiredMixin, TemplateView):
    template_name = "producers/tables/producer_members.html"

    def dispatch(self, request, *args, **kwargs):
        update_producersmatch(self.request)
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        elif not user.member.member_plan_id == 4:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProducerExclusiveMembers, self).get_context_data(**kwargs)
        user = self.request.user
        producer_id = user.producer_id
        update_exclusive_members(user)
        producer = Producers.objects.get(producer_id=user.producer_id)
        context = creatememberplan_context(context, user)
        context['user'] = user
        members = MemberProducerMatch.objects.filter(producer_id=producer_id, member_accept=True,
                                                     member__member_plan__id__in=exclusive_memberplans).order_by(
            'member__company')
        context['members'] = members
        context['title'] = str(user.producer.company) + ' exclusieve klanten'
        context['exclusive_module'] = producer.exclusive_module
        context['calculation_module'] = producer.calculation_module
        context['add_members'] = True

        return context


class CreateProducerExclusiveMember(LoginRequiredMixin, CreateView):
    template_name = "producers/create_exclusive_userprofile.html"
    form_class = CreateNewExclusiveMemberForm
    redirect_field_name = "next"

    def get_success_url(self):
        user_id = self.object.id
        new_user = UserProfile.objects.get(pk=user_id)
        new_member_id = Members.objects.aggregate(Max('member_id')).get('member_id__max') + 1

        new_member = Members(
            member_id=new_member_id,
            active=True,
            user_admin=user_id,
            company=new_user.company,
            manager=new_user.first_name + " " + new_user.last_name,
            tel_general=new_user.tel_general,
            e_mail_general=new_user.e_mail_general,
            street_number=new_user.street_number,
            postal_code=new_user.postal_code,
            city=new_user.city,
            member_plan_id=3,
            language_id=new_user.language_id,
            exclusive_producer_id=new_user.producer_id
        )

        try:
            new_member.save()
            my_profile = UserProfile.objects.get(id=new_user.id)
            my_profile.member_id = new_member.member_id
            my_profile.member_plan_id = 3
            my_profile.language_id = 1
            my_profile.save()
        except Exception as e:
            print('ExclusiveLandingView error: ', e)
            pass

        return '/producer_exlusive_members/'

    def form_valid(self, form):
        userprofile = form.save(commit=False)
        password = form.cleaned_data['password1']
        repeat_password = form.cleaned_data['password2']
        new_id = UserProfile.objects.aggregate(Max('id')).get('id__max') + 1

        if password != repeat_password:
            messages.error(self.request, "De ingevoerde wachtwoorden zijn niet hetzelfde",
                           extra_tags='alert alert-danger')
            return render(self.request, self.template_name, form)
        userprofile.id = new_id
        userprofile.username = form.cleaned_data['username']
        userprofile.email = form.cleaned_data['email']
        userprofile.first_name = form.cleaned_data['first_name']
        userprofile.last_name = form.cleaned_data['last_name']
        userprofile.jobtitle = form.cleaned_data['jobtitle']
        userprofile.company = form.cleaned_data['company']
        userprofile.mobile_number = form.cleaned_data['mobile_number']
        userprofile.tel_general = form.cleaned_data['tel_general']
        userprofile.e_mail_general = form.cleaned_data['e_mail_general']
        userprofile.street_number = form.cleaned_data['street_number']
        userprofile.postal_code = form.cleaned_data['postal_code']
        userprofile.city = form.cleaned_data['city']
        userprofile.member_plan_id = 3
        userprofile.language_id = 1
        userprofile.is_active = True
        userprofile.active = True
        userprofile.set_password(password)

        # new_id = UserProfile.objects.aggregate(Max('id')).get('id__max') + 1
        # form.instance.id = new_id
        form.instance.member_plan_id = 3
        form.instance.producer_id = self.request.user.producer_id
        userprofile.save()

        # self.user = form.save(self.request)
        # try:
        #     return complete_signup(
        #         self.request, self.user,
        #         ACCOUNT_EMAIL_VERIFICATION,
        #         self.get_success_url())
        # except ImmediateHttpResponse as e:
        #     return e.response
        return super(CreateProducerExclusiveMember, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ret = super(CreateProducerExclusiveMember, self).get_context_data(**kwargs)
        site_name = define_site_name(self.request.user)

        form = ret['form']
        email = self.request.session.get('account_verified_email')
        if email:
            email_keys = ['email', 'email2']
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)

        countries = DropdownCountries.objects.filter(language_id=1).order_by('country_id')
        ret.update({"login_url": login_url,
                    "site_name": site_name,
                    "countries": countries,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


# signup = CreateProducerExclusiveMember.as_view()


# class UMemberUpdateForm:
#     pass


# class CreateNewExclusiveMemberLanding(View):
#
#     def dispatch(self, request, *args, **kwargs):
#         user = self.request.user
#
#         if not user.is_authenticated:
#             return redirect('/welcome/')
#
#         if not user.member_id:
#             new_member = Members(
#                 active=True,
#                 user_admin=user.id,
#                 company=user.company,
#                 manager=user.first_name + " " + user.last_name,
#                 tel_general=user.tel_general,
#                 e_mail_general=user.e_mail_general,
#                 street_number=user.street_number,
#                 postal_code=user.postal_code,
#                 city=user.city,
#                 member_plan_id=3,
#                 language_id=user.language_id,
#                 exclusive_producer_id=user.producer_id
#             )
#
#             try:
#                 new_member.save()
#                 my_profile = UserProfile.objects.get(id=user.id)
#                 my_profile.member_id = new_member.member_id
#                 my_profile.member_plan_id = 3
#                 my_profile.language_id = 1
#                 my_profile.save()
#             except Exception as e:
#                 print('SignupLandingView error: ', e)
#                 pass
#         else:
#             pass
#
#         return redirect('/printproject_dashboard/1')