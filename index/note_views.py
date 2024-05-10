from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from methods.models import *


class DeleteNoteView(View, LoginRequiredMixin):
    model = Notes

    # dispatch is called when the class instance loads
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')
        else:
            note_id = kwargs['note_id']
            note_deleted = Notes.objects.get(note_id=note_id, member_id=request.user.member_id)
            note_deleted.delete()
            return redirect(request.META.get('HTTP_REFERER'))
