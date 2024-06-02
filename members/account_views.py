import logging
from datetime import timedelta
from index.create_context import *
from members.forms.accountforms import MemberUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signals import got_request_exception
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, DetailView, View
from profileuseraccount.confirmation_mails import new_member_confirmationmail
from producers.models import *
from profileuseraccount.models import Members


def log(*args, **kwargs):
    logging.exception('error', args, kwargs)


class NoAccessView(TemplateView):
    template_name = 'no_access.html'


class ThanksSubmitView(TemplateView):
    template_name = 'thanks_submit_offer.html'


class SignupLandingView(TemplateView):
    got_request_exception.connect(log)

    # template_name = 'account/signup_landing.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        memberplan = MemberPlans.objects.get(member_plan_id=user.member_plan_id)

        if memberplan.producer:
            producerplan = True
        else:
            producerplan = False

        if not user.is_authenticated:
            return redirect('/welcome/')

        if not user.member_id:
            new_member = Members(
                active=False,
                user_admin=user.id,
                company=user.company,
                manager=user.first_name + " " + user.last_name,
                tel_general=user.tel_general,
                e_mail_general=user.e_mail_general,
                street_number=user.street_number,
                postal_code=user.postal_code,
                city=user.city,
                member_plan_id=memberplan.member_plan_id,
                language_id=memberplan.language_id,
                producerplan=producerplan,
            )

            try:
                new_member.save()
                my_profile = UserProfile.objects.get(id=user.id)
                my_profile.member_id = new_member.member_id
                my_profile.member_plan_id = new_member.member_plan_id
                my_profile.language_id = 1
                my_profile.save()
            except Exception as e:
                print('SignupLandingView error: ', e)
                pass

        else:
            pass

        if producerplan and not user.producer_id:
            new_producer = Producers(
                active=False,
                user_admin=user.id,
                company=user.company,
                manager=user.first_name + " " + user.last_name,
                tel_general=user.tel_general,
                e_mail_general=user.e_mail_general,
                street_number=user.street_number,
                postal_code=user.postal_code,
                city=user.city,
                member_plan_id=memberplan.member_plan_id,
                language_id=memberplan.language_id,
            )

            try:
                new_producer.save()
                my_profile = UserProfile.objects.get(id=user.id)
                my_profile.producer_id = new_producer.producer_id
                my_profile.member_plan_id = new_producer.member_plan_id
                my_profile.language_id = memberplan.language_id
                my_profile.save()
            except Exception as e:
                print('SignupLandingView error: ', e)
                pass

        else:
            pass

        try:
            new_member_confirmationmail(user)
        except Exception as e:
            print('SignupLandingView error: ', e)
            pass

        return redirect('/printproject_dashboard/0')


class MyAccountView(DetailView, LoginRequiredMixin):
    template_name = 'members/my_account.html'
    model = Members

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(MyAccountView, self).get_context_data(**kwargs)
        member = Members.objects.get(member_id=user.member_id)
        member_plan_id = member.member_plan_id
        memberplan = MemberPlans.objects.get(member_plan_id=member_plan_id)
        context = creatememberplan_context(context, user)
        context['memberplan'] = memberplan
        context['member'] = member
        context['member_plan_id'] = member_plan_id
        context['upgrade_member_plan'] = MemberPlans.objects.get(member_plan_id=2, language_id=user.language_id)
        context['member_plan_name'] = MemberPlans.objects.get(member_plan_id=member_plan_id,
                                                              language_id=user.language_id).plan_name
        context['plan_name'] = memberplan.plan_name
        context['expire_date'] = member.created + timedelta(days=30)
        context['memberaccount_list'] = UserProfile.objects.filter(member_id=user.member_id, active=True)
        return context


class MyAccountUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'members/my_account_update.html'
    model = Members
    form_class = MemberUpdateForm

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # maken dat user account voor bedrijfsnaam bijgewerkt wordt
        user = self.request.user
        member = Members.objects.get(member_id=user.member_id)
        member_userlist = list(UserProfile.objects.filter(member_id=user.member_id).values_list('id', flat=True))

        for member_user_id in member_userlist:
            user_update = UserProfile.objects.get(id=member_user_id)
            user_update.company = member.company
            user_update.tel_general = member.tel_general
            user_update.e_mail_general = member.e_mail_general
            user_update.street_number = member.street_number
            user_update.postal_code = member.postal_code
            user_update.city = member.city
            user_update.save()

        return reverse('my_account', kwargs={'pk': self.object.member_id})

    def get_context_data(self, *args, **kwargs):
        context = super(MyAccountUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        member = Members.objects.get(member_id=user.member_id)
        context['member'] = member
        return context


class MyAccountDeleteView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            member_id = self.kwargs['member_id']
            deactivated_member = Members.objects.get(member_id=member_id)
            deactivated_member.active = False
            deactivated_member.save()
            return redirect('/welcome/')


class DeactivateUser(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            user = self.request.user
            user_id = self.kwargs['id']
            deactivated_user = UserProfile.objects.get(id=user_id)
            deactivated_user.active = False
            deactivated_user.save()
            return redirect('/my_account/' + str(user.member_id))


class MemberplanUpgradeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            member_id = self.kwargs['member_id']

            if user.member_id == member_id and user.member.member_plan_id in [1, 3]:
                upgrade_member = Members.objects.get(member_id=member_id)
                upgrade_member.member_plan_id = 2
                upgrade_member.save()
            return redirect('/my_account/' + str(user.member_id))
