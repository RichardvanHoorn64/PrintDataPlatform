from allauth.account.views import RedirectAuthenticatedUserMixin, CloseableSignupMixin, AjaxCapableProcessFormViewMixin
from django.db.models import Max
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from profileuseraccount.form_invalids import form_invalid_message
from profileuseraccount.forms.registratie_userprofile import UserProfileCreationForm
from profileuseraccount.models import UserProfile
from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_request_param
from allauth.account.utils import (
    complete_signup,
    get_next_redirect_url,
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

    # def get_form_class(self):
    #     return get_form_class(app_settings.FORMS, 'signup', self.form_class)

    # def get_success_url(self):
    #     # Explicitly passed ?next= URL takes precedence
    #     ret = (
    #             get_next_redirect_url(
    #                 self.request,
    #                 self.redirect_field_name) or self.success_url)
    #     return ret

    def form_valid(self, form):
        member_plan_id = self.kwargs['plan_id']
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        new_id = UserProfile.objects.aggregate(Max('id')).get('id__max') + 1
        form.instance.id = new_id
        form.instance.member_plan_id = member_plan_id
        form.instance.language_id = 1

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
        form = ret['form']
        email = self.request.session.get('account_verified_email')
        if email:
            email_keys = ['email']
            email_keys.append('email2')
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


signup = UserProfileCreateView.as_view()


