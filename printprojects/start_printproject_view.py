from django.shortcuts import redirect
from assets.models import Bindingmachines
from index.translate_functions import *
from index.exclusive_functions import define_exclusive_producer_id
from members.crm_functions import update_producersmatch
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from materials.models import *
from methods.models import *
from printprojects.forms.NewPrintProject import PrintProjectsForm
from index.models import DropdownChoices
from methods.models import StandardSize, FoldingMethods
from producers.models import PackagingTariffs, EnhancementTariffs
from index.categories_groups import *


# Create your views here.
class CreateNewPrintProjectView(LoginRequiredMixin, CreateView):
    model = PrintProjects
    form_class = PrintProjectsForm
    template_name = 'printprojects/new_project.html'
    pk_url_kwarg = 'productcategory_id'
    context_object_name = 'productcategory_id'

    def get_success_url(self):
        printproject_id = self.object.printproject_id
        return '/start_printproject_workflow/' + str(printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        productcategory_id = self.kwargs['productcategory_id']
        update_producersmatch(self.request)
        user = self.request.user

        # fill general data
        form.instance.productcategory_id = productcategory_id
        form.instance.user_id = user.id
        form.instance.member_id = user.member_id

        form.instance.portrait_landscape = find_orientation(form.cleaned_data['portrait_landscape'])

        # fill print rear
        printsided = form.cleaned_data['printsided']
        print_front = form.cleaned_data['print_front']
        number_pms_colors_front = form.cleaned_data['number_pms_colors_front']
        pressvarnish_front = form.cleaned_data['pressvarnish_front']
        pressvarnish_rear = form.cleaned_data['pressvarnish_rear']

        # enhance
        if productcategory_id in categories_brochures_all:
            form.instance.enhance_sided = 1
            form.instance.enhance_rear = 0
        else:
            form.instance.enhance_sided = form.cleaned_data['enhance_sided']
        form.instance.enhance_front = find_enhancement_id(form.cleaned_data['enhance_front'])
        form.instance.enhance_rear = find_enhancement_id(form.cleaned_data['enhance_rear'])

        if printsided == 2:
            form.instance.print_rear = print_front
            form.instance.number_pms_colors_rear = number_pms_colors_front
            form.instance.pressvarnish_rear = pressvarnish_front
        elif printsided == 1:
            form.instance.print_rear = 0
            form.instance.number_pms_colors_rear = 0
            form.instance.pressvarnish_rear = 0
        else:
            form.instance.pressvarnish_rear = pressvarnish_rear

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

        # Fill PrintProject-status
        form.instance.printprojectstatus_id = 1

        # Fill size
        standardsize_id = form.cleaned_data['standard_size']

        if standardsize_id != 0:
            standard_size = StandardSize.objects.get(standardsize_id=standardsize_id)
            form.instance.height_mm_product = standard_size.height_mm_product
            form.instance.width_mm_product = standard_size.width_mm_product
            form.instance.standard_size = standard_size
        else:
            form.instance.height_mm_product = form.cleaned_data['height_mm_product']
            form.instance.width_mm_product = form.cleaned_data['width_mm_product']
            form.instance.standard_size = 0

        if productcategory_id in categories_folders:
            folding = find_foldingspecs(form.cleaned_data['folding'])
            form.instance.folding = folding[0]
            form.instance.number_of_pages = folding[1]
        else:
            form.instance.folding = 0
            form.instance.number_of_pages = form.cleaned_data['number_of_pages']

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print("form is invalid, response :", response)
        print("form errors :", form.errors)
        print("form cleaned_data :", form.cleaned_data)
        # form_invalid_message_quotes(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        user = self.request.user
        language_id = user.language_id
        dropdowns = DropdownChoices.objects.filter(language_id=language_id)
        exclusive_producer_id = define_exclusive_producer_id(user)
        context = super().get_context_data(**kwargs)
        productcategory_id = self.kwargs['productcategory_id']
        productcategory = ProductCategory.objects.get(productcategory_id=productcategory_id)
        context['update'] = False
        brochure_finishingmethods = []

        # categories
        context['productcategory'] = productcategory
        context['productcategory_id'] = productcategory.productcategory_id
        context['categories_all'] = categories_all
        context['categories_plano'] = categories_plano
        context['categories_folders'] = categories_folders
        context['categories_selfcovers'] = categories_selfcovers
        context['categories_brochures_all'] = categories_brochures_all
        context['categories_brochures_cover'] = categories_brochures_cover

        # standardsizes
        standardsizes = StandardSize.objects.filter(productcategory_id=productcategory_id)
        context['standardsizes'] = standardsizes

        # papercategories
        papercategories = PaperCategories.objects.filter(producer_id=exclusive_producer_id).values().order_by(
            'papercategory_id')
        if productcategory_id in categories_folders:
            papercategories = PaperCategories.objects.filter(producer_id=exclusive_producer_id,
                                                             folders_cover=True).values().order_by(
                'papercategory_id')
        if productcategory_id in categories_brochures_all:
            papercategories = PaperCategories.objects.filter(producer_id=exclusive_producer_id,
                                                             brochures_booklet=True).values().order_by(
                'papercategory_id')

        papercategories_cover = PaperCategories.objects.filter(producer_id=exclusive_producer_id,
                                                               brochures_cover=True).values().order_by(
            'papercategory_id')

        context['papercategories'] = papercategories
        context['papercategories_cover'] = papercategories_cover

        context['button_text'] = "Start Project"
        context['form_title'] = str(productcategory.productcategory) + ": Nieuw printproject"

        # context['member_id'] = user.member_id
        context['clients'] = Clients.objects.filter(member_id=user.member_id).order_by('client')
        context['printsided_choices'] = dropdowns.filter(dropdown='printsided_choices')
        context['print_choices'] = dropdowns.filter(dropdown='print_choices')
        context['portrait_landscape_choices'] = dropdowns.filter(dropdown='portrait_landscape_choices')
        context['pressvarnish_choices'] = dropdowns.filter(dropdown='pressvarnish_choices')

        # Enhance_choices
        if productcategory_id in categories_plano:
            context['enhance_sided_choices'] = dropdowns.filter(dropdown='enhance_sided_choices').order_by(
                'dropdown_id')

        enhance_choices = EnhancementOptions.objects.filter(language_id=language_id).order_by('enhancement_id')
        if exclusive_producer_id:
            enhance_options_producer = list(
                EnhancementTariffs.objects.filter(producer_id=exclusive_producer_id).values('enhancementtariff_id'))
            enhance_choices = enhance_choices.filter(enhancementption_id__in=enhance_options_producer)

        context['enhance_choices'] = enhance_choices
        context['no_enhancement'] = "Geen veredeling"

        # Packaging choices
        packaging_choices = PackagingOptions.objects.filter(language_id=language_id).order_by('packagingoption_id')

        if exclusive_producer_id:
            packagingoptions_producer = list(
                PackagingTariffs.objects.filter(producer_id=exclusive_producer_id).values('packagingtariff_id'))
            packaging_choices = packaging_choices.filter(packagingoption_id__in=packagingoptions_producer)

        context['packaging_choices'] = packaging_choices

        # Folders foldingmethods
        if productcategory_id in categories_folders:
            context['foldingmethods'] = FoldingMethods.objects.all().order_by('foldingmethod_id')

        # Brochures finishingmethods
        if productcategory_id in categories_brochures_all:
            if productcategory_id in categories_stapled:
                brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=3)
            else:
                brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=5)

            if exclusive_producer_id:
                bindingoptions_producer = list(
                    Bindingmachines.objects.filter(producer_id=exclusive_producer_id).values('finishingmethod_id'))
                brochure_finishingmethods = brochure_finishingmethods.filter(
                    finishingmethod_id__in=bindingoptions_producer)

        context['brochure_finishingmethods'] = brochure_finishingmethods

        if productcategory_id in categories_selfcovers:
            context['type_booklet'] = ' selfcover'

        if productcategory_id in categories_brochures_cover:
            context['type_booklet'] = ' binnenwerk'

        return context
