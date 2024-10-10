from django.views.generic import TemplateView
from django.shortcuts import redirect
from index.categories_groups import *
from index.create_context import creatememberplan_context
from index.exclusive_functions import img_loc_logo
from index.models import *
from profileuseraccount.models import UserProfile, Members


class WelcomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        if not user.active:
            return redirect('/no_access/')

        # authenticated user landing
        if user.is_authenticated and not user.member_id:
            return redirect('/signup_landing/')

        elif user.is_authenticated and not user.member.active:
            in_whitelist = Whitelist.objects.filter(type='email',
                                                    whitelist_text='demodrukker@printdataplatform.nl').exists()

            if in_whitelist:
                try:
                    user = UserProfile.objects.get(pk=user.id)
                    user.active = True
                    user.save()
                except UserProfile.DoesNotExist:
                    pass

                try:
                    member = Members.objects.get(member_id=user.member_id)
                    member.active = True
                    member.save()
                except Members.DoesNotExist:
                    pass

            if not in_whitelist:
                return redirect('/wait_for_approval/')

        # set as producer
        is_producer = Whitelist.objects.filter(type='producer', whitelist_text=str(user.member_id)).exists()
        if is_producer and user.member_plan_id == 1:
            try:
                user = UserProfile.objects.get(pk=user.id)
                user.member_plan_id = 4
                user.save()
            except UserProfile.DoesNotExist:
                pass

            try:
                member = Members.objects.get(member_id=user.member_id)
                member.producerplan = True
                member.member_plan_id = 4
                member.save()
            except Members.DoesNotExist:
                pass

            if not user.producer_id:
                new_producer = Producers(
                    active=True,
                    user_admin=user.id,
                    company=user.company,
                    manager=user.first_name + " " + user.last_name,
                    tel_general=user.tel_general,
                    mobile_number=user.mobile_number,
                    e_mail_general=user.e_mail_general,
                    street_number=user.street_number,
                    postal_code=user.postal_code,
                    city=user.city,
                    member_plan_id=user.member_plan_id,
                    language_id=user.language_id,
                )

                try:
                    new_producer.save()
                    my_profile = UserProfile.objects.get(id=user.id)
                    my_profile.producer_id = new_producer.producer_id
                    my_profile.save()
                except UserProfile.DoesNotExist:
                    pass

            else:
                pass

            if user.member_plan_id == 1:
                return redirect('/printdataplatform_dashboard/')
            elif user.member_plan_id == 4:
                return redirect('/producer_sales_dashboard/0')
            else:
                return redirect('/wait_for_approval/')

        elif user.is_authenticated and user.member.active and user.member_plan_id not in producer_memberplans:
            return redirect('/printdataplatform_dashboard/')

        elif user.is_authenticated and user.member.active and user.member_plan_id in producer_memberplans:
            return redirect('/producer_sales_dashboard/0')

        elif user.is_authenticated and user.member.active and user.member_plan_id not in producer_memberplans:
            return redirect('/printdataplatform_dashboard/')

        else:
            return redirect('/no_access/')


class WaitForApproval(TemplateView):
    template_name = 'wait_for_approval.html'


class PricingView(TemplateView):
    template_name = 'homepage/components/pricing.html'


class ConditionView(TemplateView):
    template_name = 'homepage/conditions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ConditionView, self).get_context_data(**kwargs)
        user = self.request.user
        skin = 'skins/skin_open.html'
        language_id = 1
        page = 'Home'

        if user.is_authenticated:
            context = creatememberplan_context(context, user)
            skin = 'skins/skin.html'
            language_id = self.request.user.language_id
            page = 'Dashboard' + str(user.company)
        else:
            context['img_loc_logo'] = img_loc_logo(user)

        if language_id == 1:
            context['title'] = 'Spelregels PrintDataPlatform'
            context[
                'subtitle'] = ("Door gebruik te maken van het PrintDataPlatform geeft u aan akkoord te zijn met onze "
                               "spelregels")
        if language_id == 2:
            context['title'] = 'Conditions PrintDataPlatform'
            context['subtitle'] = "By using the PrintDataPlatform you agree to our conditions"

        context['skin'] = skin
        context['page'] = page

        context['conditions'] = Conditions.objects.filter(language_id=language_id).order_by('sequence')
        return context


class FaqView(TemplateView):
    template_name = 'homepage/faq.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        user = self.request.user
        language_id = self.request.user.language_id
        context = creatememberplan_context(context, user)
        if language_id == 1:
            context['title'] = "Vragen en antwoorden"
            context['subtitle'] = "We helpen graag"
        if language_id == 2:
            context['title'] = "Questions and answers"
            context['subtitle'] = "We love to help"

        context['faqs'] = Faqs.objects.filter(language_id=language_id).order_by('sequence')
        return context


class EventsView(TemplateView):
    template_name = 'homepage/events.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        user = self.request.user
        language_id = self.request.user.language_id
        events = Events.objects.filter(language_id=language_id).order_by('sequence')

        context = creatememberplan_context(context, user)
        context['title'] = "Events"

        if language_id == 1:
            if events:
                context['subtitle'] = "Meld je aan voor een van onze bijeenkomsten"
            else:
                context['subtitle'] = "Nog geen  bijeenkomsten gepland"
        if language_id == 2:
            if events:
                context['subtitle'] = "Register for one of our meetings"
            else:
                context['subtitle'] = "No meetings planned yet"

        context['events'] = Events.objects.filter(language_id=language_id).order_by('sequence')
        return context


class TestErrorView(TemplateView):
    template_name = 'account/password_reset_done.html'
