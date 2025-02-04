from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class TriggerError(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
          test = 1 / 0  # Force a ZeroDivisionError
          print(test)
