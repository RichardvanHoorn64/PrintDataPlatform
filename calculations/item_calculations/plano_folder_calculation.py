from calculations.functions.function_save_calculation import save_calculation
from calculations.functions.functions_folders import *
from calculations.functions.functions_general import *


def plano_folder_calculation(user, rfq):
    error = []
    calculation_plano = []
    producer_id = user.producer_id
    planoproduct_height_mm = rfq.height_mm_product
    planoproduct_width_mm = rfq.width_mm_product
    number_of_pages = 1

    # general settings
    purchase_paper_perc_added = GeneralCalculationSettings.objects.get(
        producer_id=producer_id).purchase_paper_perc_added
    calculationsettings = GeneralCalculationSettings.objects.get(producer_id=producer_id)

    # packaging and transport
    if not error:
        try:
            packagingtariff = PackagingOptions.objects.get(packaging=rfq.packaging)
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

    # Test productsize input
    if not error:
        productsize_check(rfq)

    # Test paper choice availability and define papercatalog
    if not error:
        try:
            paper_fit_for_rfq = paper_available_plano(rfq, producer_id)
        except Exception as e:
            error = 'Paper fit_for rfq plano product not available.' + str(e)

    # define plano product size
    if not error:
        try:
            if rfq.productcategory_id == 2:
                folderspecs = define_folderspecs(rfq)  # Folders
                planoproduct_height_mm = folderspecs[0]
                planoproduct_width_mm = folderspecs[1]
                foldingmachine_number_of_stations = folderspecs[2]
                number_of_pages = folderspecs[3]
        except Exception as e:
            error = 'Folderspecs definitions failed.' + str(e)

        # - Calculation plano product -----------------------------------------------------------------------------------------------
        assets_printers_plano = []

        try:
            assets_printers_plano = pd.DataFrame(Printers.objects.filter(producer_id=producer_id).values())

        except Printers.DoesNotExist:
            error = 'No plano product printer fit for this request.'

        if not error:
            try:
                calculation_plano = pd.DataFrame(
                    assets_printers_plano[(assets_printers_plano.printsize_width >= planoproduct_width_mm)
                                          & (assets_printers_plano.printsize_height >= planoproduct_height_mm)
                                          ])
                calculation_plano['printer'] = calculation_plano['asset_name']
            except Exception as e:
                error = 'No plano product printers fit for plano product:' + str(e)

        # PAPER CALCULATION
        # select paperspec_id fit for printer plano product
        if not error:
            try:
                calculation_plano['paperspec_id'] = calculation_plano.apply(
                    lambda row: paperidselector(row['printer_id'], paper_fit_for_rfq,
                                                planoproduct_height_mm,
                                                planoproduct_width_mm), axis=1)

            except Exception as e:
                error = 'No paperspec_id for requested plano product availeble.' + str(e)

        if not error and len(calculation_plano) == 0:
            error = 'Paperbrand plano product not availeble.'

        # Define number of colors plano product, per printer, pressvarnish
        if not error:
            try:
                calculation_plano['number_of_colors_front'] = calculation_plano.apply(
                    lambda row: calculate_number_of_colors_front(rfq, row['varnish_unit']), axis=1)
                calculation_plano['number_of_colors_rear'] = calculation_plano.apply(
                    lambda row: calculate_number_of_colors_rear(rfq, row['varnish_unit']), axis=1)
            except Exception as e:
                error = 'Calculation number of colors plano product failed.' + str(e)

        if not error:
            try:
                calculation_plano['items_per_sheet'] = calculation_plano.apply(
                    lambda row: items_per_sheet_calculation(row['paperspec_id'], planoproduct_height_mm,
                                                            planoproduct_width_mm),
                    axis=1)
            except Exception as e:
                error = 'items per_sheet calculation failed.' + str(e)

        # calculate paper_width height plano product
        if not error:
            try:
                calculation_plano['paper_width_plano'] = calculation_plano.apply(
                    lambda row: find_paper_width(row['paperspec_id'], ), axis=1)

                calculation_plano['paper_height_plano'] = calculation_plano.apply(
                    lambda row: find_paper_height(row['paperspec_id'], ), axis=1)

            except Exception as e:
                error = 'Papersizes plano product runs not defined.' + str(e)

        if not error:
            try:

                calculation_plano['number_of_printruns'] = calculation_plano.apply(
                    lambda row: number_of_printruns_calculation(rfq.printsided, row['printer_id']), axis=1)
            except Exception as e:
                error = 'Number of_printruns plano product not defined.' + str(e)

        # calculate platecost plano product
        if not error:
            try:
                calculation_plano['purchase_plates'] = calculation_plano.apply(
                    lambda row: purchase_plates_calculation(rfq, row['printer_id'], row['items_per_sheet'],
                                                            row['number_of_printruns']), axis=1)
                calculation_plano['margin_plates'] = calculation_plano.apply(
                    lambda row: margin_plates_calculation(rfq, row['printer_id'], row['items_per_sheet'],
                                                          row['number_of_printruns']), axis=1)
                calculation_plano['platecost'] = calculation_plano['purchase_plates'] + \
                                                 calculation_plano['margin_plates']
            except Exception as e:
                error = 'Calculation platecost plano product failed.' + str(e)

        # calculate printingwaste plano product
        if not error:
            try:

                calculation_plano['waste_printing'] = calculation_plano.apply(
                    lambda row: printingwaste_calculation(True, rfq, row['printer_id'],
                                                          rfq.printsided, row['items_per_sheet']),
                    axis=1)

                calculation_plano['waste_printing1000extra'] = calculation_plano.apply(
                    lambda row: printingwaste_calculation(False, rfq, row['printer_id'],
                                                          rfq.printsided, row['items_per_sheet']),
                    axis=1)

            except Exception as e:
                error = 'No printingwaste calculation for plano product.' + str(e)

        if not error:
            try:
                calculation_plano['net_paper_quantity'] = calculation_plano.apply(
                    lambda row: net_paper_quantity_calculation(rfq.volume, row['items_per_sheet'], ),
                    axis=1)
                calculation_plano['net_paper_quantity1000extra'] = calculation_plano.apply(
                    lambda row: net_paper_quantity_calculation(1000, row['items_per_sheet'], ),
                    axis=1)

            except Exception as e:
                error = 'net paper quantity calculation plano product failed.' + str(e)

        if not error:
            try:
                calculation_plano['paper_quantity'] = calculation_plano[
                                                          'net_paper_quantity'] + \
                                                      calculation_plano['waste_printing']
                calculation_plano['paper_quantity1000extra'] = calculation_plano[
                                                                   'net_paper_quantity1000extra'] + \
                                                               calculation_plano['waste_printing1000extra']
            except Exception as e:
                error = 'net_paper_quantity_complete_plano failed.' + str(e)

        # plano product cutting
        if not error:
            try:
                calculation_plano['cuttingmachine'] = calculation_plano.apply(
                    lambda row: definecuttingmachine(producer_id, row['paperspec_id'], ), axis=1)
                calculation_plano = calculation_plano[calculation_plano['cuttingmachine'] != 0]
            except Exception as e:
                error = 'No cuttingmachine for plano product availeble.' + str(e)

        if not error:
            try:
                calculation_plano['cuttingcost'] = calculation_plano.apply(
                    lambda row: cuttingcostcalculation(True, rfq, row['cuttingmachine'],
                                                       row['paperspec_id'],
                                                       row['items_per_sheet']),
                    axis=1)
                calculation_plano['cuttingcost1000extra'] = calculation_plano.apply(
                    lambda row: cuttingcostcalculation(False, rfq, row['cuttingmachine'],
                                                       row['paperspec_id'],
                                                       row['items_per_sheet']),
                    axis=1)

            except Exception as e:
                error = 'Cutting plano product calculation failed.' + str(e)

            try:
                calculation_plano['enhancecost'] = calculation_plano.apply(
                    lambda row: enhancement_cost_calculation(True, rfq, producer_id, row['paper_quantity'],
                                                             row['paperspec_id'], row['items_per_sheet']),
                    axis=1)
                calculation_plano['enhancecost1000extra'] = calculation_plano.apply(
                    lambda row: enhancement_cost_calculation(False, rfq, producer_id, row['paper_quantity'],
                                                             row['paperspec_id'],
                                                             row['items_per_sheet']),
                    axis=1)

            except Exception as e:
                error = 'Enhancement cost calculation plano product failed.' + str(e)

        if not error:
            try:
                calculation_plano['printing_starttime'] = calculation_plano.apply(
                    lambda row: printing_starttime_calculation(rfq, row['printer_id'],
                                                               row['items_per_sheet']),
                    axis=1)
                # printing_runtime_calculation(rfq, printer_id, paper_quantity, items_per_sheet):
                calculation_plano['printing_runtime'] = calculation_plano.apply(
                    lambda row: printing_runtime_calculation(rfq, row['printer_id'], row['paper_quantity'],
                                                             rfq.paperweight),
                    axis=1)

                calculation_plano['printing_runtime1000extra'] = calculation_plano.apply(
                    lambda row: printing_runtime_calculation(rfq, row['printer_id'],
                                                             row['paper_quantity1000extra'],
                                                             rfq.paperweight),
                    axis=1)

                calculation_plano['printingcost'] = calculation_plano.apply(
                    lambda row: printingcost_calculation(True, rfq.volume, row['tariff_eur_hour'],
                                                         row['printing_starttime'],
                                                         row['printing_runtime']),
                    axis=1)

                calculation_plano['printingcost1000extra'] = calculation_plano.apply(
                    lambda row: printingcost_calculation(True, rfq.volume, row['tariff_eur_hour'], 0,
                                                         row['printing_runtime1000extra']), axis=1)

            except Exception as e:
                error = 'Calculation printingcost plano product failed.' + str(e)

        # inkcost plano product calculation
        if not error:
            try:
                calculation_plano['inkcost'] = calculation_plano.apply(
                    lambda row: inkcost_calculation(True, rfq, row['printer_id'], row['paper_quantity'],
                                                    rfq.printsided), axis=1)
                calculation_plano['inkcost1000extra'] = calculation_plano.apply(
                    lambda row: inkcost_calculation(False, rfq, row['printer_id'],
                                                    row['paper_quantity1000extra'],
                                                    rfq.printsided), axis=1)
            except Exception as e:
                error = 'Inkcost calculation plano product failed.' + str(e)

        # folding calculation
        if not error:
            if rfq.productcategory_id == 2:
                calculation_plano['number_of_pages'] = number_of_pages
                try:
                    calculation_plano['foldingmachine'] = calculation_plano.apply(
                        lambda row: define_foldingmachine(foldingmachine_number_of_stations, producer_id,
                                                          planoproduct_width_mm, planoproduct_height_mm), axis=1)
                except Exception as e:
                    error = 'No folding machine fit for this request.' + str(e)
            # foldingcost  calculation
            if not error:
                try:
                    calculation_plano['foldingcost'] = calculation_plano.apply(
                        lambda row: foldingcost_calculation(True, rfq, foldingmachine_number_of_stations,
                                                            row['paperspec_id'], row['foldingmachine']),
                        axis=1)
                    calculation_plano['foldingcost1000extra'] = calculation_plano.apply(
                        lambda row: foldingcost_calculation(False, rfq, foldingmachine_number_of_stations,
                                                            row['paperspec_id'], row['foldingmachine']),
                        axis=1)

                except Exception as e:
                    error = 'Folding cost calculation failed.' + str(e)
            # foldingwaste calculation
            if not error:
                try:
                    calculation_plano['waste_folding'] = calculation_plano.apply(
                        lambda row: foldingwaste_calculation(True, rfq, row['foldingmachine']), axis=1)
                    calculation_plano['waste_folding1000extra'] = calculation_plano.apply(
                        lambda row: foldingwaste_calculation(False, rfq, row['foldingmachine']), axis=1)
                except Exception as e:
                    error = 'Folding waste calculation failed.' + str(e)

        # papercost  calculation
        if not error:
            try:
                calculation_plano['paperprice_1000sheets'] = calculation_plano.apply(
                    lambda row: paperprice_1000sheets_calculation(producer_id, row['paperspec_id']
                                                                  ), axis=1)

                calculation_plano['papercost'] = calculation_plano.apply(
                    lambda row: papercost_calculation(row['paper_quantity'],
                                                      row['paperprice_1000sheets']
                                                      ), axis=1)

                calculation_plano['paper_added value'] = calculation_plano.apply(
                    lambda row: paper_added_value_calculation(purchase_paper_perc_added, row['papercost']),
                    axis=1)

                calculation_plano['papercost_total'] = calculation_plano['papercost'] + \
                                                       calculation_plano['paper_added value']

                calculation_plano['papercost1000extra'] = calculation_plano.apply(
                    lambda row: papercost_calculation(row['paper_quantity1000extra'],
                                                      row['paperprice_1000sheets']), axis=1)

                calculation_plano['paper_added value1000extra'] = calculation_plano.apply(
                    lambda row: paper_added_value_calculation(purchase_paper_perc_added,
                                                              row['papercost1000extra']),
                    axis=1)

                calculation_plano['papercost_total1000extra'] = calculation_plano[
                                                                    'papercost1000extra'] + \
                                                                calculation_plano[
                                                                    'paper_added value1000extra']

            except Exception as e:
                error = 'Papercost calculation failed.' + str(e)

        if not error:
            try:
                calculation_plano['orderweight_kg'] = calculation_plano.apply(
                    lambda row: orderweight_kg_plano_calculation(True, rfq, planoproduct_height_mm,
                                                                 planoproduct_width_mm, row['paperspec_id']),
                    axis=1)
                calculation_plano['orderweight_kg1000extra'] = calculation_plano.apply(
                    lambda row: orderweight_kg_plano_calculation(False, rfq, planoproduct_height_mm,
                                                                 planoproduct_width_mm, row['paperspec_id']),
                    axis=1)
            except Exception as e:
                error = 'Orderweight calculation folders failed.' + str(e)

        if not error:
            try:
                calculation_plano['packagingcost'] = calculation_plano.apply(
                    lambda row: packaging_cost_calculation(True, rfq, packagingoption_id, producer_id,
                                                           row['orderweight_kg']), axis=1)

                calculation_plano['packagingcost1000extra'] = calculation_plano.apply(
                    lambda row: packaging_cost_calculation(False, rfq, packagingoption_id, producer_id,
                                                           row['orderweight_kg'], ), axis=1)

            except Exception as e:
                error = 'Packaging calculation failed.' + str(e)

        if not error:
            try:
                calculation_plano['transportcost'] = calculation_plano.apply(
                    lambda row: transport_costs_calculation(True, rfq, transportoption_id, producer_id,
                                                            row['orderweight_kg']), axis=1)

                calculation_plano['transportcost1000extra'] = calculation_plano.apply(
                    lambda row: transport_costs_calculation(False, rfq, transportoption_id, producer_id,
                                                            row['orderweight_kg']), axis=1)

            except Exception as e:
                error = 'Transport calculation failed.' + str(e)

        if not error:
            try:
                calculation_plano['order_startcost'] = calculate_order_startcost(producer_id)
            except Exception as e:
                error = 'No order_startcost defined:' + str(e)

        if not error:
            try:
                calculation_plano['total_cost'] = (
                        calculation_plano['order_startcost'] +
                        calculation_plano['printingcost'] +
                        calculation_plano['cuttingcost'] +
                        calculation_plano['enhancecost'] +
                        calculation_plano['foldingcost'] +
                        calculation_plano['inkcost'] +
                        calculation_plano['platecost'] +
                        calculation_plano['papercost_total'] +
                        calculation_plano['packagingcost'] +
                        calculation_plano['transportcost']
                )

                calculation_plano['total_cost1000extra'] = (
                        calculation_plano['printingcost1000extra'] +
                        calculation_plano['cuttingcost1000extra'] +
                        calculation_plano['enhancecost1000extra'] +
                        calculation_plano['foldingcost1000extra'] +
                        calculation_plano['inkcost1000extra'] +
                        calculation_plano['papercost_total1000extra'] +
                        calculation_plano['packagingcost1000extra'] +
                        calculation_plano['transportcost1000extra']
                )

            except Exception as e:
                error = "Total cost calculation plano product failed: " + str(error) + str(e)

    if not error:
        try:
            calculation_plano['added_value'] = calculation_plano.apply(
                lambda row: added_value_plano_calculation(producer_id, rfq,
                                                          row['total_cost'], row['papercost'],
                                                          row['foldingmachine'], row['foldingcost'],
                                                          row['inkcost'], row['purchase_plates'],
                                                          row['paperspec_id'], row['enhancecost']), axis=1)

            calculation_plano['added_value1000extra'] = calculation_plano.apply(
                lambda row: added_value_plano_calculation(producer_id, rfq,
                                                          row['total_cost1000extra'], row['papercost1000extra'],
                                                          row['foldingmachine'], row['foldingcost1000extra'],
                                                          row['inkcost1000extra'], 0,
                                                          row['paperspec_id'], row['enhancecost']), axis=1)

            calculation_plano['perc_added_value'] = calculation_plano.apply(
                lambda row: perc_added_value_calculation(row['total_cost'], row['added_value'], ), axis=1)

            calculation_plano['perc_added_value1000extra'] = calculation_plano.apply(
                lambda row: perc_added_value_calculation(row['total_cost1000extra'], row['added_value1000extra'], ),
                axis=1)
            calculation_plano['purchase_paper_perc_added'] = purchase_paper_perc_added

        except Exception as e:
            error = 'Plano added value calculation failed' + str(e)

    if not error:
        try:
            calculation_plano['memberdiscount'] = calculation_plano.apply(
                lambda row: clientrelated_sales_allowance_calculation(rfq, producer_id,
                                                                      row['perc_added_value'],
                                                                      row['total_cost']), axis=1)

            calculation_plano['memberdiscount1000extra'] = calculation_plano.apply(
                lambda row: clientrelated_sales_allowance_calculation(rfq, producer_id,
                                                                      row['perc_added_value1000extra'],
                                                                      row['total_cost1000extra']),
                axis=1)

        except Exception as e:
            error = 'Brochure total client discount calculation failed' + str(e)

    if not error:
        try:

            calculation_plano['offer_value'] = calculation_plano['total_cost'] - calculation_plano[
                'memberdiscount']

            calculation_plano['offer_value1000extra'] = calculation_plano['total_cost1000extra'] - \
                                                        calculation_plano[
                                                            'memberdiscount1000extra']
        except Exception as e:
            error = 'Brochure calculation not completed.' + str(e)

    #  Save best offer---------------------------------------------------------------------------------------------
    best_offer = []
    if not error:
        try:
            best_offer_cost = min(calculation_plano['total_cost'])
            best_offer = calculation_plano[calculation_plano.total_cost == best_offer_cost]

            not_used_columns = ['printer_booklet', 'printer_cover', 'cuttingmachine_booklet', 'foldingmachines_booklet',
                                'bindingmachine', 'paperspec_id_booklet', 'paperspec_id_cover',
                                'pages_per_sheet_booklet', 'pages_per_katern_booklet', 'number_of_printruns_booklet',
                                'book_thickness', 'waste_binding', 'waste_binding1000extra', 'waste_printing_cover',
                                'waste_printing_cover1000extra', 'waste_binding_cover', 'waste_binding_cover1000extra',
                                'printingcost_booklet', 'printingcost_cover', 'printingcost_booklet1000extra',
                                'printingcost_cover1000extra', 'inkcost_cover', 'inkcost_cover1000extra',
                                'inkcost_booklet', 'inkcost_booklet1000extra', 'foldingcost_booklet',
                                'foldingcost_booklet1000extra', 'bindingcost', 'bindingcost1000extra',
                                'enhancecost_cover', 'enhancecost_cover1000extra', 'purchase_plates_booklet',
                                'margin_plates_booklet', 'platecost_booklet', 'purchase_plates_cover',
                                'margin_plates_cover', 'platecost_cover', 'papercost_booklet_total',
                                'papercost_booklet_total1000extra', 'papercost_cover_total',
                                'papercost_cover_total1000extra', 'net_paper_quantity_booklet',
                                'net_paper_quantity_booklet1000extra', 'net_paper_quantity_cover',
                                'net_paper_quantity_cover1000extra', 'paper_quantity_booklet',
                                'paper_quantity_booklet1000extra', 'paper_quantity_cover',
                                'paper_quantity_cover1000extra', 'number_of_printruns_cover', 'cuttingcost_booklet',
                                'cuttingcost_booklet1000extra', 'cuttingcost_cover', 'cuttingcost_cover1000extra']
            for col in not_used_columns:
                best_offer.insert(2, col, 0.0)
        except Exception as e:
            error = 'Offer value calculation failed.' + str(e)

    # save calculation
    save_calculation(rfq, best_offer, error)
