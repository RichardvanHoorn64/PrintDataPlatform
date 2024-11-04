from printprojects.models import PrintProjects
from index.forms.form_fieldtypes import *


class PrintProjectsForm(forms.ModelForm):
    client_id = integer_field_notreq
    clientcontact_id = integer_field_notreq
    project_title = char_field_1000_false
    description = char_field_1000_false
    message_extra_work = char_field_1000_false
    own_quotenumber = char_field_100_false
    client_quotenumber = char_field_100_false
    volume = integer_field_notreq
    format_selection = char_field_200_false
    standard_size = char_field_200_false
    height_mm_product = integer_field_notreq
    width_mm_product = integer_field_notreq
    papercategory = char_field_200_false
    paperbrand = char_field_200_false
    paperweight = char_field_100_false
    papercolor = char_field_200_false
    printsided = char_field_100_false

    print_front = char_field_100_false
    print_back = char_field_100_false
    print_booklet = char_field_100_false

    number_pms_colors_front = integer_field_notreq
    number_pms_colors_back = integer_field_notreq
    number_pms_colors_booklet = integer_field_notreq

    pressvarnish_front = char_field_100_false
    pressvarnish_back = char_field_100_false
    pressvarnish_booklet = char_field_100_false

    enhance_sided = char_field_100_false
    enhance_front = char_field_100_false
    enhance_back = char_field_100_false

    packaging = char_field_100_false
    number_of_pages = integer_field_notreq
    portrait_landscape = char_field_100_false
    finishing_brochures = char_field_100_false
    paperbrand_new = char_field_100_false
    paperweight_new = char_field_100_false
    papercolor_new = char_field_100_false

    brochure_type = char_field_100_false

    # folders
    folding = char_field_200_false

    # paper cover
    papercategory_cover = char_field_200_false
    paperbrand_cover = char_field_200_false
    paperweight_cover = char_field_100_false
    papercolor_cover = char_field_200_false

    paperbrand_cover_new = char_field_200_false
    paperweight_cover_new = char_field_100_false
    papercolor_cover_new = char_field_200_false

    supply_date = date_field
    delivery_date = date_field

    class Meta:
        model = PrintProjects
        fields = (
            'client_id', 'clientcontact_id', 'project_title', 'description', 'message_extra_work',
            'own_quotenumber', 'client_quotenumber', 'volume', 'format_selection', 'standard_size',
            'height_mm_product', 'width_mm_product', 'papercategory', 'paperbrand', 'paperweight', 'papercolor',
            'printsided', 'print_front', 'print_back', 'print_booklet','number_pms_colors_front', 'number_pms_colors_back',
            'number_pms_colors_booklet', 'pressvarnish_front', 'pressvarnish_back', 'pressvarnish_booklet', 'enhance_sided', 'enhance_front', 'enhance_back',
            'packaging', 'number_of_pages', 'portrait_landscape', 'finishing_brochures', 'paperbrand_new', 'paperweight_new', 'papercolor_new',
            'brochure_type', 'papercategory_cover', 'paperbrand_cover', 'paperweight_cover', 'papercolor_cover', 'paperbrand_cover_new',
            'paperweight_cover_new', 'papercolor_cover_new', 'folding', 'paperweight_cover', 'papercolor_cover',
            'supply_date', 'delivery_date')
