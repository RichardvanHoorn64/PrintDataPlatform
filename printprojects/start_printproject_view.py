import math
from django.shortcuts import redirect
from assets.models import Bindingmachines
from index.create_context import creatememberplan_context
from index.forms.form_invalids import form_invalid_message_quotes
from index.translate_functions import *
from index.convert_functions import *
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

        print('form: ', form.cleaned_data)

        paperbrand = form.cleaned_data['paperbrand']
        paperweight = form.cleaned_data['paperweight']
        paperbrand_cover = form.cleaned_data['paperbrand_cover']
        paperweight_cover = form.cleaned_data['paperweight_cover']

        if productcategory_id not in categories_envelopes:
            form.instance.papercolor = PaperCatalog.objects.filter(producer_id=1,
                                                                   paperbrand=paperbrand,
                                                                   paperweight_m2=paperweight).values_list('papercolor',
                                                                                                           flat=True).first()

        if productcategory_id in categories_brochures_cover:
            form.instance.papercolor_cover = PaperCatalog.objects.filter(producer_id=1,
                                                                         paperbrand=paperbrand_cover,
                                                                         paperweight_m2=paperweight_cover).values_list(
                'papercolor', flat=True).first()

        # fill general data
        form.instance.productcategory_id = productcategory_id
        form.instance.user_id = user.id
        form.instance.member_id = user.member_id
        form.instance.portrait_landscape = find_orientation(form.cleaned_data['portrait_landscape'])
        form.instance.packaging = find_packaging_id(form.cleaned_data['packaging'])

        # fill colors
        print_front = int(form.cleaned_data['print_front'])
        print_back = int(form.cleaned_data['print_back'])
        number_pms_colors_front = form.cleaned_data['number_pms_colors_front']
        number_pms_colors_back = form.cleaned_data['number_pms_colors_back']

        # fill empty pms
        if number_pms_colors_front == "":
            number_pms_colors_front = 0
        if number_pms_colors_back == "":
            number_pms_colors_back = 0

        if productcategory_id in categories_brochures_all:
            printsided = 2
        else:
            printsided = define_print_sided(print_front, print_back, number_pms_colors_front, number_pms_colors_back)

        # fill print back
        if productcategory_id in categories_selfcovers:
            print_front = 0
            print_back = 0
            printsided = 2
            pressvarnish_front = 0
            pressvarnish_back = 0

        else:
            pressvarnish_front = form.cleaned_data['pressvarnish_front']
            pressvarnish_back = form.cleaned_data['pressvarnish_back']

        if printsided == 2:
            print_back = print_front
            pressvarnish_back = pressvarnish_front
        if printsided == 1:
            print_back = 0
            form.instance.number_pms_colors_back = 0
            form.instance.pressvarnish_back = 0

        if productcategory_id in categories_envelopes:
            pressvarnish_front = 0
            pressvarnish_back = 0

        form.instance.printsided = printsided
        form.instance.print_front = print_front
        form.instance.print_back = print_back
        form.instance.pressvarnish_front = pressvarnish_front
        form.instance.pressvarnish_back = pressvarnish_back

        # handling pms data
        number_pms_colors_front = form.cleaned_data['number_pms_colors_front']
        number_pms_colors_back = form.cleaned_data['number_pms_colors_back']

        if number_pms_colors_front is None:
            number_pms_colors_front = 0
        if number_pms_colors_back is None:
            number_pms_colors_back = 0
        if printsided == 2:
            number_pms_colors_back = number_pms_colors_front
        form.instance.number_pms_colors_front = number_pms_colors_front
        form.instance.number_pms_colors_back = number_pms_colors_back

        if not productcategory_id in categories_brochures_cover:
            form.instance.paperweight_cover = 0

        if productcategory_id in categories_plano_envelopes:
            form.instance.pressvarnish_booklet = 0
            form.instance.finishing_brochures = 0

        if not productcategory_id in categories_envelopes:
            form.instance.paperweight_cover = 0
            form.instance.pressvarnish_booklet = 0
            form.instance.finishing_brochures = 0
            form.instance.folding = 0

        # Fill PrintProject-status
        form.instance.printprojectstatus_id = 1

        if productcategory_id in categories_envelopes:
            env_category_id = form.cleaned_data['env_category_id']
            env_size_close_cut = form.cleaned_data['env_size_close_cut']
            env_material_color = form.cleaned_data['env_material_color']
            env_window = form.cleaned_data['env_window']
            env = EnvelopeCatalog.objects.filter(env_category_id=env_category_id, env_size_close_cut=env_size_close_cut,
                                                 env_material_color=env_material_color, env_window=env_window,
                                                 producer_id=1)[0]
            form.instance.height_mm_product = env.env_height_mm
            form.instance.width_mm_product = env.env_width_mm
            form.instance.standard_size = 0

        # Fill size
        if productcategory_id not in categories_envelopes:
            standardsize_id = form.cleaned_data['standard_size']
            try:
                standard_size = StandardSize.objects.get(standardsize_id=standardsize_id)
                form.instance.height_mm_product = standard_size.height_mm_product
                form.instance.width_mm_product = standard_size.width_mm_product
                form.instance.standard_size = standard_size
            except StandardSize.DoesNotExist:
                form.instance.height_mm_product = form.cleaned_data['height_mm_product']
                form.instance.width_mm_product = form.cleaned_data['width_mm_product']
                form.instance.standard_size = 0

        # portrait_landscape
        if form.cleaned_data['portrait_landscape'] == 0:
            form.instance.portrait_landscape = 1  # staand

        if productcategory_id in categories_folders:
            folding_id = int(form.cleaned_data['folding'])
            # folding_id = find_foldingspecs(folding)
            form.instance.folding = folding_id
            form.instance.number_of_pages = find_folding_number_of_pages(folding_id)
        else:
            form.instance.folding = 0
            form.instance.number_of_pages = form.cleaned_data['number_of_pages']

        # number of pages brochures
        if productcategory_id in categories_brochures_all:
            number_of_pages = form.cleaned_data['number_of_pages']
            form.instance.number_of_pages = 4 * math.ceil(number_of_pages) / 4

        # fill enhance sided
        if productcategory_id in categories_brochures_all:
            form.instance.enhance_sided = 1
            form.instance.enhance_back = 0
        elif productcategory_id in categories_envelopes:
            form.instance.enhance_sided = 0
            form.instance.enhance_back = 0
        else:
            enhance_front = int(form.cleaned_data['enhance_front'])
            enhance_back = int(form.cleaned_data['enhance_back'])
            form.instance.enhance_sided = define_enhance_sided(enhance_front, enhance_back)

        # for envelopes
        if productcategory_id in categories_envelopes:
            form.instance.packaging = 1

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print("form is invalid, response :", response)
        print("form errors :", form.errors)
        print("form cleaned_data :", form.cleaned_data)
        form_invalid_message_quotes(form, response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        productcategory_id = self.kwargs['productcategory_id']
        productcategory = ProductCategory.objects.get(productcategory_id=productcategory_id)
        context['update'] = False

        creatememberplan_context(context, user)
        language_id = user.language_id
        dropdowns = DropdownChoices.objects.filter(language_id=user.language_id)

        member_plan_id = user.member_plan_id
        show_papercolor = True

        # categories
        context['productcategory'] = productcategory
        context['productcategory_id'] = productcategory_id

        # standardsizes
        standardsizes = StandardSize.objects.filter(productcategory_id=productcategory_id).order_by('standardsize_id')
        context['standardsizes'] = standardsizes

        # papercatalog producer
        papercatalog = PaperCatalog.objects.filter(producer_id=1)

        # papercategories general
        papercategories = papercatalog.values()

        # papercategories folders
        if productcategory_id in [categories_folders, categories_brochures_all]:
            papercategories = papercatalog.filter(paperweight_m2__lte=300).values()

        # papercategories booklet
        if productcategory_id in categories_brochures_all:
            papercategories = papercatalog.filter(singe_sided=False, paperweight_m2__lte=170).values()

        # papercategories booklet
        if productcategory_id in categories_envelopes:
            envelopecategories = EnvelopeCategory.objects.filter(producer_id=1)
        else:
            envelopecategories = []

        context['envelopecategories'] = envelopecategories

        # papercategories cover
        papercategories_cover = papercatalog.values()

        context['papercategories'] = papercategories.distinct('papercategory').order_by('papercategory')
        context['papercategories_cover'] = papercategories_cover.distinct('papercategory').order_by('papercategory')

        context['button_text'] = "Start Project"
        context['form_title'] = str(productcategory.productcategory) + ": Nieuw printproject"

        # context['member_id'] = user.member_id
        context['clients'] = Clients.objects.filter(member_id=user.member_id).order_by('client')
        context['printsided_choices'] = dropdowns.filter(dropdown='printsided_choices')
        context['print_choices'] = dropdowns.filter(dropdown='print_choices').order_by('-value')
        context['portrait_landscape_choices'] = dropdowns.filter(dropdown='portrait_landscape_choices')
        context['pressvarnish_choices'] = dropdowns.filter(dropdown='pressvarnish_choices')

        # Enhance_choices
        if productcategory_id in categories_plano:
            context['enhance_sided_choices'] = dropdowns.filter(dropdown='enhance_sided_choices').order_by(
                'dropdown_id')

        # Folders foldingmethods
        if productcategory_id in categories_folders:
            context['foldingmethods'] = FoldingMethods.objects.all().order_by('foldingmethod_id')

        if productcategory_id in categories_selfcovers:
            context['type_booklet'] = ' selfcover'

        if productcategory_id in categories_brochures_cover:
            context['type_booklet'] = ' binnenwerk'

        enhance_choices = EnhancementOptions.objects.filter(language_id=language_id)
        packaging_choices = PackagingOptions.objects.filter(language_id=language_id).order_by('packagingoption_id')

        # Brochures finishingmethods
        brochure_finishingmethods = []
        if productcategory_id in categories_brochures_all:
            if productcategory_id in categories_stapled:
                brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=3)
            else:
                brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=5)

        if productcategory_id in categories_brochures_cover:
            print_type = " omslag"
            print_front = "buitenzijde omslag"
            print_back = "binnenzijde omslag"
            enhance_front = "buitenzijde omslag"
            enhance_back = ""

        else:
            print_type = ""
            print_front = "voorzijde"
            print_back = "achterzijde"
            enhance_front = "voorzijde"
            enhance_back = "achterzijde"

        context['packaging_choices'] = packaging_choices
        context['no_enhancement'] = 'Geen verdeling'
        context['enhance_choices'] = enhance_choices.order_by('enhancement_id')
        context['brochure_finishingmethods'] = brochure_finishingmethods
        context['show_papercolor'] = show_papercolor
        context['print_type'] = print_type
        context['print_front'] = print_front
        context['print_back'] = print_back
        context['print_front'] = enhance_front
        context['enhance_back'] = enhance_back
        return context
