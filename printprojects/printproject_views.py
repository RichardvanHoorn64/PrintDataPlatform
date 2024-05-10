from django.shortcuts import redirect

from members.crm_functions import update_producersmatch
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from index.forms.form_invalids import form_invalid_message_quotes
from materials.models import *
from methods.models import *
from printprojects.forms.NewPrintProject import PrintProjectsForm
from index.product_choices import *
from methods.models import StandardSize, FoldingMethods


# Create your views here.
class CreateNewPrintProjectView(LoginRequiredMixin, CreateView):
    model = PrintProjects
    form_class = PrintProjectsForm
    template_name = 'printprojects/new_project.html'

    def get_success_url(self):
        printproject_id = self.object.printproject_id
        return '/printproject_details/' + str(printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        update_producersmatch(self.request)
        user = self.request.user

        # fill general data
        form.instance.user_id = user.id
        form.instance.member_id = user.member_id
        form.instance.productcategory_id = form.cleaned_data['productcategory_id']

        # fill print rear
        printsided = form.cleaned_data['printsided']
        print_general = form.cleaned_data['print']
        number_pms_colors = form.cleaned_data['number_pms_colors']
        pressvarnish = form.cleaned_data['pressvarnish']

        if printsided == "Tweezijdig gelijk":
            form.instance.print_rear = print_general
            form.instance.number_pms_colors_rear = number_pms_colors
            form.instance.pressvarnish_rear = pressvarnish
        elif printsided == "Eenzijdig":
            form.instance.print_rear = "0"
            form.instance.number_pms_colors_rear = "0"
            form.instance.pressvarnish_rear = "Geen persvernis"
        else:
            pass

        # fill print rear cover
        printsided_cover = form.cleaned_data['printsided_cover']
        print_cover = form.cleaned_data['print_cover']
        number_pms_colors_cover = form.cleaned_data['number_pms_colors_cover']
        pressvarnish_cover = form.cleaned_data['pressvarnish_cover']

        if printsided_cover == "Tweezijdig gelijk":
            form.instance.print_rear_cover = print_cover
            form.instance.number_pms_colors_rear_cover = number_pms_colors_cover
            form.instance.pressvarnish_rear_cover = pressvarnish_cover
        elif printsided_cover == "Eenzijdig":
            form.instance.print_rear_cover = "0"
            form.instance.number_pms_colors_rear_cover = "0"
            form.instance.pressvarnish_rear_cover = "Geen persvernis"

        else:
            pass

        # fill paperdata strings
        paperspec_id = form.cleaned_data['papercolor']
        if paperspec_id:
            paperspec = PaperCatalog.objects.get(paperspec_id=paperspec_id)
            form.instance.papercategory = paperspec.papercategory
            form.instance.paperbrand = paperspec.paperbrand
            form.instance.paperweight = paperspec.paperweight_m2
            form.instance.papercolor = paperspec.papercolor
        else:
            form.instance.papercategory = 'New'
            form.instance.paperbrand = form.cleaned_data['paperbrand_new']
            form.instance.paperweight = form.cleaned_data['paperweight_new']
            form.instance.papercolor = form.cleaned_data['papercolor_new']

        # fill paperdata strings cover
        paperspec_id_cover = form.cleaned_data['papercolor_cover']
        if paperspec_id_cover:
            paperspec_cover = PaperCatalog.objects.get(paperspec_id=paperspec_id_cover)
            form.instance.papercategory_cover = paperspec_cover.papercategory
            form.instance.paperbrand_cover = paperspec_cover.paperbrand
            form.instance.paperweight_cover = paperspec_cover.paperweight_m2
            form.instance.papercolor_cover = paperspec_cover.papercolor
        else:
            form.instance.papercategory_cover = 'New'
            form.instance.paperbrand_cover_new = form.cleaned_data['paperbrand_cover_new']
            form.instance.paperweight_cover_new = form.cleaned_data['paperweight_cover_new']
            form.instance.papercolor_cover_new = form.cleaned_data['papercolor_cover_new']

        # Fill PrintProjectstatus
        form.instance.printprojectstatus_id = 1

        # Fill size
        standardsize_id = form.cleaned_data['standard_size']

        if standardsize_id != "0":
            standard_size = StandardSize.objects.get(standardsize_id=standardsize_id)
            form.instance.height_mm_product = standard_size.height_mm_product
            form.instance.width_mm_product = standard_size.width_mm_product
            form.instance.standard_size = standard_size
        else:
            form.instance.height_mm_product = form.cleaned_data['height_mm_product']
            form.instance.width_mm_product = form.cleaned_data['width_mm_product']
            form.instance.standard_size = 0

        foldingmethod_id = form.cleaned_data['folding']
        if foldingmethod_id != "0":
            data = FoldingMethods.objects.get(foldingmethod_id=foldingmethod_id)
            form.instance.number_of_pages = data.number_of_pages
            form.instance.folding = data.foldingmethod

        else:
            form.instance.folding = None

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['update'] = False
        context['button_text'] = "Start Project"
        context['form_title'] = "Start een nieuw printproject"

        context['productcategories'] = ProductCategory.objects.all()
        context['member_id'] = user.member_id
        context['clients'] = Clients.objects.filter(member_id=user.member_id).order_by('client')
        context['standardsizes'] = StandardSize.objects.filter(productcategory_id=1)
        context['printsided_choices'] = printsided_choices
        context['print_choices'] = print_choices
        context['portrait_landscape_choices'] = portrait_landscape_choices
        context['pressvarnish_choices'] = pressvarnish_choices
        context['enhance_sided_choices'] = enhance_sided_choices
        context['enhance_choices'] = enhance_choices
        context['packaging_choices'] = packaging_choices
        context['foldingmethods'] = FoldingMethods.objects.all().order_by('foldingmethod_id')

        return context
