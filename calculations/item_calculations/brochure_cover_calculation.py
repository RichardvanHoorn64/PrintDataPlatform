from calculations.functions.functions_brochures import *
from calculations.functions.functions_general import *


def brochure_cover_calculation(producer_id, rfq, book_thickness, portrait_landscape):
    error = []
    calculation_cover = []

    # Test paper choice availability and define papercatalog
    if not error:
        try:
            paper_fit_for_rfq_cover = paper_available_cover(rfq, producer_id)
        except Exception as e:
            error = 'Paper fit_for rfq brochure cover not available'
            print('error log: ' + error + ' ' + str(e))

    # Singe cover size
    single_cover_width = []
    single_cover_height = []
    if not error:
        try:
            single_cover = single_cover_size_calculation(rfq, producer_id, book_thickness, portrait_landscape)
            single_cover_width = single_cover[0]
            single_cover_height = single_cover[1]

        except Exception as e:
            error = 'No cover printsize calculated'
            print('error log: ' + error + ' ' + str(e))

    # - Calculation cover ----------------------------------------------------------------------------------------
    assets_printers_cover = []

    try:
        assets_printers_cover = pd.DataFrame(Printers.objects.filter(producer_id=producer_id).values())

    except Printers.DoesNotExist:
        error = 'No cover printer fit for this request.'
        print('error log: ' + error)

    if not error:
        try:
            calculation_cover = pd.DataFrame(
                assets_printers_cover[(assets_printers_cover.printsize_width >= single_cover_width)
                                      & (assets_printers_cover.printsize_height >= single_cover_height)
                                      ])
            calculation_cover['asset_name_cover'] = calculation_cover['asset_name']
        except Exception as e:
            error = 'No cover printers fit for cover'
            print('error log: ' + error + ' ' + str(e))

    # PAPER CALCULATION
    # select paperspec_id fit for printer cover
    if not error:
        try:
            calculation_cover['printer_id_cover'] = calculation_cover['printer_id']
            calculation_cover.drop(['printer_id_cover'], axis=1)
            calculation_cover['printer_cover'] = calculation_cover['asset_name']
            calculation_cover['paperspec_id_cover'] = calculation_cover.apply(
                lambda row: paperidselector(row['printer_id_cover'], paper_fit_for_rfq_cover, single_cover_height,
                                                  single_cover_width), axis=1)

        except Exception as e:
            error = 'Calculation paperspec_id for cover failed'
            print('error log: ' + error + ' ' + str(e))

    if not error and len(calculation_cover) == 0:
        error = 'Paperbrand cover not availeble.'

    # Define number of colors cover, per printer, pressvarnish
    if not error:
        try:
            calculation_cover['number_of_colors_cover'] = calculation_cover.apply(
                lambda row: calculate_number_of_colors_front(rfq, row['varnish_unit']), axis=1)
            calculation_cover['number_of_colors_back_cover'] = calculation_cover.apply(
                lambda row: calculate_number_of_colors_back(rfq, row['varnish_unit']), axis=1)
        except Exception as e:
            error = 'Calculation number of colors cover failed'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:
            calculation_cover['items_per_sheet_cover'] = calculation_cover.apply(
                lambda row: items_per_sheet_calculation(row['paperspec_id_cover'], single_cover_height,
                                                        single_cover_width),
                axis=1)
        except Exception as e:
            error = 'items per_sheet calculation failed'
            print('error log: ' + error + ' ' + str(e))

    # calculate paper_width height cover
    if not error:
        try:
            calculation_cover['paper_width_cover'] = calculation_cover.apply(
                lambda row: find_paper_width(row['paperspec_id_cover'], ), axis=1)

            calculation_cover['paper_height_cover'] = calculation_cover.apply(
                lambda row: find_paper_height(row['paperspec_id_cover'], ), axis=1)

        except Exception as e:
            error = 'Papersizes cover runs not defined'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:

            calculation_cover['number_of_printruns_cover'] = calculation_cover.apply(
                lambda row: number_of_printruns_calculation(rfq.printsided, row['printer_id_cover']), axis=1)
        except Exception as e:
            error = 'Number of_printruns cover not defined'
            print('error log: ' + error + ' ' + str(e))

    # calculate platecost cover
    if not error:
        try:
            calculation_cover['purchase_plates_cover'] = calculation_cover.apply(
                lambda row: purchase_plates_calculation(rfq, row['printer_id_cover'], row['items_per_sheet_cover'],
                                                        row['number_of_printruns_cover']), axis=1)
            calculation_cover['margin_plates_cover'] = calculation_cover.apply(
                lambda row: margin_plates_calculation(rfq, row['printer_id_cover'], row['items_per_sheet_cover'],
                                                      row['number_of_printruns_cover']), axis=1)
            calculation_cover['platecost_cover'] = calculation_cover['purchase_plates_cover'] + \
                                                   calculation_cover['margin_plates_cover']
        except Exception as e:
            error = 'Calculation platecost cover failed'
            print('error log: ' + error + ' ' + str(e))

    # calculate printing cover

    # calculate printingwaste cover
    if not error:
        try:

            calculation_cover['waste_printing_cover'] = calculation_cover.apply(
                lambda row: printingwaste_calculation(True, rfq, row['printer_id_cover'],
                                                      rfq.printsided, row['items_per_sheet_cover']),
                axis=1)

            calculation_cover['waste_printing_cover1000extra'] = calculation_cover.apply(
                lambda row: printingwaste_calculation(False, rfq, row['printer_id_cover'],
                                                      rfq.printsided, row['items_per_sheet_cover']),
                axis=1)

        except Exception as e:
            error = 'No printingwaste calculation for cover'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:
            calculation_cover['net_paper_quantity_cover'] = calculation_cover.apply(
                lambda row: net_paper_quantity_calculation(rfq.volume, row['items_per_sheet_cover'], ),
                axis=1)
            calculation_cover['net_paper_quantity_cover1000extra'] = calculation_cover.apply(
                lambda row: net_paper_quantity_calculation(1000, row['items_per_sheet_cover'], ),
                axis=1)

        except Exception as e:
            error = 'net_paper_quantity_complete_cover failed'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:
            calculation_cover['paper_quantity_cover'] = calculation_cover[
                                                            'net_paper_quantity_cover'] + \
                                                        calculation_cover['waste_printing_cover']
            calculation_cover['paper_quantity_cover1000extra'] = calculation_cover[
                                                                     'net_paper_quantity_cover1000extra'] + \
                                                                 calculation_cover['waste_printing_cover1000extra']
        except Exception as e:
            error = 'net_paper_quantity_complete_cover failed'
            print('error log: ' + error + ' ' + str(e))

    # cover cutting
    if not error:
        try:
            calculation_cover['cuttingmachine_cover'] = calculation_cover.apply(
                lambda row: definecuttingmachine(producer_id, row['paperspec_id_cover'], ), axis=1)
            calculation_cover = calculation_cover[calculation_cover['cuttingmachine_cover'] != 0]
        except Exception as e:
            error = 'No cuttingmachine for cover availeble'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:
            calculation_cover['cuttingcost_cover'] = calculation_cover.apply(
                lambda row: cuttingcostcalculation(True, rfq, row['cuttingmachine_cover'], row['paperspec_id_cover'],
                                                   row['items_per_sheet_cover']),
                axis=1)
            calculation_cover['cuttingcost_cover1000extra'] = calculation_cover.apply(
                lambda row: cuttingcostcalculation(False, rfq, row['cuttingmachine_cover'], row['paperspec_id_cover'],
                                                   row['items_per_sheet_cover']),
                axis=1)

        except Exception as e:
            error = 'Cutting cover calculation failed.' + str(e)

        try:
            calculation_cover['enhancecost_cover'] = calculation_cover.apply(
                lambda row: enhancement_cost_calculation(True, rfq, producer_id, row['paper_quantity_cover'],
                                                         row['paperspec_id_cover'], row['items_per_sheet_cover']),
                axis=1)
            calculation_cover['enhancecost_cover1000extra'] = calculation_cover.apply(
                lambda row: enhancement_cost_calculation(False, rfq, producer_id, row['paper_quantity_cover'],
                                                         row['paperspec_id_cover'],
                                                         row['items_per_sheet_cover']),
                axis=1)

        except Exception as e:
            error = 'Enhancement cost calculation cover failed, set tariff'
            print('error log: ' + error + ' ' + str(e))

    if not error:
        try:
            calculation_cover['printing_starttime_cover'] = calculation_cover.apply(
                lambda row: printing_starttime_calculation(rfq, row['printer_id_cover'], row['items_per_sheet_cover']),
                axis=1)
            # printing_runtime_calculation(rfq, printer_id, paper_quantity, items_per_sheet):
            calculation_cover['printing_runtime_cover'] = calculation_cover.apply(
                lambda row: printing_runtime_calculation(rfq, row['printer_id_cover'], row['paper_quantity_cover'],
                                                         rfq.paperweight_cover),
                axis=1)

            calculation_cover['printing_runtime_cover1000extra'] = calculation_cover.apply(
                lambda row: printing_runtime_calculation(rfq, row['printer_id_cover'],
                                                         row['paper_quantity_cover1000extra'],
                                                         rfq.paperweight_cover),
                axis=1)

            calculation_cover['printingcost_cover'] = calculation_cover.apply(
                lambda row: printingcost_calculation(True, rfq.volume, row['tariff_eur_hour'],
                                                     row['printing_starttime_cover'],
                                                     row['printing_runtime_cover']),
                axis=1)

            calculation_cover['printingcost_cover1000extra'] = calculation_cover.apply(
                lambda row: printingcost_calculation(True, rfq.volume, row['tariff_eur_hour'], 0,
                                                     row['printing_runtime_cover1000extra']), axis=1)

        except Exception as e:
            error = 'Calculation printingcost cover failed'
            print('error log: ' + error + ' ' + str(e))

    # inkcost cover calculation
    if not error:
        try:
            calculation_cover['inkcost_cover'] = calculation_cover.apply(
                lambda row: inkcost_calculation(True, rfq, row['printer_id_cover'], row['paper_quantity_cover'],
                                                rfq.printsided), axis=1)
            calculation_cover['inkcost_cover1000extra'] = calculation_cover.apply(
                lambda row: inkcost_calculation(False, rfq, row['printer_id_cover'],
                                                row['paper_quantity_cover1000extra'],
                                               rfq.printsided), axis=1)
        except Exception as e:
            error = 'Inkcost calculation cover failed'
            print('error log: ' + error + ' ' + str(e))

    best_calculation_cover = []
    if not error:
        try:
            calculation_cover['cover_subtotal_cost'] = calculation_cover['printingcost_cover'] + \
                                                       calculation_cover['cuttingcost_cover'] + \
                                                       calculation_cover['enhancecost_cover'] + \
                                                       calculation_cover['inkcost_cover'] + \
                                                       calculation_cover['platecost_cover']

            calculation_cover['cover_subtotal_cost1000extra'] = calculation_cover['printingcost_cover1000extra'] + \
                                                            calculation_cover['cuttingcost_cover1000extra'] + \
                                                            calculation_cover['enhancecost_cover1000extra'] + \
                                                            calculation_cover['inkcost_cover1000extra']

            best_calculation_cover = calculation_cover.loc[
                calculation_cover.groupby('producer_id')['cover_subtotal_cost'].idxmin()]
        except Exception as e:
            error = "Total groupby error cover: " + str(error)
            print('error log: ' + error + ' ' + str(e))

    return best_calculation_cover, error
