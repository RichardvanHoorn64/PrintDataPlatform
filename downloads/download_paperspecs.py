from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from materials.models import *

class DownloadPaperBrands(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_brands.html"

    def get_context_data(self, **kwargs):
        context = super(DownloadPaperBrands, self).get_context_data(**kwargs)
        paperbrand_list = PaperBrandReference.objects.all()
        context['paperbrand_list'] = paperbrand_list
        return context
