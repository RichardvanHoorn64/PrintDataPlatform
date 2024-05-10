import math
from math import floor
import numpy as np
import pandas as pd
from assets.models import *
from materials.models import *
from printprojects.models import MemberProducerMatch, MemberProducerSalesAllowance
from producers.models import *


def productsize_check(rfq):
    if not rfq.height_mm_product or not rfq.width_mm_product:
        error = 'No productsize defined.'
        return error

def paper_available_plano(rfq, producer_id):
    paper = PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand,
                                        papercolor=rfq.papercolor,
                                        paperweight_m2=rfq.paperweight)
    return paper


def paper_cover_available(rfq, producer_id):
    paper = PaperCatalog.objects.filter(producer_id=producer_id, paperbrand=rfq.paperbrand_cover,
                                        papercolor=rfq.papercolor_cover,
                                        paperweight_m2=rfq.paperweight_cover)
    return paper


def paperidselector(printer_id, paper_fit_for_rfq, single_item_height, single_item_width):
    printer = Printers.objects.get(printer_id=printer_id)

    paper_fit_for_printer = calculate_paper_fit_for_printer(paper_fit_for_rfq, printer, single_item_height,
                                                            single_item_width)

    max_paper_fit_for_printer = paper_fit_for_printer[
        (paper_fit_for_printer.units_per_sheet == max(paper_fit_for_printer.units_per_sheet))]
    paper_best_fit = max_paper_fit_for_printer[(max_paper_fit_for_printer.waste == min(paper_fit_for_printer.waste))]

    paperspec_id = paper_best_fit[(paper_best_fit.price_1000sheets == min(paper_best_fit.price_1000sheets))][:1][
        'paperspec_id'].iloc[0]

    return paperspec_id


def calculate_paper_fit_for_printer(paper_fit_for_rfq, printer, unitheight_mm, unitwidth_mm):
    paper_fit_for_printer = pd.DataFrame(paper_fit_for_rfq.values())
    paper_fit_for_printer = paper_fit_for_printer[(paper_fit_for_printer.paper_width_mm <= printer.printsize_width)
                                                  & (paper_fit_for_printer.paper_height_mm <= printer.printsize_height)
                                                  & (paper_fit_for_printer.paper_width_mm >= unitwidth_mm)
                                                  & (paper_fit_for_printer.paper_height_mm >= unitheight_mm)
                                                  ]

    paper_fit_for_printer['number_landscape'] = (paper_fit_for_printer.paper_width_mm / unitheight_mm).apply(
        np.floor) * (paper_fit_for_printer.paper_height_mm / unitwidth_mm).apply(np.floor)
    paper_fit_for_printer['number_portrait'] = (paper_fit_for_printer.paper_width_mm / unitheight_mm).apply(
        np.floor) * (paper_fit_for_printer.paper_height_mm / unitwidth_mm).apply(np.floor)
    paper_fit_for_printer['units_per_sheet'] = paper_fit_for_printer.apply(
        lambda row: max(row['number_landscape'], row['number_portrait']), axis=1)
    paper_fit_for_printer['product_surface'] = paper_fit_for_printer[
                                                   'units_per_sheet'] * paper_fit_for_printer.paper_height_mm * paper_fit_for_printer.paper_width_mm
    paper_fit_for_printer['waste'] = paper_fit_for_printer['paper_surface'] - paper_fit_for_printer['product_surface']

    return paper_fit_for_printer


def net_paper_quantity_calculation(volume, items_per_sheet_cover):
    net_paper_quantity = int(volume / items_per_sheet_cover)
    return net_paper_quantity


def clientrelated_sales_allowance_calculation(rfq, producer_id, perc_added_value, total_cost):
    sales_allowance = 0.00
    try:
        match = MemberProducerSalesAllowance.objects.get(producer_id=producer_id, member_id=rfq.member_id,
                                                         productcategory_id=rfq.productcategory_id)
        perc_salesallowance = float(match.perc_salesallowance)
        sales_allowance = total_cost * perc_salesallowance * perc_added_value * 0.01
    except MemberProducerSalesAllowance.DoesNotExist:
        pass
    return sales_allowance


def calculate_order_startcost(producer_id):
    order_startcost = GeneralCalculationSettings.objects.get(producer_id=producer_id).order_startcost
    return float(order_startcost)


def perc_added_value_calculation(total_cost, added_value):
    perc_tw = added_value / total_cost

    return perc_tw * 100


def paper_added_value_calculation(purchase_paper_perc_added, papercost_booklet):
    paper_added_value = papercost_booklet * float(0.01) * float(purchase_paper_perc_added)
    return paper_added_value


def orderweight_kg_plano_calculation(set_up, rfq, planoproduct_height_mm, planoproduct_width_mm, paperspec_id):
    paper = PaperCatalog.objects.get(paperspec_id=paperspec_id)
    volume = 1000

    if set_up:
        volume = rfq.volume

    orderweight_kg_plano = float(volume) * float(planoproduct_height_mm * .001) * float(
        planoproduct_width_mm * .001) * float(paper.paperweight_m2 * .001)

    return orderweight_kg_plano


def calculate_number_of_colors_front(rfq, varnish_unit):
    number_of_colors_front = 0
    if rfq.print_front == 1:  # 'black':
        number_of_colors_front = 1
    if rfq.print_front == 4:  # 'Full Colour':
        number_of_colors_front = 4
    number_of_colors = number_of_colors_front + rfq.number_pms_colors_front
    if not varnish_unit and rfq.pressvarnish_front == 1:
        number_of_colors_front = number_of_colors + 1
    return number_of_colors_front


def calculate_number_of_colors_rear(rfq, varnish_unit):
    number_of_colors_rear = 0
    if rfq.print_rear == 1:  # 'black':
        number_of_colors_rear = 1
    if rfq.print_rear == 4:  # 'Full Colour':
        number_of_colors_rear = 4
    number_of_colors = number_of_colors_rear + rfq.number_pms_colors_rear
    if not varnish_unit and rfq.pressvarnish_rear == 1:
        number_of_colors_rear = number_of_colors + 1
    return number_of_colors_rear


# Functies voor beeldmaten aanvraag
def height_mm_calc(printed_overflow, height_mm, producer_id):
    if printed_overflow:
        overflow_offset_mm = GeneralCalculationSettings.objects.get(producer_id=producer_id).overflow_offset_mm
        height_mm = height_mm + (2 * overflow_offset_mm)
    else:
        height_mm = height_mm
    return height_mm


def width_mm_calc(printed_overflow, width_mm, producer_id):
    if printed_overflow:
        overflow_offset_mm = GeneralCalculationSettings.objects.get(producer_id=producer_id).overflow_offset_mm
        width_mm = width_mm + (2 * overflow_offset_mm)
    else:
        width_mm = width_mm
    return width_mm


def inkcost_calculation(setup, rfq, printer_id, paper_quantity, printsided):
    printer = Printers.objects.get(printer_id=printer_id)
    paper_quantity = float(paper_quantity / 1000)
    black_inkcost_front = float(0.0)
    black_inkcost_rear = float(0.0)
    fc_inkcost_front = float(0.0)
    fc_inkcost_rear = float(0.0)
    pms_inkcost = float(0.0)
    pressvarnish_inkcost_front = float(0.0)
    pressvarnish_inkcost_rear = float(0.0)
    inkcost = 0.0

    if rfq.number_pms_colors_front > 0 or rfq.number_pms_colors_rear > 0:
        pms_inkcost = float(paper_quantity * float(printer.ink_1000_prints_pms))
        pms_inkcost_front = float(rfq.number_pms_colors_front) * float(pms_inkcost)
        pms_inkcost_rear = float(rfq.number_pms_colors_rear) * float(pms_inkcost)
        pms_inkcost = pms_inkcost_front + pms_inkcost_rear

        if printsided == 2:  # 'Tweezijdig gelijk':
            pms_inkcost = 2 * pms_inkcost_front

        if setup:
            if pms_inkcost < float(printer.ink_start_costs_pms):
                pms_inkcost = printer.ink_start_costs_pms

    if rfq.number_pms_colors_front > 0 or rfq.number_pms_colors_rear > 0:
        pressvarnish_inkcost = paper_quantity * float(printer.ink_1000_prints_varnish)
        pressvarnish_inkcost_front = float(rfq.pressvarnish_front) * float(pressvarnish_inkcost)
        pressvarnish_inkcost_rear = float(rfq.pressvarnish_rear) * pressvarnish_inkcost

    if rfq.print_front == 1:  # 'black':
        black_inkcost_front = paper_quantity * float(printer.ink_1000_prints_zw)
    if rfq.print_front == 4:  # 'Full Colour':
        fc_inkcost_front = paper_quantity * float(printer.ink_1000_prints_fc)

    inkcost_front = float(black_inkcost_front) + float(fc_inkcost_front) + pressvarnish_inkcost_front

    if printsided == 2:  # 'Tweezijdig gelijk':
        inkcost = 2 * inkcost_front

    if printsided == 3:  # 'Tweezijdig verschillend':
        if rfq.print_rear == 1:  # 'black':
            black_inkcost_rear = paper_quantity * float(printer.ink_1000_prints_zw)
        if rfq.print_rear == 4:  # 'Full Colour':
            fc_inkcost_rear = paper_quantity * float(printer.ink_1000_prints_fc)

        inkcost_rear = float(black_inkcost_rear) + float(fc_inkcost_rear) + pressvarnish_inkcost_rear
        inkcost = inkcost_front + inkcost_rear + pms_inkcost

    return inkcost


def items_per_sheet_calculation(paperspec_id, height_mm_gross, width_mm_gross):
    sheet = pd.DataFrame(PaperCatalog.objects.filter(paperspec_id=paperspec_id).values())
    number_of_sheets_portrait = floor(sheet.paper_width_mm.iloc[0] / width_mm_gross) * floor(
        sheet.paper_height_mm.iloc[0] / height_mm_gross)
    number_of_sheets_landscape = floor(sheet.paper_width_mm.iloc[0] / height_mm_gross) * floor(
        sheet.paper_height_mm.iloc[0] / width_mm_gross)
    items_per_sheet = max(number_of_sheets_landscape, number_of_sheets_portrait)
    return items_per_sheet


def number_of_printruns_calculation(printsided, printer_id):
    perfecting = Printers.objects.get(printer_id=printer_id).perfecting
    number_of_printruns = 2
    if printsided == 1:  # 'Eenzijdig':
        number_of_printruns = 1

    if printsided == 3:  # 'Tweezijdig verschillend' and perfecting:
        number_of_printruns = 1

    if printsided == 2:  # 'Tweezijdig gelijk' and perfecting:
        number_of_printruns = 1

    return int(number_of_printruns)


def printing_starttime_calculation(rfq, printer_id, items_per_sheet):
    printer = Printers.objects.get(printer_id=printer_id)
    start_time_varnish = printer.start_time_varnish
    use_perfecting = False

    if printer.perfecting:
        start_time_varnish = 0.0

    if items_per_sheet % 2 == 0:
        use_perfecting = True

    starttime_front = float(printer.start_time_sheet_frontside) + (float(
        rfq.number_pms_colors_front) * printer.start_time_pms_color) + (float(
        rfq.pressvarnish_front) * float(start_time_varnish))

    starttime_rear = float(printer.start_time_sheet_backside) + (float(
        rfq.number_pms_colors_rear) * printer.start_time_pms_color) + (float(
        rfq.pressvarnish_rear) * float(start_time_varnish))

    if rfq.printsided == 1:  # 'Eenzijdig':
        starttime_rear = 0.0

    if rfq.printsided == 2:  # 'Tweezijdig gelijk' or use_perfecting:
        starttime_rear = 0.0

    printing_starttime = printer.starttime_per_order + starttime_front + starttime_rear
    return printing_starttime


def printing_runtime_calculation(rfq, printer_id, paper_quantity, items_per_sheet, paperweight_m2):
    printer = Printers.objects.get(printer_id=printer_id)
    paperweight_m2 = int(paperweight_m2)
    printing_runtime = float(paper_quantity / printer.productionspeed_sheets_hour) * 60.0
    speedreduction_heavy_paper = 1.0
    speedreduction_light_paper = 1.0
    speedreduction_perfecting = 1.0
    number_of_printruns = 1.0

    if rfq.printsided == 2:  # 'Tweezijdig gelijk' and printer.perfecting:
        number_of_printruns = 1.0
        speedreduction_perfecting = ((100 - printer.perc_speedreduction_perfecting) / 100)

    if paperweight_m2 > printer.weight_heavy_paper:
        speedreduction_heavy_paper = ((100 - printer.perc_speedreduction_heavy_paper) / 100)

    if paperweight_m2 < printer.weight_light_paper:
        speedreduction_light_paper = float((100 - printer.perc_speedreduction_light_paper) / 100)

    printing_runtime = float(printing_runtime) * float(
        number_of_printruns) * speedreduction_heavy_paper * speedreduction_light_paper * float(
        speedreduction_perfecting)
    return printing_runtime


def printingcost_calculation(set_up, volume, tariff_eur_hour, printing_starttime, printing_runtime):
    if set_up:
        printing_runtime = printing_runtime
    else:
        printing_runtime = (1000 / volume) * printing_runtime

    printing_hours = (printing_starttime + printing_runtime) / 60
    printingcost = printing_hours * float(tariff_eur_hour)
    return printingcost


def purchase_plates_calculation(rfq, printer_id, items_per_sheet, number_of_printruns):
    printer = Printers.objects.get(printer_id=printer_id)
    number_colors_front = float(calculate_number_of_colors_front(rfq, printer.varnish_unit))
    number_colors_rear = float(calculate_number_of_colors_rear(rfq, printer.varnish_unit))
    buy_tariff_plate_eur = float(printer.buy_tariff_plate_eur)

    purchase_plates_front = number_colors_front * buy_tariff_plate_eur
    purchase_plates_rear = number_colors_rear * buy_tariff_plate_eur

    if number_of_printruns == 1 and not printer.perfecting:
        purchase_plates_rear = 0
    if items_per_sheet % 2 == 0 and not printer.perfecting and rfq.printsided == 1:  # "Eenzijdig":
        purchase_plates_rear = 0

    purchase_plates = purchase_plates_front + purchase_plates_rear
    return purchase_plates


def margin_plates_calculation(rfq, printer_id, items_per_sheet, number_of_printruns):
    printer = Printers.objects.get(printer_id=printer_id)
    number_colors_front = float(calculate_number_of_colors_front(rfq, printer.varnish_unit))
    number_colors_rear = float(calculate_number_of_colors_rear(rfq, printer.varnish_unit))
    margin_plate_eur = float(printer.margin_plate_eur)

    margin_plates_front = number_colors_front * margin_plate_eur
    margin_plates_rear = number_colors_rear * margin_plate_eur

    if number_of_printruns == 1 and not printer.perfecting:
        margin_plates_rear = 0
    if items_per_sheet % 2 == 0 and not printer.perfecting and rfq.printsided == 1:  # "Eenzijdig":
        margin_plates_rear = 0

    margin_plates = margin_plates_front + margin_plates_rear
    return margin_plates


# Printingwaste calculation
def printingwaste_calculation(set_up, rfq, printer_id, printsided, items_per_sheet):
    waste_setup = 0

    printer = Printers.objects.get(printer_id=printer_id)
    print_front = rfq.print_front
    number_pms_colors_front = rfq.number_pms_colors_front
    pressvarnish_front = int(rfq.pressvarnish_front)
    pressvarnish_rear = int(rfq.pressvarnish_rear)
    print_rear = rfq.print_rear
    number_pms_colors_rear = int(rfq.number_pms_colors_rear)

    waste_perfecting = 0

    printingwaste_front = int(printer.paperwaste_per_order)
    printingwaste_rear = 0

    if printsided == 2:  # 'Tweezijdig gelijk':
        print_rear = print_front
        number_pms_colors_rear = number_pms_colors_front
        pressvarnish_rear = pressvarnish_front

    waste_printrun_pms = int(
        (number_pms_colors_front + number_pms_colors_rear) * printer.perc_paperwaste_printing_1000_sheet_perfector)

    if printsided != 1:  # 'Eenzijdig' and number_of_printruns == 1:
        waste_perfecting = int(printer.perc_paperwaste_printing_1000_sheet_perfector)

    if set_up:
        if rfq.print_front == 1:  # 'black':
            printingwaste_front = printingwaste_front + printer.paperwaste_per_side_blac
        if rfq.print_front == 4:  # 'Full Colour':
            printingwaste_front = printingwaste_front + printer.paperwaste_per_side_fc

        if print_rear == 1:  # 'black':
            printingwaste_rear = int(printer.paperwaste_per_side_black)
        if print_rear == 4:  # 'Full Colour':
            printingwaste_rear = int(printer.paperwaste_per_side_fc)

        printingwaste_pms = int(rfq.number_pms_colors_front) + number_pms_colors_rear * printer.paperwaste_per_side_pms
        printingwaste_pressvarnish = (pressvarnish_front + pressvarnish_rear) * int(printer.paperwaste_per_side_varnish)
        waste_setup = printingwaste_front + printingwaste_rear + printingwaste_pms + printingwaste_pressvarnish

    # waste printrun
    waste_printrun_basis = int(printer.perc_paperwaste_printing_1000_sheets)
    waste_per1000 = (1 / items_per_sheet) * (1000 * 0.01) * int(waste_printrun_basis) + int(
        waste_printrun_pms) + waste_perfecting

    waste_printrun = float(rfq.volume * 0.001) * waste_per1000 / items_per_sheet
    printingwaste = int(waste_setup + waste_printrun)

    return printingwaste


def paperprice_1000sheets_calculation(producer_id, paperspec_id):
    paperprice_1000sheets = PaperCatalog.objects.get(producer_id=producer_id,
                                                     paperspec_id=paperspec_id).price_1000sheets
    return paperprice_1000sheets


# Berekening papiercost

def papercost_calculation(paper_quantity, paperprice_1000sheets):
    papercost = float(paper_quantity) * float(paperprice_1000sheets) * float(0.001)
    return papercost


def papiertoeslag(producer_id, papiercost_input):
    perc = GeneralCalculationSettings.objects.get(producer_id=producer_id).toeslag_inkoop_papier_perc
    if not perc or perc == 0.00:
        toeslag = 0.00
    else:
        toeslag = float(perc / 100) * papiercost_input
    return toeslag


def inkoop_papier(papier_code, aantaldrukvelbruto, producer_id):
    paksinhoud_test = PaperCatalog.objects.get(paperspec_id=papier_code, producer_id=producer_id).paksinhoud

    try:
        inkoop_papier_calc = int(math.ceil(aantaldrukvelbruto / paksinhoud)) * paksinhoud_test
    except:
        inkoop_papier_calc = aantaldrukvelbruto
    return inkoop_papier_calc


def paksinhoud(papier_code, producer_id):
    try:
        paksinhoud_calc = PaperCatalog.objects.get(paperspec_id=papier_code,
                                                   producer_id=producer_id).paksinhoud
    except:
        paksinhoud_calc = PaperCatalog.objects.get(paperspec_id=papier_code,
                                                   producer_id=producer_id).paksinhoud
    return paksinhoud_calc


def definecuttingmachine(producer_id, paperspec_id):
    paperbrand = PaperCatalog.objects.filter(paperspec_id=paperspec_id)[0]
    vel_width = paperbrand.paper_width_mm / 2
    vel_height = paperbrand.paper_height_mm

    cuttingmachines = pd.DataFrame(
        Cuttingmachines.objects.filter(producer_id=producer_id, max_width_mm__gte=vel_height,
                                       max_depth_mm__gte=vel_width).values())
    cuttingmachine_id = \
        cuttingmachines[cuttingmachines.tariff_eur_hour == min(cuttingmachines.tariff_eur_hour)][
            'cuttingmachine_id'].iloc[
            0]
    return cuttingmachine_id


def define_bindingmachine_name(producer_id, bindingmachine_id):
    bindingmachine_name = Bindingmachines.objects.get(producer_id=producer_id,
                                                      bindingmachine_id=bindingmachine_id).asset_name
    return bindingmachine_name


def define_cuttingmachine_name(producer_id, cuttingmachine_id):
    cuttingmachine_name = Cuttingmachines.objects.get(producer_id=producer_id,
                                                      cuttingmachine_id=cuttingmachine_id).asset_name
    return cuttingmachine_name


def cuttingruntimecalculation(cuttingmachine_id, paperspec_id, items_per_sheet, volume):
    paper = PaperCatalog.objects.get(paperspec_id=paperspec_id)
    cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id)
    max_stackheight_mm = cuttingmachine.max_stackheight_mm * 10
    paper_thickening = 1
    number_of_cuts = items_per_sheet

    if paper.paper_thickening:
        paper_thickening = paper.paper_thickening

    cutting_stackheight_mm = volume * paper.paperweight_m2 * float(paper_thickening) * 0.001
    number_of_stacks = cutting_stackheight_mm / max_stackheight_mm
    number_of_stacks = math.ceil(number_of_stacks)
    if number_of_stacks < 1:
        number_of_stacks = 1

    stack_cuttingtime = float(cuttingmachine.time_cutting_sec) * number_of_stacks
    extra_cuttingtime = (number_of_cuts * cuttingmachine.time_per_extra_sec * number_of_stacks)
    cuttingruntime = float(stack_cuttingtime + extra_cuttingtime) / 3600
    return cuttingruntime


def cuttingcostcalculation(set_up, rfq, cuttingmachine_id, paperspec_id, items_per_sheet):
    cuttingmachine = Cuttingmachines.objects.get(cuttingmachine_id=cuttingmachine_id)
    cuttingsetuptime = float(0.0)
    volume = 1000 / items_per_sheet

    if set_up:
        cuttingsetuptime = float(cuttingmachine.setup_order_min) / 60
        volume = rfq.volume / items_per_sheet

    cuttingruntime = cuttingruntimecalculation(cuttingmachine_id, paperspec_id, items_per_sheet, volume)
    cuttingtotaltime = cuttingsetuptime + cuttingruntime
    cuttingcost = cuttingtotaltime * float(cuttingmachine.tariff_eur_hour)
    cuttingcost = float(cuttingcost)
    return cuttingcost


def packaging_cost_calculation(set_up, rfq, packagingoption_id, producer_id, orderweight_kg):
    packaging_tariff = PackagingTariffs.objects.get(producer_id=producer_id, packagingoption_id=packagingoption_id,
                                                    availeble=True)
    packaging_unit_costs = float(0.0)
    if set_up:
        orderweight_kg = orderweight_kg
        set_op_cost = float(packaging_tariff.setup_cost)

    else:
        orderweight_kg = float(orderweight_kg / (rfq.volume * float(0.001)))
        set_op_cost = float(0.0)

    max_weight_packaging_unit_kg = packaging_tariff.max_weight_packaging_unit_kg
    if max_weight_packaging_unit_kg > 0:
        number_of_packaging_units = np.ceil(orderweight_kg / packaging_tariff.max_weight_packaging_unit_kg)
        packaging_unit_costs = float(number_of_packaging_units) * float(packaging_tariff.cost_per_unit)

    packaging_cost_per_100kg = (orderweight_kg * float(.01)) * float(packaging_tariff.cost_per_100kg)
    packaging_cost = set_op_cost + packaging_cost_per_100kg + packaging_unit_costs
    return packaging_cost


def transport_costs_calculation(set_up, rfq, transportoption_id, producer_id, orderweight_kg):
    transporttariff = TransportTariffs.objects.get(producer_id=producer_id, transportoption_id=transportoption_id,
                                                   availeble=True)

    if set_up:
        orderweight_kg = orderweight_kg
        setup_cost = float(transporttariff.setup_cost)

    else:
        orderweight_kg = float(orderweight_kg * (1000 / rfq.volume))
        setup_cost = float(0.0)

    transport_costs = setup_cost + (orderweight_kg * float(transporttariff.cost_per_100kg) * .01)
    return transport_costs


def calculate_enhancement_cost(set_up, volume, enhancement_id, enhancement_tariffs):
    enhancement_cost = 0.0
    setup_cost = 0.0

    enhancement_tariffs = enhancement_tariffs[enhancement_tariffs.enhancement_id == enhancement_id]
    min_tariff = min(enhancement_tariffs.production_cost_1000sheets)

    enhancement_tariff = \
        enhancement_tariffs[enhancement_tariffs.production_cost_1000sheets == min_tariff].iloc[0]

    if set_up:
        setup_cost = float(enhancement_tariff.setup_cost)

    if enhancement_tariff.any():
        enhancement_cost = volume * float(
            enhancement_tariff.production_cost_1000sheets)
        enhancement_cost = enhancement_cost + setup_cost
        if set_up:
            if enhancement_cost < float(enhancement_tariff.minimum_cost):
                enhancement_cost = float(enhancement_tariff.minimum_cost)
        else:
            enhancement_cost = enhancement_cost

    return enhancement_cost


def enhancement_cost_calculation(set_up, rfq, producer_id, paper_quantity_cover, paperspec_id, items_per_sheet):
    enhancement_cost_front = 0.0
    enhancement_cost_rear = 0.0
    paperspec = PaperCatalog.objects.get(paperspec_id=paperspec_id)

    volume = (1000 / items_per_sheet) * 0.001
    if set_up:
        volume = paper_quantity_cover * 0.001

    enhancement_tariffs = pd.DataFrame(
        EnhancementTariffs.objects.filter(producer_id=producer_id, availeble=True,
                                          max_sheet_width__lte=paperspec.paper_width_mm,
                                          max_sheet_height__lte=paperspec.paper_height_mm).values())

    if rfq.enhance_front > 0:
        enhancement_cost_front = calculate_enhancement_cost(set_up, volume, rfq.enhance_front, enhancement_tariffs)

    if rfq.enhance_rear > 0:
        enhancement_cost_rear = calculate_enhancement_cost(set_up, volume, rfq.enhance_rear, enhancement_tariffs)

    enhancement_cost = enhancement_cost_front + enhancement_cost_rear
    return enhancement_cost


def added_value_plano_calculation(producer_id, rfq, total_cost, papercost,
                                  foldingmachine_id, foldingcost, inkcost, purchase_plates,
                                  paperspec_id, enhancementcost):
    folding_purchase = 0.0
    enhance_purchase = 0.0
    enhance_front_added_value = True
    enhance_rear_added_value = True
    enhancement_tariffs_front = []

    added_value_foldingmachine = Foldingmachines.objects.get(producer_id=producer_id,
                                                             foldingmachine_id=foldingmachine_id).added_value

    if not added_value_foldingmachine:
        folding_purchase = foldingcost

    try:
        enhancement_id_front = EnhancementOptions.objects.get(enhancement=rfq.enhance_front).enhancement_id
    except EnhancementOptions.DoesNotExist:
        enhancement_id_front = 0

    try:
        enhancement_id_rear = EnhancementOptions.objects.get(enhancement=rfq.enhance_rear).enhancement_id
    except EnhancementOptions.DoesNotExist:
        enhancement_id_rear = 0

    if enhancement_id_front > 0 or enhancement_id_rear > 0:
        paperspec = PaperCatalog.objects.get(paperspec_id=paperspec_id)
        enhancement_tariffs = pd.DataFrame(
            EnhancementTariffs.objects.filter(producer_id=producer_id, availeble=True,
                                              max_sheet_width__lte=paperspec.paper_width_mm,
                                              max_sheet_height__lte=paperspec.paper_height_mm).values())

        if enhancement_id_front > 0:
            enhancement_tariffs_front = enhancement_tariffs[enhancement_tariffs.enhancement_id == enhancement_id_front]
            min_tariff = min(enhancement_tariffs_front.production_cost_1000sheets)
            enhance_front_added_value = \
                enhancement_tariffs[enhancement_tariffs.production_cost_1000sheets == min_tariff].iloc[0].added_value

        if enhancement_id_rear > 0:
            enhancement_tariffs_rear = enhancement_tariffs[enhancement_tariffs.enhancement_id == enhancement_id_rear]
            min_tariff = min(enhancement_tariffs_front.production_cost_1000sheets)
            enhance_rear_added_value = \
                enhancement_tariffs[enhancement_tariffs.production_cost_1000sheets == min_tariff].iloc[0].added_value

        if not enhance_front_added_value or not enhance_rear_added_value:
            enhance_purchase = enhancementcost

    purchase = papercost + inkcost + purchase_plates + folding_purchase + enhance_purchase
    brochure_added_value = total_cost - purchase
    return brochure_added_value


def find_paper_width(paperspec_id_fit_for_printer):
    paperspec__fit_for_printer = PaperCatalog.objects.get(paperspec_id=paperspec_id_fit_for_printer)
    paper_width_mm = paperspec__fit_for_printer.paper_width_mm
    return paper_width_mm


def find_paper_height(paperspec_id_fit_for_printer):
    paperspec__fit_for_printer = PaperCatalog.objects.get(paperspec_id=paperspec_id_fit_for_printer)
    paper_height_mm = paperspec__fit_for_printer.paper_height_mm
    return paper_height_mm
