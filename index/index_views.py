from django.views.generic import TemplateView
from django.shortcuts import redirect

from index.models import Conditions, Faqs
from profileuseraccount.models import MemberPlans


class WelcomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        host = self.request.META["HTTP_HOST"]
        user = self.request.user

        if not user.is_authenticated:
            if host in ['127.0.0.1:8000', 'www.printdatahub.com', 'printdatahub-dev.azurewebsites.net', 'localhost:8000' ]:
                return redirect('/home/')
            else:
                return redirect('/accounts/login/')

        # authenticated user landing
        if user.is_authenticated and not user.member_id:
            return redirect('/signup_landing/')

        elif user.is_authenticated and not user.member.active:
            return redirect('/wait_for_approval/')

        elif user.is_authenticated and user.member_id and user.member.memberplan_id == 4:
            return redirect('/producer_sales_dashboard/0')

        elif user.is_authenticated and user.member_id and user.member.memberplan_id != 4:
            return redirect('/printdataplatform_dashboard/')

        else:
            return redirect('/no_access/')


class HomeView(TemplateView):
    template_name = 'homepage/startpage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['plan1'] = MemberPlans.objects.filter(memberplan=1).first()
        context['plan2'] = MemberPlans.objects.filter(memberplan=2).first()
        context['plan3'] = MemberPlans.objects.filter(memberplan=3).first()
        context['plan4'] = MemberPlans.objects.filter(memberplan=4).first()

        return context


class PricingView(TemplateView):
    template_name = 'homepage/components/pricing.html'


class ConditionView(TemplateView):
    template_name = 'homepage/conditions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ConditionView, self).get_context_data(**kwargs)
        language_id = self.request.user.language_id
        context['conditions'] = Conditions.objects.filter(language_id=language_id).order_by('sequence')
        if language_id == 1:
            context['title'] = "Spelregels"
            context[
                'subtitle'] = "Door gebruik te maken van het PrintDataPlatform geeft u aan akkoord te zijn met onze spelregels"
        if language_id == 2:
            context['title'] = "Questions and answers"
            context['subtitle'] = "We love to help"
        return context


class FaqView(TemplateView):
    template_name = 'homepage/faq.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        language_id = self.request.user.language_id
        if language_id == 1:
            context['title'] = "Vragen en antwoorden"
            context['subtitle'] = "We helpen graag"
        if language_id == 2:
            context['title'] = "Questions and answers"
            context['subtitle'] = "We love to help"

        context['faqs'] = Faqs.objects.filter(language_id=language_id).order_by('sequence')
        return context
