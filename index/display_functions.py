from index.categories_groups import *
from index.models import *
from index.convert_functions import *
from printprojects.models import ClientContacts
from producers.models import ProducerProductOfferings
from producers.producer_functions import get_producercategories


def describe_requester(printproject):
    user = UserProfile.objects.get(id=printproject.user_id)
    requester = user.first_name + " " + user.last_name + ", " + user.company
    return requester


def printproject_client_quotenumber(client_quotenumber):
    if client_quotenumber:
        client_quotenumber = client_quotenumber
    else:
        client_quotenumber = "Geen opgave"
    return client_quotenumber


def printproject_own_quotenumber(printproject):
    if printproject.own_quotenumber:
        quotenumber = printproject.own_quotenumber
    else:
        quotenumber = printproject.printproject_id
    return quotenumber


def printproject_description(printproject, productcategory):
    text = str(printproject.volume) + " ex. " + productcategory + " " + printproject.project_title
    return text


def offer_salesprice(offer):
    if offer.offer:
        offerprice = '€ ' + str(offer.offer)
    else:
        offerprice = "Nog geen offerte uitgebracht"
    return offerprice


def offer_salesprice1000extra(offer):
    if offer.offer1000extra:
        offerprice1000extra = "€ " + str(offer.offer1000extra)
    else:
        offerprice1000extra = ''
    return offerprice1000extra


def printproject_salesprice(printproject):
    if printproject.salesprice:
        salesprice = "€ " + str(printproject.salesprice)
    else:
        salesprice = "Nog geen verkoopprijs ingevoerd"
    return salesprice


def printproject_salesprice1000extra(printproject):
    if printproject.salesprice_1000extra:
        salesprice_1000extra = "€ " + str(printproject.salesprice_1000extra)
    else:
        salesprice_1000extra = "Nog niet ingevoerd"
    return salesprice_1000extra


def printproject_invoiceturnover(printproject):
    if printproject.invoiceturnover:
        invoiceturnover = "€ " + str(printproject.invoiceturnover)
    else:
        invoiceturnover = "--"
    return invoiceturnover


def printproject_size(printproject):
    text = str(printproject.width_mm_product) + " x " + str(
        printproject.height_mm_product) + " mm, " + write_orientation_text(printproject.portrait_landscape)
    return text


def printproject_paper(papercategory, paperbrand, paperweight, papercolor):
    printprojectpaper = str(paperbrand) + ", " + str(paperweight) + " g/m2, " + str(papercolor)
    return printprojectpaper


def printproject_printing_booklet(print_booklet, number_pms_colors_booklet, pressvarnish_booklet):
    pms_colors = ""
    pressvarnish = ""

    if number_pms_colors_booklet == 1:
        pms_colors = " en 1 pms kleur"
    if number_pms_colors_booklet > 1:
        pms_colors = " en " + str(number_pms_colors_booklet) + " pms kleuren"
    if pressvarnish_booklet > 0:
        pressvarnish = " en persvernis"

    print_booklet_text = "Geheel in " + write_print_text(print_booklet)
    printprojectprinting_booklet = print_booklet_text + pms_colors + pressvarnish
    return printprojectprinting_booklet


def printproject_printing(printsided, print_front, print_back, number_pms_colors_front, number_pms_colors_back):
    printsided_text = write_sided_text(printsided)
    print_front_text = write_print_text(print_front)
    print_back_text = write_print_text(print_back)
    pms_colors_front = write_print_text(number_pms_colors_front)
    pms_colors_back = write_print_text(number_pms_colors_back)

    printprojectprinting = []
    if printsided in [1, 2]:  # "Eenzijdig" or "Tweezijdig gelijk"
        printprojectprinting = printsided_text + " in " + print_front_text

    if printsided == 3:  # "Tweezijdig verschillend"
        printprojectprinting = ("Voorzijde in " + print_front_text + pms_colors_front + ", achterzijde in "
                                + print_back_text + " " + pms_colors_back)

    return printprojectprinting


def printproject_varnish(printsided, pressvarnish_front, pressvarnish_back, ):
    pressvarnish_front_description = "geen persvernis"
    pressvarnish_back_description = "geen persvernis"

    pressvarnish_description = pressvarnish_front_description

    if pressvarnish_front == 1:
        pressvarnish_front_description = "persvernis"

    if pressvarnish_back == 1:
        pressvarnish_back_description = "persvernis"

    if pressvarnish_front == pressvarnish_back and printsided == 1:
        pressvarnish_description = "Eenzijdig " + pressvarnish_front_description
        if printsided == 2 and pressvarnish_front == 1:
            pressvarnish_description = "Tweeijdig " + pressvarnish_front_description

    if printsided == 3:
        pressvarnish_description = "Voorzijde " + pressvarnish_front_description + " en achterzijde " + pressvarnish_back_description
    return str(pressvarnish_description)


def printproject_enhance(productcategory, enhance_sided, enhance_front, enhance_back):
    enhance_front_text = write_enhance_text(enhance_front)
    enhance_back_text = write_enhance_text(enhance_back)
    enhance_description = 'Geen opgave'

    if productcategory in categories_brochures_all:
        enhance_description = enhance_front_text + " op omslag buitenzijde"

    if productcategory == categories_selfcovers:
        enhance_description = enhance_front_text

    if productcategory in categories_plano:
        enhance_description = "Geen opgave"
        if enhance_sided == 1:  # 'Alleen voorzijde':
            enhance_description = "Alleen op voorzijde " + enhance_front_text + ", achterzijde geen veredeling "
        if enhance_sided == 2:  # 'Tweezijdig gelijk':
            enhance_description = "Tweezijdig " + enhance_front_text
        if enhance_sided == 3:  # 'Alleen achterzijde':
            enhance_description = "Achterzijde " + enhance_back_text + ", voorzijde geen veredeling "
        if enhance_sided == 4:  # 'Tweezijdig verschillend':
            enhance_description = "Voorzijde " + enhance_front_text + "en achterzijde " + enhance_back_text
    return enhance_description


def printproject_packaging(packaging):
    packaging = int(packaging)

    try:
        packaging_description = PackagingOptions.objects.get(packagingoption_id=packaging).packaging
    except PackagingOptions.DoesNotExist:
        packaging_description = "Handzaam in dozen "
    return packaging_description


def printproject_message_extra_work(message_extra_work):
    if message_extra_work:
        message_extra_work_text = message_extra_work
    else:
        message_extra_work_text = "Geen extra werk aangevraagd"
    return message_extra_work_text


def printproject_number_of_pages(printproject):
    productcategory_id = printproject.productcategory_id
    number_of_pages = str(printproject.number_of_pages)
    if productcategory_id == 1:
        pages = "2 pagina's"
    elif productcategory_id == 2:
        pages = number_of_pages + " pagina's"
    elif productcategory_id == 3:
        pages = number_of_pages + " pagina's selfcover."
    elif productcategory_id in categories_brochures_cover:
        pages = number_of_pages + " pagina's binnenwerk in 4 pagina's omslag"
    else:
        pages = number_of_pages
    return pages


def printproject_finishing(printproject):
    productcategory_id = printproject.productcategory_id
    finishing_text = ""
    if productcategory_id in categories_plano_no_folder:
        finishing_text = 'Gesneden tot afgewerkt formaat'
    if productcategory_id in categories_folders:
        finishing_text = write_foldingmethod_text(printproject.folding)
    if productcategory_id in categories_brochures_all:
        finishing_text = write_brochurefinishing_text(printproject.finishing_brochures)

    return finishing_text


def printproject_clientcontact(clientcontact_id):
    if not clientcontact_id:
        clientcontactname = "Geen contactpersoon opgegeven"
    else:
        clientcontactname = ClientContacts.objects.get(clientcontact_id=clientcontact_id).clientcontact

    return clientcontactname


def order_delivery_adress(order):
    delivery_adress = str(order.deliver_company) + ' ' + str(order.deliver_street_number) + ', ' + str(
        order.deliver_postcode) + ' ' + str(order.deliver_city)
    return delivery_adress


def order_delivery_contact(order):
    delivery_contact = str(order.deliver_company) + ', ' + str(order.deliver_contactperson) + ', tel: ' + str(
        order.deliver_tel)
    return delivery_contact


def order_requester(order):
    try:
        user = UserProfile.objects.get(id=order.orderer_id)
        requester = str(user.first_name) + "" + str(user.last_name)
    except Exception as e:
        requester = 'onbekend'

    return requester


def display_country(country_code, language_id):
    try:
        country = DropdownCountries.objects.get(country_code=country_code, language_id=language_id).country
    except DropdownCountries.DoesNotExist:
        country = 'Nederland'
    return country


def display_producercategories(producer_id):
    all_productcategories = ProductCategory.objects.all().values_list(
        'productcategory_id', flat=True)
    producer_product_categories = get_producercategories(producer_id)
    available_producercategories = ""

    for productcategory_id in all_productcategories:
        if productcategory_id in producer_product_categories:
            product_category = ProductCategory.objects.get(productcategory_id=productcategory_id).productcategory
            available_producercategories = available_producercategories + str(product_category) + ", "

    return available_producercategories[:-2] + '.'


# for envelopes
def display_env_category_name(printproject):
    printproject_env_category_name = printproject.env_category_name
    return printproject_env_category_name


def display_env_size_close_cut(printproject):
    printproject_env_size_close_cut = printproject.env_size_close_cut
    return printproject_env_size_close_cut


def display_env_material_color(printproject):
    printproject_env_material_color = printproject.env_material_color
    return printproject_env_material_color


def display_env_window(printproject):
    printproject_env_window = printproject.env_window
    return printproject_env_window
