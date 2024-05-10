from index.convert_functions import *


def printproject_description(productcategory, volume, project_title):
    printprojectdescription = str(volume) + " ex. " + productcategory + " " + project_title
    return printprojectdescription


def printproject_size(width_mm_product, height_mm_product, portrait_landscape):
    printprojectsize = str(width_mm_product) + " x " + str(height_mm_product) + "mm, " + write_orientation_text(portrait_landscape)
    return printprojectsize


def printproject_paper(papercategory, paperbrand, paperweight, papercolor, ):
    printprojectpaper = str(papercategory) + " " + str(paperbrand) + " " + str(paperweight) + " " + str(papercolor)
    return printprojectpaper


def printproject_printing(printsided, print_front, print_rear, number_pms_colors, number_pms_colors_rear):
    if number_pms_colors == 0:
        pms_colors = ""
    elif number_pms_colors == 1:
        pms_colors = " en " + str(number_pms_colors) + " pms kleur"
    else:
        pms_colors = " en " + str(number_pms_colors) + " pms kleuren"

    if number_pms_colors_rear == 0:
        pms_colors_rear = ""
    elif number_pms_colors_rear == 1:
        pms_colors_rear = " en " + str(number_pms_colors_rear) + " pms kleur"
    else:
        pms_colors_rear = " en " + str(number_pms_colors_rear) + " pms kleuren"

    if printsided == "Tweezijdig verschillend":
        printprojectprinting = "Voorzijde in " + print_front + pms_colors + ", achterzijde in " + print_rear + " " + pms_colors_rear
    else:
        printprojectprinting = printsided + " in " + print_front + pms_colors
    return printprojectprinting


def printproject_varnish(printsided, pressvarnish, pressvarnish_rear):
    if pressvarnish == pressvarnish_rear:
        printproject_varnish_text = pressvarnish
    elif pressvarnish != pressvarnish_rear and printsided == "Tweezijdig verschillend":
        printproject_varnish_text = "Voorzijde " + pressvarnish + " en achterzijde " + pressvarnish_rear

    else:
        printproject_varnish_text = pressvarnish
    return printproject_varnish_text


def printproject_enhance(productcategory, enhance_sided, enhance, enhance_rear):
    if productcategory in [4, 5]:
        if enhance == 'Geen veredeling':
            enhance_description = "Geen"
        else:
            enhance_description = enhance + " op omslag buitenzijde"
    elif productcategory == 3:
        if enhance == 'Geen veredeling':
            enhance_description = "Geen"
        else:
            enhance_description = enhance
    else:
        if enhance_sided == 'Geen veredeling':
            enhance_description = "Geen"
        elif enhance_sided == 'Tweezijdig gelijk':
            enhance_description = "Tweezijdig " + enhance
        elif enhance_sided == 'Tweezijdig verschillend':
            enhance_description = "Voorzijde " + enhance + "en achterzijde " + enhance_rear
        elif enhance_sided == 'Alleen voorzijde':
            enhance_description = "Voorzijde " + enhance + ", achterzijde geen veredeling "
        elif enhance_sided == 'Alleen achterzijde':
            enhance_description = "Achterzijde " + enhance_rear + ", voorzijde geen veredeling "
        else:
            enhance_description = "Geen opgave"

    return enhance_description


def printproject_finishing(productcategory, number_of_pages, finishing_brochures, folding):
    if productcategory == 2:
        finisching = str(number_of_pages) + " pagina's, " + folding
    elif productcategory == 3:
        finisching = finishing_brochures + " gebrocheerd, " + str(number_of_pages) + " pagina's selfcover"
    elif productcategory in [4, 5]:
        finisching = finishing_brochures + ", " + str(number_of_pages) + " pagina's binnenwerk in 4 pagina's omslag"
    else:
        finisching = finishing_brochures
    return finisching

