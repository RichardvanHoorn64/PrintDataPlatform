from index.display_functions import *
from index.site_startfunctions import define_site_name, img_loc_logo
from printprojects.models import ProductCategory


def creatememberplan_context(context, user):
    context['site_name'] = define_site_name(user)
    context['img_loc_logo'] = img_loc_logo(user)
    context['starter_memberplans'] = starter_memberplans
    context['free_memberplans'] = free_memberplans
    context['open_memberplans'] = open_memberplans
    context['pro_memberplans'] = pro_memberplans
    context['non_exclusive_memberplans'] = non_exclusive_memberplans
    context['producer_memberplans'] = producer_memberplans
    context['producer_pro_memberplans'] = producer_pro_memberplans
    context['offer_availeble'] = offer_availeble
    context['printdataplatform_url'] = 'https://www.printdataplatform.nl'
    context['categories_all'] = categories_all
    context['categories_plano'] = categories_plano
    context['categories_folders'] = categories_folders
    context['categories_selfcovers'] = categories_selfcovers
    context['categories_brochures_all'] = categories_brochures_all
    context['categories_brochures_cover'] = categories_brochures_cover
    context['categories_all_no_envelopes']  = categories_all_no_envelopes
    context['categories_plano_no_folder']  = categories_plano_no_folder
    context['categories_plano_envelopes'] = categories_plano_envelopes
    context['categories_stapled'] = categories_stapled
    context['categories_envelopes'] = categories_envelopes

    if user.member_plan_id in producer_memberplans:
        context['producer'] = Producers.objects.get(producer_id=user.producer_id)
    return context


def createprintproject_context(context, user, printproject):
    context = creatememberplan_context(context, user)
    productcategory = ProductCategory.objects.get(productcategory_id=printproject.productcategory_id).productcategory
    printproject_title = printproject_description(printproject, productcategory)

    context['productcategory_id'] = printproject.productcategory_id
    context['printproject_title'] = printproject_title
    context['printproject_own_quotenumber'] = printproject_own_quotenumber(printproject)
    context['member_id'] = user.member_id
    context['printproject'] = printproject
    context['productcategory'] = printproject.productcategory
    context['productcategory_cover'] = [4, 5]
    context['productcategory_brochures'] = [3, 4, 5]
    context['printproject_requester'] = describe_requester(printproject)
    context['printproject_size'] = printproject_size(printproject)
    context['member_id'] = user.member_id
    context['printproject_paper'] = printproject_paper(printproject.papercategory, printproject.paperbrand,
                                                       printproject.paperweight, printproject.papercolor)
    context['printproject_printing_booklet'] = printproject_printing_booklet(
        printproject.print_booklet,
        printproject.number_pms_colors_booklet,
        printproject.pressvarnish_booklet)

    context['printproject_printing_cover'] = printproject_printing(printproject.printsided, printproject.print_front,
                                                                   printproject.print_back,
                                                                   printproject.number_pms_colors_front,
                                                                   printproject.number_pms_colors_back)

    context['printproject_paper_cover'] = printproject_paper(printproject.papercategory_cover,
                                                             printproject.paperbrand_cover,
                                                             printproject.paperweight_cover,
                                                             printproject.papercolor_cover)
    context['printproject_printing'] = printproject_printing(printproject.printsided, printproject.print_front,
                                                             printproject.print_back,
                                                             printproject.number_pms_colors_front,
                                                             printproject.number_pms_colors_back)
    context['printproject_varnish'] = printproject_varnish(printproject.printsided, printproject.pressvarnish_front,
                                                           printproject.pressvarnish_back)
    context['printproject_enhance'] = printproject_enhance(printproject.productcategory_id,
                                                           printproject.enhance_sided, printproject.enhance_front,
                                                           printproject.enhance_back, )
    context['printproject_finishing'] = printproject_finishing(printproject)

    context['printproject_packaging'] = printproject_packaging(printproject.packaging)

    context['printproject_message_extra_work'] = printproject_message_extra_work(printproject.message_extra_work)

    context['printproject_salesprice'] = printproject_salesprice(printproject)
    context['printproject_salesprice1000extra'] = printproject_salesprice1000extra(printproject)
    context['printproject_invoiceturnover'] = printproject_invoiceturnover(printproject)
    context['offer_table_title'] = "Aanbiedingen voor: " + printproject_title

    context['printproject_clientcontact'] = printproject_clientcontact(printproject.clientcontact_id)
    context['printproject_client_quotenumber'] = printproject_client_quotenumber(printproject.client_quotenumber)
    context['printproject_number_of_pages'] = printproject_number_of_pages(printproject)

    if printproject.productcategory_id in categories_envelopes:
        context['printproject_env_size_close_cut'] = display_env_size_close_cut(printproject)
        context['printproject_env_material_color'] = display_env_material_color(printproject)
        context['printproject_env_window'] = display_env_window(printproject)

    return context
