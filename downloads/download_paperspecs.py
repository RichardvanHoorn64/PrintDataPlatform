from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from index.create_context import creatememberplan_context
from materials.models import *

class DownloadPaperBrands(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_brands.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(DownloadPaperBrands, self).get_context_data(**kwargs)
        paperbrand_list = PaperBrandReference.objects.all()
        context = creatememberplan_context(context, user)
        context['paperbrand_list'] = paperbrand_list
        return context
