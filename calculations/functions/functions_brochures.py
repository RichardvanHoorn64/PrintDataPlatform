from calculations.functions.functions_general import *
from materials.models import PaperCatalog
from producers.models import EnhancementTariffs


def paper_available_cover(rfq, producer_id):
    paper_cover = PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand_cover,
                                              papercolor=rfq.papercolor_cover,
                                              paperweight_m2=rfq.paperweight_cover)
    return paper_cover


def paper_available_booklet(rfq, producer_id):
    paper = PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand, papercolor=rfq.papercolor,
                                        paperweight_m2=rfq.paperweight)
    return paper


def single_cover_size_calculation(rfq, producer_id, book_thickness, portrait_landscape):
    overflow_offset_mm = GeneralCalculationSettings.objects.get(producer_id=producer_id).overflow_offset_mm
    if portrait_landscape == 1:  # 'staand':
        single_cover_width = (2 * rfq.width_mm_product) + (2 * overflow_offset_mm) + book_thickness
        single_cover_height = rfq.height_mm_product + (2 * overflow_offset_mm)
    else:
        single_cover_width = rfq.height_mm_product + (2 * overflow_offset_mm) + book_thickness
        single_cover_height = rfq.width_mm_product + (2 * overflow_offset_mm)

    return single_cover_width, single_cover_height


def printerfilter_booklet(printer_id, rfq):
    printerfilter = 'fit'
    printer = Printers.objects.get(printer_id=printer_id)
    number_of_colors_booklet = calculate_number_of_colors_booklet(rfq, printer.varnish_unit)
    printer = Printers.objects.get(printer_id=printer_id)

    if printer.max_number_colors < number_of_colors_booklet:
        printerfilter = 'not fit'

    if rfq.number_pms_colors_booklet > 0 and not printer.pms_offered:
        printerfilter = 'not fit'

    if int(rfq.pressvarnish_booklet) > 0 and not printer.varnish_unit:
        printerfilter = 'not fit'

    return printerfilter


#  calculate number of booklet pages per printer
def pages_per_sheet_booklet_calculation(printer_id, katernheight8_mm, katernwidth8_mm):
    printer = Printers.objects.get(printer_id=printer_id)

    number_of_pages_landscape = int(printer.printsize_width / katernwidth8_mm) * int(
        printer.printsize_height / katernheight8_mm)
    number_of_pages_portrait = int(printer.printsize_width / katernheight8_mm) * int(
        printer.printsize_height / katernwidth8_mm)
    max_number_of_katern8 = int(max(number_of_pages_landscape, number_of_pages_portrait))
    pages_per_sheet_booklet = max_number_of_katern8 * 8

    return pages_per_sheet_booklet


# booklet paperidselector
def paperidselector_booklet(printer_id, pages_per_sheet_booklet, paper_fit_for_rfq, katernheight8_mm,
                            katernwidth8_mm,
                            katernmargin):
    printer = Printers.objects.get(printer_id=printer_id)
    max_image_katern = calculate_max_image_katern(pages_per_sheet_booklet, katernwidth8_mm, katernheight8_mm,
                                                  katernmargin)

    imagewidth = max_image_katern[0]
    imageheight = max_image_katern[1]

    paper_fit_for_printer = calculate_paper_fit_for_printer(paper_fit_for_rfq, printer, imageheight, imagewidth)

    max_paper_fit_for_printer = paper_fit_for_printer[
        (paper_fit_for_printer.units_per_sheet == max(paper_fit_for_printer.units_per_sheet))]
    paper_best_fit = max_paper_fit_for_printer[(max_paper_fit_for_printer.waste == min(paper_fit_for_printer.waste))]

    paperspec_id_booklet = paper_best_fit[
                               (paper_best_fit.price_1000sheets == min(paper_best_fit.price_1000sheets))][:1][
        'paperspec_id'].iloc[0]

    return paperspec_id_booklet


def multiple_of4(number_of_pages):
    return int(math.ceil(number_of_pages / 4)) * 4


def calculate_max_image_katern(max_pages_per_printer, katernwidth8_mm_bruto, katernheight8_mm_bruto, katernmargin):
    if max_pages_per_printer <= 8:
        imagewidth = katernwidth8_mm_bruto
        imageheight = katernheight8_mm_bruto

    elif max_pages_per_printer <= 12:
        imagewidth = (katernwidth8_mm_bruto * 1.5) + katernmargin
        imageheight = katernheight8_mm_bruto + katernmargin

    elif max_pages_per_printer <= 16:
        imagewidth = (katernheight8_mm_bruto * 2) + katernmargin
        imageheight = katernwidth8_mm_bruto + katernmargin

    elif max_pages_per_printer <= 24:
        imagewidth = (katernwidth8_mm_bruto * 2) + katernmargin
        imageheight = (katernheight8_mm_bruto * 1.5) + katernmargin

    elif max_pages_per_printer <= 32:
        imagewidth = (katernwidth8_mm_bruto * 2) + katernmargin
        imageheight = (katernheight8_mm_bruto * 2) + katernmargin

    elif max_pages_per_printer <= 48:
        imagewidth = (katernwidth8_mm_bruto * 2) + katernmargin
        imageheight = (katernheight8_mm_bruto * 3) + katernmargin

    elif max_pages_per_printer <= 64:
        imagewidth = (katernheight8_mm_bruto * 4) + katernmargin
        imageheight = (katernwidth8_mm_bruto * 2) + katernmargin

    elif max_pages_per_printer <= 72:
        imagewidth = (katernwidth8_mm_bruto * 3) + katernmargin
        imageheight = (katernheight8_mm_bruto * 3) + katernmargin

    elif max_pages_per_printer <= 96:
        imagewidth = (katernheight8_mm_bruto * 4) + katernmargin
        imageheight = (katernheight8_mm_bruto * 3) + katernmargin

    elif max_pages_per_printer <= 128:
        imagewidth = (katernwidth8_mm_bruto * 4) + katernmargin
        imageheight = (katernheight8_mm_bruto * 4) + katernmargin

    else:
        imagewidth = 0
        imageheight = 0
    imagewidth = float(imagewidth)
    imageheight = float(imageheight)
    return imagewidth, imageheight


def calculate_number_of_sheets_complete(number_of_pages, pages_per_sheet_booklet):
    number_of_sheets_complete = math.floor(number_of_pages / pages_per_sheet_booklet)
    return number_of_sheets_complete


def calculate_number_of_sheets_incomplete(number_of_pages, pages_per_sheet_booklet):
    number_of_sheets_complete = math.floor(number_of_pages / pages_per_sheet_booklet)
    number_of_rest_pages = number_of_pages - (number_of_sheets_complete * pages_per_sheet_booklet)
    perfector_page_limit = math.ceil(int(pages_per_sheet_booklet / 2))

    number_of_sheets_incomplete = 0.0

    if 0 < number_of_rest_pages <= perfector_page_limit:
        number_of_sheets_incomplete = 1
    if number_of_rest_pages > 0 and number_of_rest_pages > perfector_page_limit:
        number_of_sheets_incomplete = 2
    return number_of_sheets_incomplete


def calculate_pages_per_katern_full(pages_per_sheet_booklet, booklet_foldingfactor):
    pages_per_katern_full = 0
    if booklet_foldingfactor > 0:
        pages_per_katern_full = math.floor(pages_per_sheet_booklet * (1 / booklet_foldingfactor))
    return pages_per_katern_full


def calculate_number_of_katerns_full(pages_per_katern_booklet, booklet_foldingfactor, number_of_pages):
    number_of_katerns_full = 0
    if number_of_pages > 0:
        number_of_katerns_full = int((number_of_pages / pages_per_katern_booklet) * (1 / booklet_foldingfactor))
    return int(number_of_katerns_full)


def calculate_number_of_katerns_half(number_of_pages, number_of_katerns_full, pages_per_katern_full):
    number_of_katerns_half = 0
    number_of_pages_katerns_full = number_of_katerns_full * pages_per_katern_full
    number_of_restpages = number_of_pages - number_of_pages_katerns_full
    if number_of_restpages > 0:
        number_of_katerns_half = math.floor(number_of_restpages / (pages_per_katern_full * 0.5))
    return int(number_of_katerns_half)


def calculate_number_of_katerns_quarter(number_of_pages, number_of_katerns_full, number_of_katerns_half,
                                        pages_per_katern_full):
    number_of_katerns_quarter = 0
    number_of_pages_katerns_full = number_of_katerns_full * pages_per_katern_full
    number_of_pages_katerns_half = number_of_katerns_half * (pages_per_katern_full / 2)

    number_of_restpages = number_of_pages - number_of_pages_katerns_full - number_of_pages_katerns_half
    if number_of_restpages > 0:
        number_of_katerns_quarter = math.floor(number_of_restpages / (pages_per_katern_full * 0.25))
    return int(number_of_katerns_quarter)


def katern_width_calc(rfq, katernmargin, headmargin):
    if rfq.portrait_landscape == 'staand':
        width = int(2 * rfq.width_mm_product) + katernmargin + headmargin
    else:
        width = int(2 * rfq.height_mm_product) + headmargin
    return width


def katern_height_calc(rfq, katernmargin, headmargin):
    if rfq.portrait_landscape == 'staand':
        height = int(2 * rfq.height_mm_product) + katernmargin + headmargin
    else:
        height = int(2 * rfq.width_mm_product) + headmargin

    return height


def filter_foldingmachines_fit_rfq(producer_id, rfq):
    if rfq.portrait_landscape == 1:
        fit_foldingmachines_rfq = pd.DataFrame(Foldingmachines.objects.filter(
            producer_id=producer_id,
            foldingtype_id=1,
            min_weight_paper_katern__lte=rfq.paperweight,
            max_weight_paper_katern__gte=rfq.paperweight,
            vertical_offered=True
        ).values())
    elif rfq.portrait_landscape == 2:
        fit_foldingmachines_rfq = pd.DataFrame(Foldingmachines.objects.filter(
            producer_id=producer_id,
            foldingtype_id=1,
            min_weight_paper_katern__lte=rfq.paperweight,
            max_weight_paper_katern__gte=rfq.paperweight,
            landscape_offered=True
        ).values())
    else:
        fit_foldingmachines_rfq = pd.DataFrame(Foldingmachines.objects.filter(
            producer_id=producer_id,
            foldingtype_id=1,
            min_weight_paper_katern__lte=rfq.paperweight,
            max_weight_paper_katern__gte=rfq.paperweight,
            square_offered=True
        ).values())

    return fit_foldingmachines_rfq


def filter_foldingmachines_booklet(fit_foldingmachines_rfq, katern_width_mm, katern_height_mm,
                                   pages_per_sheet_booklet):
    fit_foldingmachines_booklet = fit_foldingmachines_rfq

    fit_foldingmachines_booklet = fit_foldingmachines_booklet[
        fit_foldingmachines_booklet.max_paperheight_mm >= katern_height_mm]
    fit_foldingmachines_booklet = fit_foldingmachines_booklet[
        fit_foldingmachines_booklet.max_paperwidth_mm >= katern_width_mm]

    fit_foldingmachines_booklet = fit_foldingmachines_booklet[
        fit_foldingmachines_booklet.pages_per_katern >= pages_per_sheet_booklet]

    # select foldingmachine best price
    fit_foldingmachines_booklet['price_per_ex'] = (
            fit_foldingmachines_booklet['tariff_eur_hour'] / fit_foldingmachines_booklet[
        'meter_per_hour'])
    foldingmachine_id = fit_foldingmachines_booklet[
        fit_foldingmachines_booklet.price_per_ex == min(fit_foldingmachines_booklet.price_per_ex)][
        'foldingmachine_id'].iloc[0]
    return foldingmachine_id


def katern_size_calc(rfq, katernmarge, kopmarge):
    if rfq.portrait_landscape == 'staand':
        katern_width_mm = int(2 * rfq.width_mm_product) + katernmarge + kopmarge
        katern_height_mm = int(2 * rfq.height_mm_product) + katernmarge + kopmarge
    else:
        katern_width_mm = int(2 * rfq.height_mm_product) + katernmarge
        katern_height_mm = int(2 * rfq.width_mm_product) + katernmarge
    return katern_width_mm, katern_height_mm


def calculate_booklet_foldingfactor(fit_foldingmachines_rfq, rfq, katernmargin, headmargin,
                                    pages_per_sheet_booklet):
    katern_width_mm, katern_height_mm = katern_size_calc(rfq, katernmargin, headmargin)

    height_mm_2 = katern_width_mm / 2
    width_mm_2 = katern_height_mm
    height_mm_4 = width_mm_2 / 2
    width_mm_4 = height_mm_2
    pages_per_sheet_booklet2 = pages_per_sheet_booklet / 2
    pages_per_sheet_booklet4 = pages_per_sheet_booklet / 4

    foldingfactor = 0
    try:
        foldingmachine_fit_1 = filter_foldingmachines_booklet(fit_foldingmachines_rfq,
                                                              katern_width_mm, katern_height_mm,
                                                              pages_per_sheet_booklet)
        if foldingmachine_fit_1:
            foldingfactor = 1

    except Exception as e:
        print("foldingmachine_fit_1 error: ", e)
        foldingfactor = 0

    if foldingfactor == 0:
        try:
            foldingmachine_fit_2 = filter_foldingmachines_booklet(fit_foldingmachines_rfq,
                                                                  width_mm_2, height_mm_2,
                                                                  pages_per_sheet_booklet2)
            if foldingmachine_fit_2 != 0:
                foldingfactor = 2
        except Exception as e:
            print("foldingmachine_fit_2 error: ", e)
            foldingfactor = 0

    if foldingfactor == 0:
        try:
            foldingmachine_fit_4 = filter_foldingmachines_booklet(fit_foldingmachines_rfq,
                                                                  width_mm_4, height_mm_4,
                                                                  pages_per_sheet_booklet4)
            if foldingmachine_fit_4 != 0:
                foldingfactor = 4
        except Exception as e:
            print("foldingmachine_fit_4 error: ", e)

    return foldingfactor


def define_foldingmachine_id_booklet(fit_foldingmachines_rfq, foldingsheettype, katern_width_mm, katern_height_mm,
                                     pages_per_sheet_booklet, foldingfactor):
    foldingmachine_id = 0
    if foldingfactor > 0:
        if foldingsheettype == 2:
            katern_width_mm = katern_width_mm * (1 / foldingfactor)
        if foldingsheettype == 4:
            katern_width_mm = katern_width_mm * (1 / foldingfactor)
            katern_height_mm = katern_height_mm * (1 / foldingfactor)

        katern_height_mm = katern_height_mm / foldingfactor
        katern_width_mm = katern_width_mm / foldingfactor
        pages_per_sheet_booklet = pages_per_sheet_booklet / foldingsheettype
        foldingmachine_id = filter_foldingmachines_booklet(fit_foldingmachines_rfq,
                                                           katern_width_mm, katern_height_mm,
                                                           pages_per_sheet_booklet)

    return foldingmachine_id


def define_foldingmachine_names_booklet(booklet_foldingfactor, foldingmachine_id, foldingmachine_id_half,
                                        foldingmachine_id_quarter):
    foldingmachine_full_katern = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id).asset_name
    foldingmachine_names_booklet = "full katerns: " + foldingmachine_full_katern

    if booklet_foldingfactor > 1:
        foldingmachine_half_katern = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_half).asset_name
        foldingmachine_names_booklet = foldingmachine_names_booklet + " half katern: " + foldingmachine_half_katern

    if booklet_foldingfactor > 2:
        foldingmachine_quarter_katern = Foldingmachines.objects.get(
            foldingmachine_id=foldingmachine_id_quarter).asset_name
        foldingmachine_names_booklet = (foldingmachine_names_booklet + " quarter katern: "
                                        + foldingmachine_quarter_katern)
    return foldingmachine_names_booklet


def foldingcost_calculation(set_up, rfq, foldingmachine, number_of_katerns, paper_width, paper_height):
    perc_wastefactor = 1.0 + float(foldingmachine.paperwaste_1000sheet_perc / 100)

    volume = 1000

    if set_up:
        volume = rfq.volume

    volume = volume * perc_wastefactor

    setup_time_minutes = 0
    runlength = 0

    if number_of_katerns > 0 and set_up:
        setup_time_minutes = foldingmachine.setup_time_1e_katern_min + (
                (number_of_katerns - 1) * foldingmachine.setup_time_next_katern_min)
        volume = volume * perc_wastefactor

    if foldingmachine.sheet_input == '1':  # drukvel_hoogte
        runlength = (paper_width + foldingmachine.margin_katern_mm) * number_of_katerns * volume

    if foldingmachine.sheet_input == '2':  # drukvel_breedte
        runlength = (paper_height + foldingmachine.margin_katern_mm) * number_of_katerns * volume

    runtime_minutes = (runlength * 0.001) / float(foldingmachine.meter_per_hour)
    foldingcost = (setup_time_minutes + runtime_minutes) * float(foldingmachine.tariff_eur_hour / 60)

    return foldingcost


def calculate_foldingwaste(set_up, foldingmachine, foldingfactor, number_of_katerns, volume):
    paperwaste_1000sheets_perc = float(foldingmachine.paperwaste_1000sheet_perc)
    wastefactor = (1.0 / foldingfactor)
    foldingwaste_start = 0

    if number_of_katerns > 0 and not set_up:
        foldingwaste_start = float(foldingmachine.paperwaste_start) * float(number_of_katerns) * (
                1.0 / foldingfactor)
    foldingwaste_run = float(volume) * paperwaste_1000sheets_perc * .01 * float(
        number_of_katerns) * (wastefactor / foldingfactor)

    foldingwaste = foldingwaste_start + foldingwaste_run
    return foldingwaste


def foldingsheetsize_per_foldingfactor(foldingfactor, paper_width_booklet, paper_height_booklet):
    if foldingfactor == 1:
        paper_width_full = paper_width_booklet
        paper_height_full = paper_height_booklet
        paper_width_half = paper_width_booklet / 2
        paper_height_half = paper_height_booklet
        paper_width_quarter = paper_width_booklet / 2
        paper_height_quarter = paper_height_booklet / 2
    elif foldingfactor == 2:
        paper_width_full = paper_width_booklet / 2
        paper_height_full = paper_height_booklet
        paper_width_half = paper_width_booklet / 2
        paper_height_half = paper_height_booklet / 2
        paper_width_quarter = paper_width_booklet / 4
        paper_height_quarter = paper_height_booklet / 2
    elif foldingfactor == 4:
        paper_width_full = paper_width_booklet / 2
        paper_height_full = paper_height_booklet / 2
        paper_width_half = paper_width_booklet / 4
        paper_height_half = paper_height_booklet / 2
        paper_width_quarter = paper_width_booklet / 4
        paper_height_quarter = paper_height_booklet / 4
    else:
        paper_width_full = 0
        paper_height_full = 0
        paper_width_half = 0
        paper_height_half = 0
        paper_width_quarter = 0
        paper_height_quarter = 0
    return (paper_width_full, paper_height_full, paper_width_half, paper_height_half,
            paper_width_quarter, paper_height_quarter)


# folding calculation


def foldingcost_booklet_calculation(set_up, rfq, foldingfactor, paper_width_booklet, paper_height_booklet,
                                    foldingmachine_id_full, foldingmachine_id_half, foldingmachine_id_quarter,
                                    number_of_katerns_full, number_of_katerns_half, number_of_katerns_quarter):
    foldingcost_full = 0
    foldingcost_half = 0
    foldingcost_quarter = 0

    (paper_width_full, paper_height_full, paper_width_half, paper_height_half, paper_width_quarter,
     paper_height_quarter) = foldingsheetsize_per_foldingfactor(
        foldingfactor, paper_width_booklet, paper_height_booklet)

    if foldingfactor > 0:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_full)
        foldingcost_full = foldingcost_calculation(set_up, rfq, foldingmachine, number_of_katerns_full,
                                                   paper_width_full,
                                                   paper_height_full)

    if foldingfactor > 1:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_half)
        foldingcost_half = foldingcost_calculation(set_up, rfq, foldingmachine, number_of_katerns_half,
                                                   paper_width_half,
                                                   paper_height_half)

    if foldingfactor > 2:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_quarter)
        foldingcost_quarter = foldingcost_calculation(set_up, rfq, foldingmachine, number_of_katerns_quarter,
                                                      paper_width_quarter,
                                                      paper_height_quarter)

    foldingcost = foldingcost_full + foldingcost_half + foldingcost_quarter
    return foldingcost


def foldingwaste_booklet_calculation(set_up, volume, foldingfactor, paper_width_booklet, paper_height_booklet,
                                     foldingmachine_id_full, foldingmachine_id_half, foldingmachine_id_quarter,
                                     number_of_katerns_full, number_of_katerns_half, number_of_katerns_quarter):
    foldingwaste_full = 0.0
    foldingwaste_half = 0.0
    foldingwaste_quarter = 0.0

    if foldingfactor > 0:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_full)
        foldingwaste_full = calculate_foldingwaste(set_up, foldingmachine, foldingfactor, number_of_katerns_full,
                                                   volume)

    if foldingfactor > 1:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_half)
        foldingwaste_half = calculate_foldingwaste(set_up, foldingmachine, foldingfactor, number_of_katerns_half,
                                                   volume)

    if foldingfactor > 2:
        foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id_quarter)
        foldingwaste_quarter = calculate_foldingwaste(set_up, foldingmachine, foldingfactor,
                                                      number_of_katerns_quarter,
                                                      volume)

    foldingwaste = foldingwaste_full + foldingwaste_half + foldingwaste_quarter
    return foldingwaste


def calculate_number_of_rest_pages(number_of_pages, pages_per_sheet_booklet):
    aantal_sheet_compleet = math.floor(number_of_pages / pages_per_sheet_booklet)
    number_of_pages_compleet_productie = aantal_sheet_compleet * pages_per_sheet_booklet
    number_of_rest_pages = number_of_pages - number_of_pages_compleet_productie
    return number_of_rest_pages


def calculate_number_of_printruns_booklet(printer_id, number_of_sheets_complete_booklet,
                                          number_of_sheets_incomplete_booklet, number_of_rest_pages,
                                          pages_per_sheet_booklet):
    perfecting = Printers.objects.get(printer_id=printer_id).perfecting
    extra_printruns = 0

    if number_of_sheets_incomplete_booklet > 0:
        extra_printruns = 1

        if (number_of_rest_pages * 2) >= pages_per_sheet_booklet:
            extra_printruns = 2

    if perfecting:
        number_of_printruns_booklet = number_of_sheets_complete_booklet + number_of_sheets_incomplete_booklet
    else:
        number_of_printruns_booklet = (number_of_sheets_complete_booklet * 2) + extra_printruns

    return number_of_printruns_booklet


def calculate_net_paper_quantity_incomplete_booklet(volume, number_of_rest_pages, number_of_sheets_incomplete_booklet,
                                                    pages_per_sheet_booklet):
    if number_of_sheets_incomplete_booklet == 0:
        printruns_factor = 0
    elif (number_of_rest_pages * 4) <= pages_per_sheet_booklet:
        printruns_factor = 0.25
    elif (number_of_rest_pages * 2) <= pages_per_sheet_booklet:
        printruns_factor = 0.5
    else:
        printruns_factor = 1

    net_paper_quantity_incomplete_booklet = volume * number_of_sheets_incomplete_booklet * printruns_factor
    return net_paper_quantity_incomplete_booklet


def calculate_net_paper_quantity_complete_booklet(volume, number_of_sheets_complete_booklet, ):
    net_paper_quantity_complete_booklet = (volume * number_of_sheets_complete_booklet)
    return net_paper_quantity_complete_booklet


def bindingwaste_booklet_calculation(bindingmachine_id, net_paper_quantity_booklet_total):
    bindingmachine = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id)

    bindingwaste_booklet = float(bindingmachine.paperwaste_perc) * float(net_paper_quantity_booklet_total / 100)
    return bindingwaste_booklet


def bindingwaste_booklet_calculation1000extra(bindingmachine_id, net_paper_quantity_booklet_total, volume):
    bindingmachine = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id)
    paper_quantity1000extra = net_paper_quantity_booklet_total * (1000 / volume)
    bindingwaste_booklet1000extra = float(bindingmachine.paperwaste_perc) * float(paper_quantity1000extra / 100)
    return bindingwaste_booklet1000extra


def printing_booklet_starttime_calculation(printer_id, number_of_printruns_booklet, rfq):
    printer = Printers.objects.get(printer_id=printer_id)
    pressvarnish = float(rfq.pressvarnish_booklet)

    set_uptime_order = printer.starttime_per_order
    # calculate set up time booklet
    if printer.perfecting:
        setup = printer.start_time_sheet_frontside
    else:
        setup = printer.start_time_sheet_frontside + printer.start_time_sheet_backside

    printing_starttime_booklet = (number_of_printruns_booklet * setup) + \
                                 (rfq.number_pms_colors_booklet * printer.start_time_pms_color) + \
                                 (pressvarnish * printer.start_time_varnish) + printer.changetime_perfector
    printing_booklet_starttime = set_uptime_order + printing_starttime_booklet
    return printing_booklet_starttime


def printing_booklet_runtime_calculation(printer_id, paper_quantity_booklet, rfq):
    printer = Printers.objects.get(printer_id=printer_id)
    paperweight_m2 = int(rfq.paperweight)
    basic_runtime = float(paper_quantity_booklet / printer.productionspeed_sheets_hour) * 60

    if printer.perfecting:
        printing_runtime_booklet = basic_runtime * float((100 - printer.perc_speedreduction_perfecting) / 100)
    else:
        printing_runtime_booklet = basic_runtime * 2

    if paperweight_m2 > printer.weight_heavy_paper:
        speedreduction_heavy_paper = float((100 - printer.perc_speedreduction_heavy_paper) / 100)
        printing_runtime_booklet = printing_runtime_booklet * speedreduction_heavy_paper

    if paperweight_m2 < printer.weight_light_paper:
        speedreduction_light_paper = float((100 - printer.perc_speedreduction_light_paper) / 100)
        printing_runtime_booklet = printing_runtime_booklet * speedreduction_light_paper

    return printing_runtime_booklet


def printingwaste_booklet_calculation1000extra(rfq, printer_id, net_paper_quantity_booklet1000extra):
    printer = Printers.objects.get(printer_id=printer_id)
    perfecting_runfactor = 2.0

    if printer.perfecting:
        perfecting_runfactor = 1.0

    waste_printing = float(printer.perc_paperwaste_printing_1000_sheets)
    waste_pms = float(rfq.number_pms_colors_booklet) * float(printer.perc_extra_paperwaste_printing_pms)
    waste_perc = float(waste_printing + waste_pms) * perfecting_runfactor * 0.01
    printingwaste_booklet1000extra = float(net_paper_quantity_booklet1000extra) * waste_perc
    return printingwaste_booklet1000extra


def printingwaste_booklet_calculation(rfq, printer_id, printingwaste_booklet1000extra,
                                      number_of_printruns_booklet):
    printer = Printers.objects.get(printer_id=printer_id)
    waste_fc = 0.0
    waste_black = 0.0
    waste_pms = 0.0
    waste_pressvarnish = 0.0

    paperwaste_per_order = float(printer.paperwaste_per_order)

    if rfq.print_booklet == 1:  # 'Zwart':
        waste_black = float(printer.paperwaste_per_side_black) * 2

    if rfq.print_booklet == 4:  # 'Full Colour':
        waste_fc = float(printer.paperwaste_per_side_fc) * 2

    if int(rfq.pressvarnish_booklet) > 0:
        waste_pressvarnish = float(printer.paperwaste_per_side_varnish) * 2

    if rfq.number_pms_colors_booklet > 0:
        waste_pms = float(rfq.number_pms_colors_booklet * printer.paperwaste_per_side_pms) * 2

    paperwaste_setup = paperwaste_per_order + (waste_fc + waste_black + waste_pms + waste_pressvarnish) * float(
        number_of_printruns_booklet)

    paperwaste_run = float(rfq.volume / 1000) * float(printingwaste_booklet1000extra)
    printingwaste_booklet = paperwaste_setup + paperwaste_run
    return printingwaste_booklet


def define_cuttingmachine_booklet(producer_id, paperspec_id, number_of_sheets_incomplete_booklet, foldingfactor):
    cuttingmachine_id = 0
    if number_of_sheets_incomplete_booklet > 0 or foldingfactor > 0:
        paperbrand = PaperCatalog.objects.get(paperspec_id=paperspec_id)
        sheet_width = paperbrand.paper_width_mm
        sheet_height = paperbrand.paper_height_mm
        cuttingmachines = pd.DataFrame(
            Cuttingmachines.objects.filter(producer_id=producer_id, max_width_mm__gt=sheet_height,
                                           max_depth_mm__gt=sheet_width,
                                           ).values())
        cuttingmachine_id = cuttingmachines[cuttingmachines.tariff_eur_hour == min(cuttingmachines.tariff_eur_hour)][
            'cuttingmachine_id'].iloc[
            0]
    return cuttingmachine_id


def cutting_setuptime_booklet(cuttingmachine_booklet, booklet_foldingfactor, number_of_sheets_incomplete_booklet):
    setup_time = 0.0
    if not cuttingmachine_booklet == 0:
        if booklet_foldingfactor > 1 or number_of_sheets_incomplete_booklet > 1:
            cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_booklet)
            setup_time = float(cuttingmachine.setup_order_min) / 60

    return setup_time


def cutting_runtime_booklet(booklet_foldingfactor, cuttingmachine_id, paperspec_id_booklet,
                            aantal_sheet_compleet_booklet,
                            number_of_sheets_incomplete_booklet, aantal_foldingsheet_half, aantal_foldingsheet_quarter,
                            ):
    paperbrand = PaperCatalog.objects.get(paperspec_id=paperspec_id_booklet)
    cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id)
    max_stackheight_mm = float(cuttingmachine.max_stackheight_mm) * 10
    paperweight_m2 = float(paperbrand.paperweight_m2)
    paper_thickening = float(1)
    runtime_booklet_full = 0
    runtime_booklet_rest = 0

    if paperbrand.paper_thickening:
        paper_thickening = float(paperbrand.paper_thickening)

    if booklet_foldingfactor > 1:
        stackheight_mm_booklet_full = aantal_sheet_compleet_booklet * paperweight_m2 * paper_thickening * 0.001
        number_of_stacks_booklet_full = math.ceil(stackheight_mm_booklet_full / max_stackheight_mm)
        number_of_cuts_booklet_full = booklet_foldingfactor / 2
        runtime_booklet_full = (
                number_of_cuts_booklet_full * float(cuttingmachine.time_per_extra_sec) * number_of_stacks_booklet_full)

    if number_of_sheets_incomplete_booklet > 1:
        number_of_cuts_half = aantal_foldingsheet_half * booklet_foldingfactor
        number_of_cuts_quarter = aantal_foldingsheet_quarter * booklet_foldingfactor * 2
        max_stackheight_mm_mm_restsheet = (number_of_sheets_incomplete_booklet
                                           * paperweight_m2 * paper_thickening * 0.001)
        number_of_stacks_rest = math.ceil(max_stackheight_mm_mm_restsheet / max_stackheight_mm)
        number_of_cuts_rest = max(number_of_cuts_half, number_of_cuts_quarter)
        runtime_booklet_rest = (number_of_cuts_rest * cuttingmachine.time_per_extra_sec * number_of_stacks_rest)

    runtime_cutting_booklet = float(runtime_booklet_full + runtime_booklet_rest) / 3600

    return runtime_cutting_booklet


def cuttingcost_booklet_calculation(cuttingmachine_id, setup_time, runtime_cutting_booklet):
    cuttingcost_booklet = 0
    if cuttingmachine_id != 0:
        cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id)
        cutting_time = setup_time + runtime_cutting_booklet
        cuttingcost_booklet = float(cutting_time) * float(cuttingmachine.tariff_eur_hour)

    return cuttingcost_booklet


def cuttingcost_booklet_calculation1000extra(volume, cuttingmachine_id, runtime_cutting_booklet):
    cuttingcost_booklet1000extra = 0.0

    if cuttingmachine_id != 0:
        cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id)
        cutting_time = runtime_cutting_booklet * float(1000 / volume)
        cuttingcost_booklet1000extra = float(cutting_time) * float(cuttingmachine.tariff_eur_hour)

    return cuttingcost_booklet1000extra


def define_bindingmachine_id(selfcover, producer_id, rfq, finishingmethod_id, number_of_katerns_full,
                             number_of_katerns_half, number_of_katerns_quarter):
    number_of_stations = number_of_katerns_full + number_of_katerns_half + number_of_katerns_quarter
    bindingmachines_producer = pd.DataFrame(
        Bindingmachines.objects.filter(producer_id=producer_id, finishingmethod=finishingmethod_id).values())
    width = rfq.width_mm_product + 3
    height = rfq.height_mm_product + 6

    bindingmachines_producer = bindingmachines_producer[
        bindingmachines_producer.max_number_stations_max >= number_of_stations]
    bindingmachines_producer = bindingmachines_producer[(bindingmachines_producer.max_width_untrimmed_mm >= width) & (
            bindingmachines_producer.min_width_untrimmed_mm <= width) & (
                                                                bindingmachines_producer.max_height_untrimmed_mm >= height) & (
                                                                bindingmachines_producer.min_height_untrimmed_mm <= height)]

    if not selfcover:
        bindingmachines_producer = bindingmachines_producer[bindingmachines_producer.cover_feeder == True]

    bindingmachine_id = \
        bindingmachines_producer[
            bindingmachines_producer.tariff_eur_hour == min(bindingmachines_producer.tariff_eur_hour)][
            'bindingmachine_id'].iloc[0]
    return bindingmachine_id


def bindingcost_setup_calculation(bindingmachine_id, number_of_katerns_total, portrait_landscape, selfcover):
    bindingmachine = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id)
    set_up_stations_orientation = 0.0
    set_up_order = float(bindingmachine.setup_order_min)
    set_up_cover = 0

    if not selfcover:
        set_up_cover = float(bindingmachine.setup_time_cover_min)

    number_of_stations_extra = float(number_of_katerns_total - bindingmachine.max_number_stations_default)
    if number_of_stations_extra <= 0:
        number_of_stations_extra = 0.0
    set_up_extra_stations = float(number_of_stations_extra * bindingmachine.setup_time_station_min)

    if portrait_landscape == 2:
        set_up_stations_orientation = float(bindingmachine.setup_landscape)
    if portrait_landscape == 3:
        set_up_stations_orientation = float(bindingmachine.setup_square)

    binding_setup_time = set_up_order + set_up_cover + set_up_extra_stations + set_up_stations_orientation

    bindingcost_setup = float(binding_setup_time / 60) * float(bindingmachine.tariff_eur_hour)
    return bindingcost_setup


def bindingcost_run_calculation(volume, portrait_landscape, number_of_katerns_total, bindingmachine_id):
    bindingmachine = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id)
    speedreduction_portrait_landscape = 1.0
    wastefactor = 1.0 - float(bindingmachine.paperwaste_perc / 100)

    # drumpelwaarde aanmaken
    speedreduction_extra_station = bindingmachine.speedreduction_extra_station
    aantal_stations_extra = float(number_of_katerns_total - bindingmachine.max_number_stations_default)
    if aantal_stations_extra <= 0:
        speedreduction_stations_extra = 1.0
    else:
        speedreduction = 1.0 - (speedreduction_extra_station * 0.01)
        speedreduction_stations_extra = speedreduction ** aantal_stations_extra

    if portrait_landscape == 'liggend':
        speedreduction_portrait_landscape = (100.0 - float(bindingmachine.speedreduction_landscape)) * 0.01
    if portrait_landscape == 'vierkant':
        speedreduction_portrait_landscape = (100.0 - float(bindingmachine.speedreduction_square)) * 0.01

    speed_hour = float(
        bindingmachine.max_speed_hour) * speedreduction_portrait_landscape * wastefactor * speedreduction_stations_extra
    bindingcost_run = (float(bindingmachine.tariff_eur_hour) / speed_hour) * float(volume)
    return bindingcost_run


def bindingcost_calculation(bindingcost_setup, bindingcost_run):
    return bindingcost_setup + bindingcost_run


def binding_waste_calculation(bindingmachine_id_input, aantal_drukvel):
    bindingmachine = Bindingmachines.objects.get(id=bindingmachine_id_input)
    binding_waste = float(bindingmachine.waste_perc) * float(aantal_drukvel / 100)
    return binding_waste


def binding_waste_calculation1000extra(bindingmachine_id_input, aantal_drukvel1000extra):
    bindingmachine = Bindingmachines.objects.get(id=bindingmachine_id_input)
    binding_waste1000extra = float(bindingmachine.waste_perc) * float(aantal_drukvel1000extra / 100)
    return binding_waste1000extra


def orderweight_kg_brochures_calculation(set_up, selfcover, rfq, number_of_pages):
    orderweight_kg_cover = float(0.0)

    if set_up:
        volume = rfq.volume
    else:
        volume = 1000

    pagefactor = float(rfq.height_mm_product) * float(rfq.width_mm_product) * float(0.0001)

    if not selfcover:
        orderweight_kg_cover = float(volume) * float(rfq.paperweight_cover) * pagefactor * float(0.00002)

    orderweight_kg_booklet = float(volume) * float(rfq.paperweight) * pagefactor * float(number_of_pages / 2) * float(
        0.00001)

    orderweight_kg_brochures = orderweight_kg_booklet + orderweight_kg_cover
    return orderweight_kg_brochures


def inkcost_booklet_calculation(setup, rfq, pers_id, paper_quantity_booklet):
    printer = Printers.objects.get(printer_id=pers_id)
    paper_quantity_booklet = float(paper_quantity_booklet / 1000)
    inkcost_print = float(0)
    pms_inkcost_booklet = 0

    if rfq.number_pms_colors_booklet > 0:
        pms_inkcost = float(paper_quantity_booklet * float(printer.ink_1000_prints_pms))
        pms_inkcost_booklet = float(rfq.number_pms_colors_front) * float(pms_inkcost) * 2.0

        if setup:
            if pms_inkcost_booklet < float(printer.ink_start_costs_pms):
                pms_inkcost_booklet = printer.ink_start_costs_pms

    if rfq.print_booklet == 1:  # 'Zwart':
        inkcost_print = paper_quantity_booklet * float(printer.ink_1000_prints_zw) * 2
    if rfq.print_booklet == 4:  # 'Full Colour':
        inkcost_print = paper_quantity_booklet * float(printer.ink_1000_prints_fc) * 2

    inkcost_varnish = float(paper_quantity_booklet) * float(printer.ink_1000_prints_varnish) * int(
        rfq.pressvarnish_booklet) * 2

    inkcost_booklet = inkcost_print + inkcost_varnish + pms_inkcost_booklet
    return inkcost_booklet


def added_value_brochure_calculation(selfcover, producer_id, total_cost, papercost_booklet, papercost_cover,
                                     foldingmachine_id,
                                     foldingcost_booklet, bindingmachine_id, bindingcost, inkcost_booklet,
                                     inkcost_cover, purchase_plates_booklet, purchase_plates_cover, rfq,
                                     paperspec_id, enhancementcost_cover):
    folding_purchase = 0.0
    binding_purchase = 0.0
    enhance_cover_added_value = True

    added_value_foldingmachine = Foldingmachines.objects.get(producer_id=producer_id,
                                                             foldingmachine_id=foldingmachine_id).added_value
    added_value_bindingmachine = Bindingmachines.objects.get(producer_id=producer_id,
                                                             bindingmachine_id=bindingmachine_id).added_value

    if not added_value_foldingmachine:
        folding_purchase = foldingcost_booklet

    if not added_value_bindingmachine:
        binding_purchase = bindingcost

    purchase = papercost_booklet + inkcost_booklet + purchase_plates_booklet + folding_purchase + binding_purchase

    if not selfcover:
        purchase = purchase + papercost_cover + inkcost_cover + purchase_plates_cover

        try:
            enhancement_id = EnhancementOptions.objects.get(enhancement=rfq.enhance_front).enhancement_id
        except EnhancementOptions.DoesNotExist:
            enhancement_id = []

        if enhancement_id:
            paperspec = PaperCatalog.objects.get(paperspec_id=paperspec_id)
            enhancement_id = EnhancementOptions.objects.get(enhancement=rfq.enhance_front).enhancement_id
            enhancement_tariffs = pd.DataFrame(
                EnhancementTariffs.objects.filter(producer_id=producer_id, availeble=True,
                                                  max_sheet_width__lte=paperspec.paper_width_mm,
                                                  max_sheet_height__lte=paperspec.paper_height_mm,
                                                  enhancement_id=enhancement_id).values())

            min_tariff = min(enhancement_tariffs.production_cost_1000sheets)
            enhance_cover_added_value = \
                enhancement_tariffs[enhancement_tariffs.production_cost_1000sheets == min_tariff].iloc[0].added_value

        if not enhance_cover_added_value:
            purchase = purchase + enhancementcost_cover

    brochure_added_value = total_cost - purchase
    return brochure_added_value


def calculate_number_of_colors_booklet(rfq, varnish_unit):
    number_of_colors_booklet = 0
    if rfq.print_booklet == 1:  # 'black':
        number_of_colors_booklet = 1
    if rfq.print_booklet == 4:  # 'Full Colour':
        number_of_colors_booklet = 4
    number_of_colors = number_of_colors_booklet + rfq.number_pms_colors_booklet
    if not varnish_unit and rfq.pressvarnish_front == 1:
        number_of_colors_booklet = number_of_colors + 1
    return number_of_colors_booklet


def purchase_plates_booklet_calculation(printer_id, number_of_printruns_booklet, rfq):
    printer = Printers.objects.get(printer_id=printer_id)
    number_of_colors = calculate_number_of_colors_booklet(rfq, printer.varnish_unit)

    purchase_plates = float(number_of_colors) * float(
        number_of_printruns_booklet) * float(printer.buy_tariff_plate_eur)

    if printer.perfecting:
        purchase_plates_booklet = purchase_plates * 2
    else:
        purchase_plates_booklet = purchase_plates

    return purchase_plates_booklet


def margin_plates_booklet_calculation(printer_id, number_of_printruns_booklet, rfq):
    printer = Printers.objects.get(printer_id=printer_id)
    number_of_colors = calculate_number_of_colors_booklet(rfq, printer.varnish_unit)

    margin_plate_calculation = float(number_of_colors) * float(
        number_of_printruns_booklet) * float(printer.margin_plate_eur)

    if printer.perfecting:
        margin_plates_booklet = margin_plate_calculation * 2
    else:
        margin_plates_booklet = margin_plate_calculation

    return margin_plates_booklet


def calc_book_thickness(selfcover, rfq, producer_id):
    thickness_cover = 0

    paper_thickness_booklet = \
        PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand, papercolor=rfq.papercolor,
                                    paperweight_m2=rfq.paperweight).values()[0].get('paper_thickening')
    thickness_booklet = float(rfq.paperweight) * float(0.001) * float(paper_thickness_booklet) * float(
        rfq.number_of_pages / 2)

    if not selfcover:
        paper_thickness_cover = \
            PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand_cover,
                                        papercolor=rfq.papercolor_cover,
                                        paperweight_m2=rfq.paperweight_cover).values()[0].get('paper_thickening')
        thickness_cover = float(rfq.paperweight_cover) * float(0.001) * float(paper_thickness_cover) * float(2.0)

    thickness = thickness_booklet + thickness_cover
    if thickness < 1:
        thickness = 1
    return thickness


def bindingwaste_cover_calculation(set_up, rfq, bindingmachine_id, items_per_sheet_cover):
    volume = 1000
    if set_up:
        volume = rfq.volume

    waste_perc = Bindingmachines.objects.get(bindingmachine_id=bindingmachine_id).paperwaste_perc
    bindingwaste_cover = float(volume / items_per_sheet_cover) * float(waste_perc) * 0.01

    return bindingwaste_cover
