from django.views.generic import TemplateView
from django.shortcuts import redirect

from index.create_context import creatememberplan_context
from index.models import Conditions, Faqs
from profileuseraccount.models import MemberPlans


class WelcomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        host = self.request.META["HTTP_HOST"]
        user = self.request.user

        if not user.is_authenticated:
            if host in ['127.0.0.1:8000', 'www.printdatahub.com', 'printdatahub-dev.azurewebsites.net',
                        'localhost:8000']:
                return redirect('/home/')
            else:
                return redirect('/accounts/login/')

        # authenticated user landing
        if user.is_authenticated and not user.member_id:
            return redirect('/signup_landing/')

        elif user.is_authenticated and not user.member.active:
            return redirect('/wait_for_approval/')

        elif user.is_authenticated and user.member.active and user.member.producerplan:
            return redirect('/producer_sales_dashboard/0')

        elif user.is_authenticated and user.member.active and not user.member.producerplan:
            return redirect('/printdataplatform_dashboard/')

        else:
            return redirect('/no_access/')


class WaitForApproval(TemplateView):
    template_name = 'wait_for_approval.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif user.is_authenticated and user.member.active and user.member.producerplan:
            return redirect('/producer_sales_dashboard/0')

        elif user.is_authenticated and user.member.active and not user.member.producerplan:
            return redirect('/printdataplatform_dashboard/')
        else:
            return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'homepage/startpage.html'

    def get_context_data(self, *args, **kwargs):
        language_id = 1

        context = super(HomeView, self).get_context_data(**kwargs)
        context['plan1'] = MemberPlans.objects.filter(member_plan_id=1, language_id=language_id).first()
        context['plan2'] = MemberPlans.objects.filter(member_plan_id=2, language_id=language_id).first()
        context['plan3'] = MemberPlans.objects.filter(member_plan_id=3, language_id=language_id).first()
        context['plan4'] = MemberPlans.objects.filter(member_plan_id=4, language_id=language_id).first()

        return context


class PricingView(TemplateView):
    template_name = 'homepage/components/pricing.html'


class ConditionView(TemplateView):
    template_name = 'homepage/conditions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ConditionView, self).get_context_data(**kwargs)
        user = self.request.user
        context = creatememberplan_context(context, user)
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
