from methods.models import *


def find_host(self):
    host = self.request.META["HTTP_HOST"]
    return host


def write_print_text(print_input):
    print_text = ''
    if print_input == 1:
        print_text = "zwart"
    if print_input == 4:
        print_text = "full colour"
    return print_text


def write_sided_text(sided_input):
    printsided_text = ''
    if sided_input == 1:
        printsided_text = "Eenzijdig"
    if sided_input == 2:
        printsided_text = "Tweezijdig gelijk"
    if sided_input == 3:
        printsided_text = "Tweezijdig verschillend"
    return printsided_text


def write_pms_text(number_pms_colors):
    pms_text = ""
    if number_pms_colors == 1:
        pms_text = " en " + str(number_pms_colors) + " pms kleur"
    if number_pms_colors > 1:
        pms_text = " en " + str(number_pms_colors) + " pms kleuren"

    return pms_text


def write_enhance_text(enhance_input):
    try:
        enhance_text = EnhancementOptions.objects.get(enhancement_id=enhance_input).enhancement
    except EnhancementOptions.DoesNotExist:
        enhance_text = 'Geen veredeling'

    return enhance_text


def write_foldingmethod_text(folding_input):
    try:
        foldingmethod_text = FoldingMethods.objects.get(foldingmethod_id=folding_input).foldingmethod
    except FoldingMethods.DoesNotExist:
        foldingmethod_text = ''

    return foldingmethod_text


def write_brochurefinishing_text(finishing_input):
    try:
        brochurefinishing_text = BrochureFinishingMethods.objects.get(
            finishingmethod_id=finishing_input).finishingmethod
    except BrochureFinishingMethods.DoesNotExist:
        brochurefinishing_text = ''

    return brochurefinishing_text


def write_orientation_text(orientation_input):
    orientation_text = ""
    if orientation_input == 1:
        orientation_text = " staand"
    if orientation_input == 2:
        orientation_text = " liggend"
    if orientation_input == 3:
        orientation_text = " vierkant"
    return orientation_text
