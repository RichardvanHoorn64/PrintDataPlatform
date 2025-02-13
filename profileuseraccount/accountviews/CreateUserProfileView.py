from allauth.account.views import RedirectAuthenticatedUserMixin, CloseableSignupMixin, AjaxCapableProcessFormViewMixin
from django.db.models import Max
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from index.site_startfunctions import define_site_name
from index.models import *
from index.translate_functions import find_gendercode
from profileuseraccount.form_invalids import form_invalid_message
from profileuseraccount.forms.registration_userprofile import UserProfileCreationForm
from profileuseraccount.models import UserProfile
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.utils import get_request_param
from allauth.account.utils import (
    complete_signup,
    passthrough_next_redirect_url,
)
from printdataplatform.settings import ACCOUNT_EMAIL_VERIFICATION

INTERNAL_RESET_URL_KEY = "set-password"
INTERNAL_RESET_SESSION_KEY = "_password_reset_key"

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'password1', 'password2'))


class UserProfileCreateView(RedirectAuthenticatedUserMixin, CloseableSignupMixin,
                            AjaxCapableProcessFormViewMixin, FormView):
    template_name = "account/signup.html"
    form_class = UserProfileCreationForm
    redirect_field_name = "next"
    success_url = '/signup_landing/'

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        email = form.cleaned_data['email']

        email_blacklist = BlacklistEmail.objects.filter(excluded=True).values_list('email', flat=True)
        if email in email_blacklist:
            return redirect('/no_access/')

        domain_blacklist = BlacklistDomains.objects.filter(excluded=True).values_list('domain', flat=True)
        domain = email.split(sep="@")[1]
        if domain in domain_blacklist:
            return redirect('/no_access/')

        # of SignupView to access the newly created User instance
        new_id = UserProfile.objects.aggregate(Max('id')).get('id__max') + 1
        gender = form.cleaned_data['gender']
        form.instance.id = new_id
        form.instance.member_plan_id = 1
        form.instance.producer_id = 1
        form.instance.active = False
        form.instance.gender = find_gendercode(gender)

        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request, self.user,
                ACCOUNT_EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ret = super(UserProfileCreateView, self).get_context_data(**kwargs)
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
        genders = DropdownChoices.objects.filter(dropdown='gender', language_id=1).order_by('dropdown_id')

        ret.update({"login_url": login_url,
                    "site_name": site_name,
                    'genders': genders,
                    "countries": countries,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


signup = UserProfileCreateView.as_view()


class UMemberUpdateForm:
    pass
