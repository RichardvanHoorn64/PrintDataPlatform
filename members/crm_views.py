from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from printprojects.models import MemberProducerMatch


class ChangeMemberProducerStatus(TemplateView, LoginRequiredMixin):
    template_name = 'producers/new_producer.html'
    pk_url_kwarg = 'memberproducerstatus_id'
    context_object_name = 'memberproducerstatus_id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            memberproducermatch_id = kwargs.get('memberproducermatch_id')
            memberproducerstatus_id = kwargs.get('memberproducerstatus_id')
            update_record = MemberProducerMatch.objects.get(memberproducermatch_id=memberproducermatch_id)
            update_record.memberproducerstatus_id = memberproducerstatus_id
            update_record.save()
            return redirect('/producer_dashboard/0')
