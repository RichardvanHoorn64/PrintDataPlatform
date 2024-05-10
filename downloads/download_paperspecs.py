from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from materials.models import PaperBrand


class DownloadPaperBrands(LoginRequiredMixin, TemplateView):
    template_name = "materials/paper_brands.html"
    pk_url_kwarg = 'papercategory_id'

    def get_context_data(self, **kwargs):
        context = super(DownloadPaperBrands, self).get_context_data(**kwargs)
        papercategory_id = self.kwargs['papercategory_id']

        if papercategory_id == 0:
            paperbrand_list = PaperBrand.objects.all()
        else:
            paperbrand_list = PaperBrand.objects.filter(papercategory_id=papercategory_id)
        context['paperbrand_list'] = paperbrand_list
        return context
