from calculations.functions.function_save_calculation import save_calculation
from calculations.functions.functions_brochures import *
from calculations.functions.functions_general import *
from calculations.item_calculations.brochure_cover_calculation import brochure_cover_calculation


def brochure_calculation(producer_id, rfq):
    selfcover = False
    if rfq.productcategory_id == 3:
        selfcover = True


    # Test productsize input
    error = []
    if not error:
        productsize_check(rfq)

    portrait_landscape = rfq.portrait_landscape
    if rfq.height_mm_product == rfq.width_mm_product:
        portrait_landscape = 'vierkant'

    # general settings
    calculationsettings = GeneralCalculationSettings.objects.get(producer_id=producer_id)
    katernmargin = calculationsettings.katernmargin
    headmargin = calculationsettings.headmargin
    number_of_pages = multiple_of4(rfq.number_of_pages)
    purchase_paper_perc_added = GeneralCalculationSettings.objects.get(
        producer_id=producer_id).purchase_paper_perc_added

    # packaging and transport
    if not error:
        try:
            packagingtariff = PackagingOptions.objects.get(packagingoption_id=rfq.packaging)
            packagingoption_id = packagingtariff.packagingoption_id
        except Exception as e:
            error = 'No packagingtariff available, update settings.' + str(e)

    if not error:
        try:
            transport = "Verzenden, naar één adres in Nederland"
            transporttariff = TransportOptions.objects.get(transport=transport)
            transportoption_id = transporttariff.transportoption_id
        except Exception as e:
            error = 'No transporttariff available, update settings.' + str(e)

    # Test paper choice availability
    paper_fit_for_rfq = []
    if not error:
        try:
            paper_fit_for_rfq = paper_available_booklet(rfq, producer_id)
            if len(paper_fit_for_rfq) == 0:
                error = 'Paper for brochure booklet not available.'
        except Exception as e:
            error = 'Paper fit_for rfq brochure booklet not available.' + str(e)

    # Test productsize input
    if not error:
        productsize_check(rfq)

    # Calculate book thickness
    book_thickness = 0
    if not error:
        try:
            book_thickness = calc_book_thickness(selfcover, rfq, producer_id)
        except Exception as e:
            error = 'book thickness calculation failed, ' + str(e)

    # booklet------------------------------------------------------------------------------------------
    # paper booklet
    katern_aflopend = True
    katern_height = 0
    katern_width = 0

    if not error:
        try:
            # katerns 4 pages per sheet
            katern_width = katern_width_calc(rfq, katernmargin, headmargin)
            katern_height = katern_height_calc(rfq, katernmargin, headmargin)

            # katerns 8 pages per sheet
            katernheight8_mm = height_mm_calc(katern_aflopend, katern_height, producer_id)
            katernwidth8_mm = width_mm_calc(katern_aflopend, katern_width, producer_id)
        except Exception as e:
            error = 'No katernsizes calculated.' + str(e)

    # select printers for booklet
    calculation_booklet = []

    try:
        assets_printers_booklet = pd.DataFrame(Printers.objects.filter(producer_id=producer_id).values())

    except Printers.DoesNotExist:
        assets_printers_booklet = []
        error = 'No booklet printer fit for this request.'

    if not error:
        try:
            calculation_booklet = pd.DataFrame(
                assets_printers_booklet[(assets_printers_booklet.printsize_width >= katern_width)
                                        & (assets_printers_booklet.printsize_height >= katern_height)
                                        ])

            calculation_booklet['filter'] = calculation_booklet.apply(
                lambda row: printerfilter_booklet(row['printer_id'], rfq, ), axis=1)

            calculation_booklet['printer_booklet'] = calculation_booklet['asset_name']
            if len(calculation_booklet) == 0:
                error = 'No booklet printers fit for katern of 8 pages.'

        except Exception as e:
            error = 'No booklet printers fit for katern of 8 pages:' + str(e)

    if not error:
        try:
            calculation_booklet['order_startcost'] = calculate_order_startcost(producer_id)
        except Exception as e:
            error = 'No order_startcost defined:' + str(e)

            #  calculate number of booklet pages per printer
    if not error:
        try:
            # Pages per booklet sheet
            calculation_booklet['pages_per_sheet_booklet'] = calculation_booklet.apply(
                lambda row: pages_per_sheet_booklet_calculation(row['printer_id'], katernheight8_mm,
                                                                katernwidth8_mm), axis=1)

        except Exception as e:
            error = 'Calculation max number of booklet pages per printer per sheet failed.  Error:' + str(e)

        # PAPER CALCULATION
        # select paperspec_id fit for printer booklet
    if not error:
        try:
            calculation_booklet['paperspec_id_booklet'] = calculation_booklet.apply(
                lambda row: paperidselector_booklet(row['printer_id'], row['pages_per_sheet_booklet'],
                                                    paper_fit_for_rfq,
                                                    katernheight8_mm, katernwidth8_mm, katernmargin), axis=1)

        except Exception as e:
            error = 'Calculation paperspec_id for booklet failed.' + str(e)

    # Define number of colors booklet, per printer, pressvarnish
    if not error:
        try:
            calculation_booklet['number_of_colors_booklet'] = calculation_booklet.apply(
                lambda row: calculate_number_of_colors_booklet(rfq, row['varnish_unit']), axis=1)
        except Exception as e:
            error = 'Calculation number of_colors booklet failed.' + str(e)

    # calculate number of printing sheets
    if not error:
        try:
            calculation_booklet['number_of_rest_pages'] = calculation_booklet.apply(
                lambda row: calculate_number_of_rest_pages(number_of_pages, row['pages_per_sheet_booklet']),
                axis=1)

            # full sheet for intern pages
            calculation_booklet['number_of_sheets_complete_booklet'] = calculation_booklet.apply(
                lambda row: calculate_number_of_sheets_complete(number_of_pages, row['pages_per_sheet_booklet']),
                axis=1)

            # sheet for extra pages
            calculation_booklet['number_of_sheets_incomplete_booklet'] = calculation_booklet.apply(
                lambda row: calculate_number_of_sheets_incomplete(number_of_pages,
                                                                  row['pages_per_sheet_booklet']), axis=1)
        except Exception as e:
            error = 'Calculation number of printing sheets failed.' + str(e)

    # calculate net paper quantity
    if not error:
        try:
            calculation_booklet['net_paper_quantity_incomplete_booklet'] = calculation_booklet.apply(
                lambda row: calculate_net_paper_quantity_incomplete_booklet(rfq.volume, row['number_of_rest_pages'],
                                                                            row['number_of_sheets_incomplete_booklet'],
                                                                            row['pages_per_sheet_booklet']),
                axis=1)

            calculation_booklet['net_paper_quantity_incomplete_booklet1000extra'] = calculation_booklet.apply(
                lambda row: calculate_net_paper_quantity_incomplete_booklet(1000, row['number_of_rest_pages'],
                                                                            row['number_of_sheets_incomplete_booklet'],
                                                                            row['pages_per_sheet_booklet']),
                axis=1)

            calculation_booklet['net_paper_quantity_complete_booklet'] = calculation_booklet.apply(
                lambda row: calculate_net_paper_quantity_complete_booklet(rfq.volume,
                                                                          row['number_of_sheets_complete_booklet'],
                                                                          ),
                axis=1)

            calculation_booklet['net_paper_quantity_complete_booklet1000extra'] = calculation_booklet.apply(
                lambda row: calculate_net_paper_quantity_complete_booklet(1000,
                                                                          row['number_of_sheets_complete_booklet'],
                                                                          ),
                axis=1)

            calculation_booklet['net_paper_quantity_booklet'] = calculation_booklet[
                                                                    'net_paper_quantity_complete_booklet'] + \
                                                                calculation_booklet[
                                                                    'net_paper_quantity_incomplete_booklet']
            calculation_booklet['net_paper_quantity_booklet1000extra'] = calculation_booklet[
                                                                             'net_paper_quantity_complete_booklet1000extra'] + \
                                                                         calculation_booklet[
                                                                             'net_paper_quantity_incomplete_booklet1000extra']

        except Exception as e:
            error = 'Calculation net paper quantity failed.' + str(e)

        # PRINTING CALCULATION
        # number of printruns_booklet
    if not error:
        try:
            calculation_booklet['number_of_printruns_booklet'] = calculation_booklet.apply(
                lambda row: calculate_number_of_printruns_booklet(row['printer_id'],
                                                                  row['number_of_sheets_complete_booklet'],
                                                                  row['number_of_sheets_incomplete_booklet'],
                                                                  row['number_of_rest_pages'],
                                                                  row['pages_per_sheet_booklet']), axis=1)
        except Exception as e:
            error = 'No calculation of number of printruns.' + str(e)

    # calculate platecost booklet
    if not error:
        try:
            calculation_booklet['purchase_plates_booklet'] = calculation_booklet.apply(
                lambda row: purchase_plates_booklet_calculation(row['printer_id'], row['number_of_printruns_booklet'],
                                                                rfq), axis=1)
            calculation_booklet['margin_plates_booklet'] = calculation_booklet.apply(
                lambda row: margin_plates_booklet_calculation(row['printer_id'], row['number_of_printruns_booklet'],
                                                              rfq), axis=1)
            calculation_booklet['platecost_booklet'] = calculation_booklet['purchase_plates_booklet'] + \
                                                       calculation_booklet['margin_plates_booklet']
        except Exception as e:
            error = 'No calculation of platecost booklet.' + str(e)

    if not error:
        try:

            calculation_booklet['waste_printing1000extra'] = calculation_booklet.apply(
                lambda row: printingwaste_booklet_calculation1000extra(rfq, row['printer_id'],
                                                                       row['net_paper_quantity_booklet1000extra'], ),
                axis=1)

            calculation_booklet['waste_printing'] = calculation_booklet.apply(
                lambda row: printingwaste_booklet_calculation(rfq, row['printer_id'],
                                                              row['waste_printing1000extra'],
                                                              row['number_of_printruns_booklet'], ),
                axis=1)

        except Exception as e:
            error = 'Printingwaste calculation for booklet failed.' + str(e)

    # FOLDING CALCULATION
    # folding booklet, calculate foldingfactor and number of pages per foldingsheet
    if not error:
        try:
            foldingmachines_fit_rfq = filter_foldingmachines_fit_rfq(producer_id, rfq)
            calculation_booklet['booklet_foldingfactor'] = calculation_booklet.apply(
                lambda row: calculate_booklet_foldingfactor(foldingmachines_fit_rfq, rfq, katernmargin, headmargin,
                                                            row['pages_per_sheet_booklet']), axis=1)
        except Exception as e:
            foldingmachines_fit_rfq = []
            error = 'Calculation booklet_foldingfactor failed.' + str(e)

    if not error:
        try:
            calculation_booklet['pages_per_katern_booklet'] = calculation_booklet.apply(
                lambda row: calculate_pages_per_katern_full(row['pages_per_sheet_booklet'],
                                                            row['booklet_foldingfactor'], ), axis=1)

            calculation_booklet['number_of_katerns_full'] = calculation_booklet.apply(
                lambda row: calculate_number_of_katerns_full(row['pages_per_katern_booklet'],
                                                             row['booklet_foldingfactor'],
                                                             number_of_pages), axis=1)

            calculation_booklet['number_of_katerns_half'] = calculation_booklet.apply(
                lambda row: calculate_number_of_katerns_half(number_of_pages,
                                                             row['number_of_katerns_full'],
                                                             row['pages_per_katern_booklet'], ), axis=1)

            calculation_booklet['number_of_katerns_quarter'] = calculation_booklet.apply(
                lambda row: calculate_number_of_katerns_quarter(number_of_pages,
                                                                row['number_of_katerns_full'],
                                                                row['number_of_katerns_half'],
                                                                row['pages_per_katern_booklet'], ), axis=1)

            calculation_booklet['number_of_katerns_total'] = calculation_booklet['number_of_katerns_full'] + \
                                                             calculation_booklet['number_of_katerns_half'] + \
                                                             calculation_booklet['number_of_katerns_quarter']
            calculation_booklet = calculation_booklet[calculation_booklet['number_of_katerns_total'] != 0]

        except Exception as e:
            error = 'Number of katerns not calculated.' + str(e)

    if not error and len(calculation_booklet) == 0:
        error = 'No number of katerns calculation.'

    # calculate paper_width height booklet
    if not error:
        try:
            calculation_booklet['paper_width_booklet'] = calculation_booklet.apply(
                lambda row: find_paper_width(row['paperspec_id_booklet'], ), axis=1)

            calculation_booklet['paper_height_booklet'] = calculation_booklet.apply(
                lambda row: find_paper_height(row['paperspec_id_booklet'], ), axis=1)

        except Exception as e:
            error = 'Papersizes booklet runs not defined.' + str(e)

    # cutting booklet sheets to katern size
    if not error:
        try:
            calculation_booklet['cuttingmachine_id_booklet'] = calculation_booklet.apply(
                lambda row: define_cuttingmachine_booklet(producer_id, row['paperspec_id_booklet'],
                                                          row['number_of_sheets_incomplete_booklet'],
                                                          row['booklet_foldingfactor']), axis=1)

            calculation_booklet['cuttingmachine_booklet'] = calculation_booklet.apply(
                lambda row: define_cuttingmachine_name(producer_id, row['cuttingmachine_id_booklet'], ), axis=1)

        except Exception as e:
            error = "No cuttingmachine booklet availeble" + str(e)

    if not error:
        try:
            calculation_booklet['cutting_starttime'] = calculation_booklet.apply(
                lambda row: cutting_setuptime_booklet(row['cuttingmachine_id_booklet'], row['booklet_foldingfactor'],
                                                      row['number_of_sheets_incomplete_booklet']), axis=1)

            calculation_booklet['cutting_runtime'] = calculation_booklet.apply(
                lambda row: cutting_runtime_booklet(row['booklet_foldingfactor'], row['cuttingmachine_id_booklet'],
                                                    row['paperspec_id_booklet'],
                                                    row['number_of_sheets_complete_booklet'],
                                                    row['number_of_sheets_incomplete_booklet'],
                                                    row['number_of_katerns_half'],
                                                    row['number_of_katerns_quarter'],
                                                    ), axis=1)

            calculation_booklet['cuttingcost_booklet'] = calculation_booklet.apply(
                lambda row: cuttingcost_booklet_calculation(row['cuttingmachine_id_booklet'],
                                                            row['cutting_starttime'],
                                                            row['cutting_runtime']),
                axis=1)
            calculation_booklet['cuttingcost_booklet1000extra'] = calculation_booklet.apply(
                lambda row: cuttingcost_booklet_calculation1000extra(rfq.volume, row['cuttingmachine_id_booklet'],
                                                                     row['cutting_starttime'],
                                                                     ),
                axis=1)

        except Exception as e:
            error = "Booklet cutting calculation failed" + str(e)

    # folding calculations
    if not error:
        try:
            calculation_booklet['foldingmachine_id'] = calculation_booklet.apply(
                lambda row: define_foldingmachine_id_booklet(foldingmachines_fit_rfq, 1,
                                                             row['paper_width_booklet'],
                                                             row['paper_height_booklet'],
                                                             row['pages_per_sheet_booklet'],
                                                             row['booklet_foldingfactor']), axis=1)

            calculation_booklet['foldingmachine_id_half'] = calculation_booklet.apply(
                lambda row: define_foldingmachine_id_booklet(foldingmachines_fit_rfq, 2,
                                                             row['paper_width_booklet'],
                                                             row['paper_height_booklet'],
                                                             row['pages_per_sheet_booklet'],
                                                             row['booklet_foldingfactor']), axis=1)

            calculation_booklet['foldingmachine_id_quarter'] = calculation_booklet.apply(
                lambda row: define_foldingmachine_id_booklet(foldingmachines_fit_rfq, 4,
                                                             row['paper_width_booklet'],
                                                             row['paper_height_booklet'],
                                                             row['pages_per_sheet_booklet'],
                                                             row['booklet_foldingfactor']), axis=1)

            calculation_booklet = calculation_booklet[calculation_booklet['foldingmachine_id'] != 0]

            calculation_booklet['foldingmachines_booklet'] = calculation_booklet.apply(
                lambda row: define_foldingmachine_names_booklet(
                    row['booklet_foldingfactor'],
                    row['foldingmachine_id'],
                    row['foldingmachine_id_half'],
                    row['foldingmachine_id_quarter']), axis=1)

        except Exception as e:
            error = 'Needed foldingmachines not defined.' + str(e)

    if not error and len(calculation_booklet) == 0:
        error = 'No fitting foldingmachine availeble.'

    if not error:
        try:
            calculation_booklet['foldingcost_booklet'] = calculation_booklet.apply(
                lambda row: foldingcost_booklet_calculation(True, rfq, row['booklet_foldingfactor'],
                                                            row['paper_width_booklet'], row['paper_height_booklet'],
                                                            row['foldingmachine_id'],
                                                            row['foldingmachine_id_half'],
                                                            row['foldingmachine_id_quarter'],
                                                            row['number_of_katerns_full'],
                                                            row['number_of_katerns_half'],
                                                            row['number_of_katerns_quarter'],
                                                            ), axis=1)
            calculation_booklet['foldingcost_booklet1000extra'] = calculation_booklet.apply(
                lambda row: foldingcost_booklet_calculation(False, rfq, row['booklet_foldingfactor'],
                                                            row['paper_width_booklet'], row['paper_height_booklet'],
                                                            row['foldingmachine_id'],
                                                            row['foldingmachine_id_half'],
                                                            row['foldingmachine_id_quarter'],
                                                            row['number_of_katerns_full'],
                                                            row['number_of_katerns_half'],
                                                            row['number_of_katerns_quarter'],
                                                            ), axis=1)

        except Exception as e:
            error = 'Folding cost booklet calculation failed.' + str(e)

    if not error:
        try:

            calculation_booklet['waste_folding'] = calculation_booklet.apply(
                lambda row: foldingwaste_booklet_calculation(True, rfq.volume, row['booklet_foldingfactor'],
                                                             row['paper_width_booklet'], row['paper_height_booklet'],
                                                             row['foldingmachine_id'],
                                                             row['foldingmachine_id_half'],
                                                             row['foldingmachine_id_quarter'],
                                                             row['number_of_katerns_full'],
                                                             row['number_of_katerns_half'],
                                                             row['number_of_katerns_quarter'],
                                                             ), axis=1)
            calculation_booklet['waste_folding1000extra'] = calculation_booklet.apply(
                lambda row: foldingwaste_booklet_calculation(False, 1000, row['booklet_foldingfactor'],
                                                             row['paper_width_booklet'], row['paper_height_booklet'],
                                                             row['foldingmachine_id'],
                                                             row['foldingmachine_id_half'],
                                                             row['foldingmachine_id_quarter'],
                                                             row['number_of_katerns_full'],
                                                             row['number_of_katerns_half'],
                                                             row['number_of_katerns_quarter'],
                                                             ), axis=1)
        except Exception as e:
            error = 'Folding waste booklet calculation failed.' + str(e)

    # BINDING CALCULATION
    if not error:
        try:
            finishingmethod_id = BrochureFinishingMethods.objects.get(
                finishingmethod_id=rfq.finishing_brochures).finishingmethod_id
            calculation_booklet['bindingmachine_id'] = calculation_booklet.apply(
                lambda row: define_bindingmachine_id(selfcover, producer_id, rfq, finishingmethod_id,
                                                     row['number_of_katerns_full'],
                                                     row['number_of_katerns_half'],
                                                     row['number_of_katerns_quarter'], ),
                axis=1)

            calculation_booklet['bindingmachine'] = calculation_booklet.apply(
                lambda row: define_bindingmachine_name(producer_id, row['bindingmachine_id'], ), axis=1)
        except Exception as e:
            error = 'No fitting bindingmachine for this request.' + str(e)

    if not error:
        try:
            calculation_booklet = calculation_booklet[calculation_booklet['bindingmachine_id'] != 0]
        except Exception as e:
            error = 'No fitting bindingmachines for this request.' + str(e)
    if not error and len(calculation_booklet) == 0:
        error = 'No fitting bindingmachines for this request.'

    if not error:
        try:
            calculation_booklet['bindingcost_setup'] = calculation_booklet.apply(
                lambda row: bindingcost_setup_calculation(row['bindingmachine_id'],
                                                          row['number_of_katerns_total'], portrait_landscape,
                                                          selfcover),
                axis=1)

            calculation_booklet['bindingcost_run'] = calculation_booklet.apply(
                lambda row: bindingcost_run_calculation(rfq.volume, portrait_landscape, row['number_of_katerns_total'],
                                                        row['bindingmachine_id'], ), axis=1)

            calculation_booklet['bindingcost'] = calculation_booklet.apply(
                lambda row: bindingcost_calculation(row['bindingcost_setup'], row['bindingcost_run'], ), axis=1)

            calculation_booklet['bindingcost1000extra'] = calculation_booklet.apply(
                lambda row: bindingcost_run_calculation(1000, portrait_landscape, row['number_of_katerns_total'],
                                                        row['bindingmachine_id'], ), axis=1)

        except Exception as e:
            error = 'Bindingcost booklet calculation failed.' + str(e)

    if not error:
        try:

            calculation_booklet['waste_binding'] = calculation_booklet.apply(
                lambda row: bindingwaste_booklet_calculation(row['bindingmachine_id'],
                                                             row['net_paper_quantity_booklet'],
                                                             ), axis=1)

            calculation_booklet['waste_binding1000extra'] = calculation_booklet.apply(
                lambda row: bindingwaste_booklet_calculation1000extra(row['bindingmachine_id'],
                                                                      row['net_paper_quantity_booklet'],
                                                                      rfq.volume), axis=1)
        except Exception as e:
            error = 'Bindingwaste booklet calculation failed.' + str(e)

    if not error:
        try:
            calculation_booklet['orderweight_kg'] = calculation_booklet.apply(
                lambda row: orderweight_kg_brochures_calculation(True, selfcover, rfq, number_of_pages),
                axis=1)
            calculation_booklet['orderweight_kg1000extra'] = calculation_booklet.apply(
                lambda row: orderweight_kg_brochures_calculation(False, selfcover, rfq, number_of_pages),
                axis=1)
        except Exception as e:
            error = 'Orderweight calculation brochures failed.' + str(e)

    if not error:
        try:
            calculation_booklet['book_thickness'] = book_thickness
            calculation_booklet['packagingcost'] = calculation_booklet.apply(
                lambda row: packaging_cost_calculation(True, rfq, packagingoption_id, producer_id,
                                                       row['orderweight_kg']), axis=1)

            calculation_booklet['packagingcost1000extra'] = calculation_booklet.apply(
                lambda row: packaging_cost_calculation(False, rfq, packagingoption_id, producer_id,
                                                       row['orderweight_kg'], ), axis=1)

        except Exception as e:
            error = 'Packaging calculation failed. Update settings' + str(e)

    if not error:
        try:
            calculation_booklet['transportcost'] = calculation_booklet.apply(
                lambda row: transport_costs_calculation(True, rfq, transportoption_id, producer_id,
                                                        row['orderweight_kg']), axis=1)

            calculation_booklet['transportcost1000extra'] = calculation_booklet.apply(
                lambda row: transport_costs_calculation(False, rfq, transportoption_id, producer_id,
                                                        row['orderweight_kg']), axis=1)

        except Exception as e:
            error = 'Transport calculation failed.' + str(e)

    if not error:
        try:
            calculation_booklet['paper_quantity_booklet'] = calculation_booklet['net_paper_quantity_booklet'] + \
                                                            calculation_booklet['waste_printing'] + \
                                                            calculation_booklet['waste_folding'] + \
                                                            calculation_booklet['waste_binding']
            calculation_booklet['paper_quantity_booklet1000extra'] = calculation_booklet[
                                                                         'net_paper_quantity_booklet1000extra'] + \
                                                                     calculation_booklet[
                                                                         'waste_printing1000extra'] + \
                                                                     calculation_booklet[
                                                                         'waste_folding1000extra'] + \
                                                                     calculation_booklet[
                                                                         'waste_binding1000extra']
        except Exception as e:
            error = 'Paper quantity booklet calculation failed.' + str(e)

    # calculate printingcost booklet
    if not error:
        try:
            calculation_booklet['printing_starttime_booklet'] = calculation_booklet.apply(
                lambda row: printing_booklet_starttime_calculation(row['printer_id'],
                                                                   row['number_of_printruns_booklet'], rfq),
                axis=1)

            calculation_booklet['printing_runtime_booklet'] = calculation_booklet.apply(
                lambda row: printing_booklet_runtime_calculation(row['printer_id'],
                                                                 row['paper_quantity_booklet'], rfq),
                axis=1)

            calculation_booklet['printing_runtime_booklet1000extra'] = calculation_booklet.apply(
                lambda row: printing_booklet_runtime_calculation(row['printer_id'],
                                                                 row['paper_quantity_booklet1000extra'], rfq),
                axis=1)

            calculation_booklet['printingcost_booklet'] = calculation_booklet.apply(
                lambda row: printingcost_calculation(True, rfq.volume, row['tariff_eur_hour'],
                                                     row['printing_starttime_booklet'],
                                                     row['printing_runtime_booklet'], ),
                axis=1)

            calculation_booklet['printingcost_booklet1000extra'] = calculation_booklet.apply(
                lambda row: printingcost_calculation(False, rfq.volume, row['tariff_eur_hour'], 0,
                                                     row['printing_runtime_booklet']),
                axis=1)

        except Exception as e:
            error = 'Printingcost calculation for booklet failed.' + str(e)

    # inkcost booklet calculation
    if not error:
        try:
            calculation_booklet['inkcost_booklet'] = calculation_booklet.apply(
                lambda row: inkcost_booklet_calculation(True, rfq, row['printer_id'], row['paper_quantity_booklet'],
                                                        ), axis=1)
            calculation_booklet['inkcost_booklet1000extra'] = calculation_booklet.apply(
                lambda row: inkcost_booklet_calculation(False, rfq, row['printer_id'],
                                                        row['paper_quantity_booklet1000extra'],
                                                        ), axis=1)
        except Exception as e:
            error = 'Booklet inkcost calculation failed.' + str(e)

    # papercost booklet calculation
    if not error:
        try:
            calculation_booklet['paperprice_1000sheets_booklet'] = calculation_booklet.apply(
                lambda row: paperprice_1000sheets_calculation(producer_id, row['paperspec_id_booklet']
                                                              ), axis=1)

            calculation_booklet['papercost_booklet'] = calculation_booklet.apply(
                lambda row: papercost_calculation(row['paper_quantity_booklet'],
                                                  row['paperprice_1000sheets_booklet']
                                                  ), axis=1)

            calculation_booklet['paper_booklet_added value'] = calculation_booklet.apply(
                lambda row: paper_added_value_calculation(purchase_paper_perc_added, row['papercost_booklet']), axis=1)

            calculation_booklet['papercost_booklet_total'] = calculation_booklet['papercost_booklet'] + \
                                                             calculation_booklet['paper_booklet_added value']

            calculation_booklet['papercost_booklet1000extra'] = calculation_booklet.apply(
                lambda row: papercost_calculation(row['paper_quantity_booklet1000extra'],
                                                  row['paperprice_1000sheets_booklet']), axis=1)

            calculation_booklet['paper_booklet_added value1000extra'] = calculation_booklet.apply(
                lambda row: paper_added_value_calculation(purchase_paper_perc_added, row['papercost_booklet1000extra']),
                axis=1)

            calculation_booklet['papercost_booklet_total1000extra'] = calculation_booklet[
                                                                          'papercost_booklet1000extra'] + \
                                                                      calculation_booklet[
                                                                          'paper_booklet_added value1000extra']

        except Exception as e:
            error = 'Papercost calculation failed.' + str(e)

    # Calculate and insert calculation cover --------------------------------------------------------------------------
    calculation_cover = []
    if not error and not selfcover:
        try:
            calculation_cover = brochure_cover_calculation(producer_id, rfq, book_thickness, portrait_landscape)
            calculation_booklet = pd.merge(calculation_booklet, calculation_cover[0], on='producer_id')
            error = calculation_cover[1]

        except Exception as e:
            error = 'Cover calculation failed.' + str(calculation_cover[1]) + str(e)

    if not selfcover and not error:
        try:
            calculation_booklet['waste_binding_cover'] = calculation_booklet.apply(
                lambda row: bindingwaste_cover_calculation(True, rfq, row['bindingmachine_id'],
                                                           row['items_per_sheet_cover']),
                axis=1)

            calculation_booklet['waste_binding_cover1000extra'] = calculation_booklet.apply(
                lambda row: bindingwaste_cover_calculation(False, rfq, row['bindingmachine_id'],
                                                           row['items_per_sheet_cover']),
                axis=1)

        except Exception as e:
            error = 'Bindingwaste cover calculation failed.' + str(e)

    if not selfcover and not error:
        try:
            calculation_booklet['paper_quantity_cover'] = calculation_booklet[
                                                              'paper_quantity_cover'] + \
                                                          calculation_booklet['waste_binding_cover']
            calculation_booklet['paper_quantity_cover1000extra'] = calculation_booklet[
                                                                       'paper_quantity_cover1000extra'] + \
                                                                   calculation_booklet['waste_binding_cover1000extra']
        except Exception as e:
            error = 'paper_quantity_complete_cover failed.' + str(e)

        # Papercost cover calculation

        if not selfcover and not error:
            try:
                calculation_booklet['paperprice_1000sheets_cover'] = calculation_booklet.apply(
                    lambda row: paperprice_1000sheets_calculation(producer_id, row['paperspec_id_cover']), axis=1)

                calculation_booklet['papercost_cover'] = calculation_booklet.apply(
                    lambda row: papercost_calculation(row['paper_quantity_cover'],
                                                      row['paperprice_1000sheets_cover'], ),
                    axis=1)

                calculation_booklet['papercost_cover1000extra'] = calculation_booklet.apply(
                    lambda row: papercost_calculation(row['paper_quantity_cover1000extra'],
                                                      row['paperprice_1000sheets_cover']
                                                      ), axis=1)
            except Exception as e:
                error = 'Cover papercostcalculation failed.' + str(e)

    # added value calculation
    if not error:
        if selfcover:
            empty_cols = ['paper_cover_added value', 'papercost_cover_total', 'perc_added_value_cover',
                          'paper_cover_added_value1000extra', 'papercost_cover_total1000extra', 'papercost_cover',
                          'inkcost_cover', 'purchase_plates_cover', 'paperspec_id_cover', 'enhancecost_cover',
                          'papercost_cover1000extra', 'enhancecost_cover1000extra', 'printer_cover',
                          'waste_printing_cover', 'waste_printing_cover1000extra', 'waste_binding_cover',
                          'waste_binding_cover1000extra', 'printingcost_cover', 'printingcost_cover1000extra',
                          'inkcost_cover1000extra', 'margin_plates_cover', 'platecost_cover',
                          'net_paper_quantity_cover', 'net_paper_quantity_cover1000extra',
                          'paper_quantity_cover', 'paper_quantity_cover1000extra', 'number_of_printruns_cover',
                          'cuttingcost_cover', 'cuttingcost_cover1000extra'
                          ]
            for col in empty_cols:
                calculation_booklet.insert(2, col, 0.0)

            error = []
        else:
            try:

                calculation_booklet['paper_cover_added value'] = calculation_booklet.apply(
                    lambda row: paper_added_value_calculation(purchase_paper_perc_added, row['papercost_cover']),
                    axis=1)

                calculation_booklet['papercost_cover_total'] = calculation_booklet['papercost_cover'] + \
                                                               calculation_booklet['paper_cover_added value']

                calculation_booklet['perc_added_value_cover'] = (calculation_booklet['papercost_cover_total'] -
                                                                 calculation_booklet[
                                                                     'papercost_cover']) / calculation_booklet[
                                                                    'papercost_cover_total']

                calculation_booklet['paper_cover_added_value1000extra'] = calculation_booklet.apply(
                    lambda row: paper_added_value_calculation(purchase_paper_perc_added,
                                                              row['papercost_cover1000extra']),
                    axis=1)

                calculation_booklet['papercost_cover_total1000extra'] = calculation_booklet[
                                                                            'papercost_cover1000extra'] + \
                                                                        calculation_booklet[
                                                                            'paper_cover_added_value1000extra']

            except Exception as e:
                error = 'Cover paper calculation failed.' + str(e)

    if not error:
        try:
            if selfcover:
                calculation_booklet['cover_totalcost'] = 0
                calculation_booklet['cover_totalcost1000extra'] = 0
            else:
                calculation_booklet['cover_totalcost'] = calculation_booklet['cover_subtotal_cost'] + \
                                                         calculation_booklet['papercost_cover_total']
                calculation_booklet['cover_totalcost1000extra'] = calculation_booklet['cover_subtotal_cost1000extra'] + \
                                                                  calculation_booklet['papercost_cover_total1000extra']
        except Exception as e:
            error = 'Cover totalcost calculation failed.' + str(calculation_cover[1]) + str(e)

    if not error:
        try:
            calculation_booklet['total_cost'] = (
                    calculation_booklet['order_startcost'] +
                    calculation_booklet['platecost_booklet'] +
                    calculation_booklet['inkcost_booklet'] +
                    calculation_booklet['printingcost_booklet'] +
                    calculation_booklet['cuttingcost_booklet'] +
                    calculation_booklet['foldingcost_booklet'] +
                    calculation_booklet['bindingcost'] +
                    calculation_booklet['papercost_booklet_total'] +
                    calculation_booklet['packagingcost'] +
                    calculation_booklet['transportcost'] +
                    calculation_booklet['cover_totalcost'])

            calculation_booklet['total_cost1000extra'] = (
                    calculation_booklet['inkcost_booklet1000extra'] +
                    calculation_booklet['printingcost_booklet1000extra'] +
                    calculation_booklet['cuttingcost_booklet1000extra'] +
                    calculation_booklet['foldingcost_booklet1000extra'] +
                    calculation_booklet['bindingcost1000extra'] +
                    calculation_booklet['papercost_booklet_total1000extra'] +
                    calculation_booklet['packagingcost1000extra'] +
                    calculation_booklet['transportcost1000extra'] +
                    calculation_booklet['cover_totalcost1000extra'])

        except Exception as e:
            error = 'Brochure total cost calculation failed' + str(e)

    if not error:
        try:
            calculation_booklet['added_value'] = calculation_booklet.apply(
                lambda row: added_value_brochure_calculation(selfcover, producer_id, row['total_cost'],
                                                             row['papercost_booklet'], row['papercost_cover'],
                                                             row['foldingmachine_id'], row['foldingcost_booklet'],
                                                             row['bindingmachine_id'], row['bindingcost'],
                                                             row['inkcost_booklet'], row['inkcost_cover'],
                                                             row['purchase_plates_booklet'],
                                                             row['purchase_plates_cover'], rfq,
                                                             row['paperspec_id_cover'],
                                                             row['enhancecost_cover']), axis=1)

            calculation_booklet['perc_added_value'] = calculation_booklet.apply(
                lambda row: perc_added_value_calculation(row['total_cost'], row['added_value'], ), axis=1)

            calculation_booklet['purchase_paper_perc_added'] = purchase_paper_perc_added

            calculation_booklet['added_value1000extra'] = calculation_booklet.apply(
                lambda row: added_value_brochure_calculation(selfcover, producer_id, row['total_cost1000extra'],
                                                             row['papercost_booklet1000extra'],
                                                             row['papercost_cover1000extra'],
                                                             row['foldingmachine_id'],
                                                             row['foldingcost_booklet1000extra'],
                                                             row['bindingmachine_id'], row['bindingcost1000extra'],
                                                             0, 0, 0, 0,
                                                             rfq,
                                                             row['paperspec_id_cover'],
                                                             row['enhancecost_cover1000extra']), axis=1)

            calculation_booklet['perc_added_value1000extra'] = calculation_booklet.apply(
                lambda row: perc_added_value_calculation(row['total_cost1000extra'], row['added_value1000extra'], ),
                axis=1)
        except Exception as e:
            error = 'Brochure added value calculation failed' + str(e)

    if not error:
        try:
            calculation_booklet['memberdiscount'] = calculation_booklet.apply(
                lambda row: clientrelated_sales_allowance_calculation(rfq, producer_id,
                                                                      row['perc_added_value'],
                                                                      row['total_cost']), axis=1)

            calculation_booklet['memberdiscount1000extra'] = calculation_booklet.apply(
                lambda row: clientrelated_sales_allowance_calculation(rfq, producer_id,
                                                                      row['perc_added_value1000extra'],
                                                                      row['total_cost1000extra']),
                axis=1)

        except Exception as e:
            error = 'Brochure total client discount calculation failed' + str(e)

    if not error:
        try:

            calculation_booklet['offer_value'] = calculation_booklet['total_cost'] - calculation_booklet[
                'memberdiscount']

            calculation_booklet['offer_value1000extra'] = calculation_booklet['total_cost1000extra'] - \
                                                          calculation_booklet[
                                                              'memberdiscount1000extra']
        except Exception as e:
            error = 'Brochure calculation not completed.' + str(e)

    #  Save best offer---------------------------------------------------------------------------------------------
    best_offer = []
    if not error:
        try:
            best_offer_cost = min(calculation_booklet['total_cost'])
            best_offer = calculation_booklet[calculation_booklet.total_cost == best_offer_cost]

            not_used_columns = ['printer', 'cuttingmachine', 'foldingmachine', 'paperspec_id', 'printingcost',
                                'printingcost1000extra', 'inkcost', 'inkcost1000extra', 'foldingcost',
                                'foldingcost1000extra', 'cuttingcost', 'cuttingcost1000extra',
                                'enhancecost', 'enhancecost1000extra', 'purchase_plates', 'margin_plates',
                                'platecost',
                                'papercost_total', 'papercost_total1000extra',
                                'net_paper_quantity', 'net_paper_quantity1000extra', 'paper_quantity',
                                'paper_quantity1000extra']
            for col in not_used_columns:
                best_offer.insert(2, col, 0.0)
        except Exception as e:
            error = 'Offer value calculation failed.' + str(e)

    # save calculation
    save_calculation(rfq, best_offer, error)
