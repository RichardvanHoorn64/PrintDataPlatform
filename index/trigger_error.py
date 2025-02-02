from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class TriggerError(LoginRequiredMixin, View):
    def dispatch(request):
        1 / 0  # Forceer een ZeroDivisionError
