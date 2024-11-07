from django.shortcuts import redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from assets.models import Bindingmachines
from index.categories_groups import *
from index.exclusive_functions import define_exclusive_producer_id
from index.forms.form_invalids import form_invalid_message_quotes
from index.models import DropdownChoices, BrandPortalData
from index.translate_functions import find_packaging_id
from materials.models import PaperCatalog
from methods.models import *
from printprojects.forms.NewPrintProject import PrintProjectsForm
from index.create_context import createprintproject_context
from producers.models import EnhancementTariffs, PackagingTariffs


# Creating a clone of a printproject
class PrintProjectCloneView(LoginRequiredMixin, RedirectView):
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.member.active:
            return redirect('/wait_for_approval/')

        clone_printproject = PrintProjects.objects.get(printproject_id=self.kwargs['printproject_id'])
        clone_printproject.printproject_id = None
        clone_printproject.printprojectstatus_id = 1
        clone_printproject.project_title = "Kopie: " + clone_printproject.project_title
        clone_printproject.save()
        new_printproject_id = clone_printproject.printproject_id
        return '/printproject_update/' + str(new_printproject_id)


# Updating a (clone) printproject
class PrintProjectCloneUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'printprojects/new_project.html'
    pk_url_kwarg = 'printproject_id'
    context_object_name = 'printproject_id'
    model = PrintProjects
    form_class = PrintProjectsForm

    def get_success_url(self):
        return '/start_printproject_workflow/' + str(self.object.printproject_id)

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = PrintProjects.objects.get(printproject_id=self.kwargs['printproject_id'])
        productcategory_id = item.productcategory_id

        if form.cleaned_data['papercategory'] == "0":
            form.instance.papercategory = item.papercategory
            form.instance.paperbrand = item.paperbrand
            form.instance.paperweight = item.paperweight
            form.instance.papercolor = item.papercolor

        if productcategory_id in categories_selfcovers:
            form.instance.printsided = item.printsided
            form.instance.print_front = item.print_front
            form.instance.print_rear = item.print_rear
            form.instance.number_pms_colors_front = item.number_pms_colors_front
            form.instance.number_pms_colors_rear = item.number_pms_colors_rear
            form.instance.pressvarnish_front = item.pressvarnish_front
            form.instance.pressvarnish_rear = item.pressvarnish_rear
            form.instance.printsided = item.printsided
            form.instance.enhance_front = item.enhance_front
            form.instance.enhance_rear = item.enhance_rear
            form.instance.enhance_sided = item.enhance_sided
            form.instance.enhance_front = item.enhance_front
            form.instance.enhance_rear = item.enhance_rear
            form.instance.papercategory_cover = item.papercategory_cover
            form.instance.paperbrand_cover = item.paperbrand_cover
            form.instance.paperweight_cover = item.paperweight_cover
            form.instance.papercolor_cover = item.papercolor_cover

        if productcategory_id in categories_plano:
            form.instance.papercategory_cover = item.papercategory_cover
            form.instance.paperbrand_cover = item.paperbrand_cover
            form.instance.paperweight_cover = item.paperweight_cover
            form.instance.papercolor_cover = item.papercolor_cover

        if productcategory_id not in categories_folders:
            form.instance.folding = item.folding

        # packaging
        packaging = form.cleaned_data['packaging']
        if form.cleaned_data['packaging'] == "0":
            packaging = item.packaging
        else:
            packaging = find_packaging_id(packaging)
        form.instance.packaging = packaging

        # portrait_landscape
        if form.cleaned_data['portrait_landscape'] == "0":
            form.instance.portrait_landscape = item.portrait_landscape

        # client
        if form.cleaned_data['client_id'] == "0":
            form.instance.client_id = item.client_id

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_invalid_message_quotes(form, response)
        print("form_invalid_message:", response)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        member_plan_id = user.member.member_plan_id
        printproject_id = self.kwargs['printproject_id']
        printproject = PrintProjects.objects.get(printproject_id=printproject_id)
        productcategory_id = printproject.productcategory_id

        exclusive_producer_id = define_exclusive_producer_id(self.request.user)
        brandportal = BrandPortalData.objects.get(producer_id=exclusive_producer_id)

        language_id = user.language_id
        dropdowns = DropdownChoices.objects.filter(language_id=language_id)
        context = createprintproject_context(context, user, printproject)

        context['update'] = True
        context['button_text'] = 'Versturen'
        context['form_title'] = 'Printproject kopiëren'
        context['productcategories'] = ProductCategory.objects.all()
        context['member_id'] = user.member_id
        context['clients'] = Clients.objects.filter(member_id=user.member_id).order_by('client')

        # standardsizes
        standardsizes = StandardSize.objects.filter(productcategory_id=productcategory_id).order_by('standardsize_id')
        context['standardsizes'] = standardsizes

        # papercatalog producer
        papercatalog = PaperCatalog.objects.filter(producer_id=exclusive_producer_id)

        # papercategories general
        papercategories = papercatalog.values()

        # papercategories folders
        if productcategory_id in [categories_folders, categories_brochures_all]:
            papercategories = papercatalog.filter(singe_sided=False, paperweight_m2__lte=300).values()

        # papercategories booklet
        if productcategory_id in categories_brochures_all:
            papercategories = papercatalog.filter(singe_sided=True, paperweight_m2__lte=170).values()

        # papercategories cover
        papercategories_cover = papercatalog.values()

        context['papercategories'] = papercategories.distinct('papercategory').order_by('papercategory')
        context['papercategories_cover'] = papercategories_cover.distinct('papercategory').order_by('papercategory')

        # context['member_id'] = user.member_id
        if member_plan_id in pro_memberplans:
            try:
                client = Clients.objects.get(client_id=printproject.client_id, member_id=user.member_id).client
            except Clients.DoesNotExist:
                client = 'Geen opgave'
        else:
            client = 'Alleen voor pro accounts'

        context['client'] = client
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

        # exclusive producer dropdowns
        if member_plan_id in exclusive_memberplans:

            show_papercolor = brandportal.brandportal_show_papercolor

            if not brandportal.brandportal_show_pms_input:
                context['print_choices'] = dropdowns.filter(dropdown='print_choices').order_by('-value').exclude(
                    value=0)

            enhance_options_producer = EnhancementTariffs.objects.filter(
                producer_id=exclusive_producer_id).values_list(
                'enhancement_id', flat=True)
            enhance_choices = EnhancementOptions.objects.filter(language_id=language_id,
                                                                enhancement_id__in=enhance_options_producer)

            packagingoptions_producer = PackagingTariffs.objects.filter(
                producer_id=exclusive_producer_id).values_list(
                'packagingoption_id', flat=True)
            packaging_choices = PackagingOptions.objects.filter(language_id=language_id,
                                packagingoption_id__in=packagingoptions_producer).order_by('packagingoption_id')

            # Brochures finishingmethods exclusive producer
            bindingoptions_producer = Bindingmachines.objects.filter(producer_id=exclusive_producer_id).values_list(
                'finishingmethod_id', flat=True)
            brochure_finishingmethods = []
            if productcategory_id in categories_brochures_all:
                if productcategory_id in categories_stapled:
                    brochure_finishingmethods = BrochureFinishingMethods.objects.filter(
                        finishingmethod_id__in=bindingoptions_producer, productcategory_id=3)
                else:
                    brochure_finishingmethods = BrochureFinishingMethods.objects.filter(
                        finishingmethod_id__in=bindingoptions_producer, productcategory_id=5)
                context['show_papercolor'] = show_papercolor

        else:
            enhance_choices = EnhancementOptions.objects.filter(language_id=language_id)
            packaging_choices = PackagingOptions.objects.filter(language_id=language_id).order_by(
                'packagingoption_id')

            # Brochures finishingmethods
            brochure_finishingmethods = []
            if productcategory_id in categories_brochures_all:
                if productcategory_id in categories_stapled:
                    brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=3)
                else:
                    brochure_finishingmethods = BrochureFinishingMethods.objects.filter(productcategory_id=5)

        if productcategory_id in categories_brochures_cover:
            cover = " omslag"
        else:
            cover = ""
        context["cover"] = cover

        context['packaging_choices'] = packaging_choices

        context['no_enhancement'] = 'Geen verdeling'
        context['enhance_choices'] = enhance_choices.order_by('enhancement_id')

        context['brandportal'] = brandportal
        context['brochure_finishingmethods'] = brochure_finishingmethods
        context['show_papercolor'] = True
        context['print_type'] = ''
        if productcategory_id in categories_brochures_cover:
            context['print_type'] = 'omslag'
        return context
