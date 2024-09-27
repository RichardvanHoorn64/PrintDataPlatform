import pandas as pd
from django.utils import timezone
from decimal import Decimal
from calculations.models import Calculations


def save_calculation(producer_id, rfq, best_offer, error):
    calculation = Calculations.objects.get(printproject_id=rfq.printproject_id, producer_id=producer_id)

    if not error:
        try:
            calculation.status = 'calculated'
            calculation.error = None
            calculation.printer = best_offer['printer'].values[0]
            calculation.printer_booklet = best_offer['printer_booklet'].values[0]
            calculation.printer_cover = best_offer['printer_cover'].values[0]
            calculation.cuttingmachine = best_offer['cuttingmachine']
            calculation.cuttingmachine_booklet = best_offer['cuttingmachine_booklet']
            calculation.foldingmachine = best_offer['foldingmachine'].values[0]
            calculation.foldingmachines_booklet = best_offer['foldingmachines_booklet'].values[0]
            calculation.bindingmachine = best_offer['bindingmachine'].values[0]
            calculation.paperspec_id = pd.to_numeric(best_offer['paperspec_id'].values[0])
            calculation.paperspec_id_booklet = pd.to_numeric(best_offer['paperspec_id_booklet'].values[0])
            calculation.paperspec_id_cover = pd.to_numeric(best_offer['paperspec_id_cover'].values[0])
            calculation.purchase_paper_perc_added = pd.to_numeric(best_offer['purchase_paper_perc_added'].values[0])
            calculation.pages_per_sheet_booklet = pd.to_numeric(best_offer['pages_per_sheet_booklet'].values[0])
            calculation.pages_per_katern_booklet = pd.to_numeric(best_offer['pages_per_katern_booklet'].values[0])
            calculation.number_of_printruns_booklet = pd.to_numeric(best_offer['number_of_printruns_booklet'].values[0])
            calculation.book_thickness = best_offer['book_thickness'].values[0]
            calculation.waste_printing = pd.to_numeric(best_offer['waste_printing'].values[0])
            calculation.waste_printing1000extra = pd.to_numeric(best_offer['waste_printing1000extra'].values[0])
            calculation.waste_folding = pd.to_numeric(best_offer['waste_folding'].values[0])
            calculation.waste_folding1000extra = pd.to_numeric(best_offer['waste_folding1000extra'].values[0])
            calculation.waste_binding = pd.to_numeric(best_offer['waste_binding'].values[0])
            calculation.waste_binding1000extra = pd.to_numeric(best_offer['waste_binding1000extra'].values[0])
            calculation.waste_printing_cover = pd.to_numeric(best_offer['waste_printing_cover'].values[0])
            calculation.waste_printing_cover1000extra = pd.to_numeric(
                best_offer['waste_printing_cover1000extra'].values[0])
            calculation.waste_binding_cover = pd.to_numeric(best_offer['waste_binding_cover'].values[0])
            calculation.waste_binding_cover1000extra = pd.to_numeric(
                best_offer['waste_binding_cover1000extra'].values[0])

            calculation.order_startcost = Decimal(best_offer['order_startcost'].values[0])
            calculation.printingcost = Decimal(best_offer['printingcost'].values[0])
            calculation.printingcost_booklet = pd.to_numeric(best_offer['printingcost_booklet'].values[0])
            calculation.printingcost_cover = Decimal(best_offer['printingcost_cover'].values[0])
            calculation.printingcost1000extra = Decimal(best_offer['printingcost1000extra'].values[0])
            calculation.printingcost_booklet1000extra = Decimal(
                best_offer['printingcost_booklet1000extra'].values[0])
            calculation.printingcost_cover1000extra = Decimal(best_offer['printingcost_cover1000extra'].values[0])
            calculation.inkcost = Decimal(best_offer['inkcost'].values[0])
            calculation.inkcost1000extra = Decimal(best_offer['inkcost1000extra'].values[0])
            calculation.inkcost_cover = Decimal(best_offer['inkcost_cover'].values[0])
            calculation.inkcost_cover1000extra = Decimal(best_offer['inkcost_cover1000extra'].values[0])
            calculation.inkcost_booklet = Decimal(best_offer['inkcost_booklet'].values[0])
            calculation.inkcost_booklet1000extra = Decimal(best_offer['inkcost_booklet1000extra'].values[0])

            calculation.foldingcost = Decimal(best_offer['foldingcost'].values[0])
            calculation.foldingcost1000extra = Decimal(best_offer['foldingcost1000extra'].values[0])
            calculation.foldingcost_booklet = Decimal(best_offer['foldingcost_booklet'].values[0])
            calculation.foldingcost_booklet1000extra = Decimal(best_offer['foldingcost_booklet1000extra'].values[0])

            calculation.bindingcost = Decimal(best_offer['bindingcost'].values[0])
            calculation.bindingcost1000extra = Decimal(best_offer['bindingcost1000extra'].values[0])

            calculation.enhancecost = Decimal(best_offer['enhancecost'].values[0])
            calculation.enhancecost1000extra = Decimal(best_offer['enhancecost1000extra'].values[0])
            calculation.enhancecost_cover = Decimal(best_offer['enhancecost_cover'].values[0])
            calculation.enhancecost_cover1000extra = Decimal(best_offer['enhancecost_cover1000extra'].values[0])

            calculation.purchase_plates = Decimal(best_offer['purchase_plates'].values[0])
            calculation.margin_plates = Decimal(best_offer['margin_plates'].values[0])
            calculation.platecost = Decimal(best_offer['platecost'].values[0])
            calculation.purchase_plates_booklet = Decimal(best_offer['purchase_plates_booklet'].values[0])
            calculation.margin_plates_booklet = Decimal(best_offer['margin_plates_booklet'].values[0])
            calculation.platecost_booklet = Decimal(best_offer['platecost_booklet'].values[0])
            calculation.purchase_plates_cover = Decimal(best_offer['purchase_plates_cover'].values[0])
            calculation.margin_plates_cover = Decimal(best_offer['margin_plates_cover'].values[0])
            calculation.platecost_cover = Decimal(best_offer['platecost_cover'].values[0])

            calculation.papercost_total = Decimal(best_offer['papercost_total'].values[0])
            calculation.papercost_total1000extra = Decimal(best_offer['papercost_total1000extra'].values[0])
            calculation.papercost_booklet_total = Decimal(best_offer['papercost_booklet_total'].values[0])
            calculation.papercost_booklet_total1000extra = Decimal(
                best_offer['papercost_booklet_total1000extra'].values[0])
            calculation.papercost_cover_total = Decimal(best_offer['papercost_cover_total'].values[0])
            calculation.papercost_cover_total1000extra = Decimal(best_offer['papercost_cover_total1000extra'].values[0])

            calculation.net_paper_quantity = pd.to_numeric(best_offer['net_paper_quantity'].values[0])
            calculation.net_paper_quantity1000extra = pd.to_numeric(best_offer['net_paper_quantity1000extra'].values[0])
            calculation.net_paper_quantity_booklet = pd.to_numeric(best_offer['net_paper_quantity_booklet'].values[0])
            calculation.net_paper_quantity_booklet1000extra = pd.to_numeric(
                best_offer['net_paper_quantity_booklet1000extra'].values[0])
            calculation.net_paper_quantity_cover = pd.to_numeric(best_offer['net_paper_quantity_cover'].values[0])
            calculation.net_paper_quantity_cover1000extra = pd.to_numeric(
                best_offer['net_paper_quantity_cover1000extra'].values[0])

            calculation.number_of_printruns_cover = pd.to_numeric(best_offer['number_of_printruns_cover'].values[0])

            calculation.packagingcost = Decimal(best_offer['packagingcost'].values[0])
            calculation.packagingcost1000extra = Decimal(best_offer['packagingcost1000extra'].values[0])

            calculation.orderweight_kg = Decimal(best_offer['orderweight_kg'].values[0])
            calculation.orderweight_kg1000extra = Decimal(best_offer['orderweight_kg1000extra'].values[0])
            calculation.transportcost = Decimal(best_offer['transportcost'].values[0])
            calculation.transportcost1000extra = Decimal(best_offer['transportcost1000extra'].values[0])

            calculation.cuttingcost = Decimal(best_offer['cuttingcost'].values[0])
            calculation.cuttingcost1000extra = Decimal(best_offer['cuttingcost1000extra'].values[0])
            calculation.cuttingcost_booklet = Decimal(best_offer['cuttingcost_booklet'].values[0])
            calculation.cuttingcost_booklet1000extra = Decimal(
                best_offer['cuttingcost_booklet1000extra'].values[0])
            calculation.cuttingcost_cover = Decimal(best_offer['cuttingcost_cover'].values[0])
            calculation.cuttingcost_cover1000extra = Decimal(
                best_offer['cuttingcost_cover1000extra'].values[0])

            calculation.paper_quantity = pd.to_numeric(best_offer['paper_quantity'].values[0])
            calculation.paper_quantity1000extra = pd.to_numeric(best_offer['paper_quantity1000extra'].values[0])
            calculation.paper_quantity_booklet = pd.to_numeric(best_offer['paper_quantity_booklet'].values[0])
            calculation.paper_quantity_booklet1000extra = pd.to_numeric(
                best_offer['paper_quantity_booklet1000extra'].values[0])
            calculation.paper_quantity_cover = pd.to_numeric(best_offer['paper_quantity_cover'].values[0])
            calculation.paper_quantity_cover1000extra = pd.to_numeric(
                best_offer['paper_quantity_cover1000extra'].values[0])

            calculation.transportationcost = Decimal(best_offer['transportcost'].values[0])
            calculation.transportationcost1000extra = Decimal(best_offer['transportcost1000extra'].values[0])

            calculation.total_cost = Decimal(best_offer['total_cost'].values[0])
            calculation.total_cost1000extra = Decimal(best_offer['total_cost1000extra'].values[0])
            calculation.added_value = Decimal(best_offer['added_value'].values[0])
            calculation.perc_added_value = Decimal(best_offer['perc_added_value'].values[0])
            calculation.added_value1000extra = Decimal(best_offer['added_value1000extra'].values[0])
            calculation.perc_added_value1000extra = Decimal(best_offer['perc_added_value1000extra'].values[0])
            calculation.memberdiscount = Decimal(best_offer['memberdiscount'].values[0])
            calculation.memberdiscount1000extra = Decimal(best_offer['memberdiscount1000extra'].values[0])
            calculation.offer_date = timezone.now().today().date()
            calculation.offer_value = Decimal(best_offer['offer_value'].values[0])
            calculation.offer_value1000extra = Decimal(best_offer['offer_value1000extra'].values[0])

            calculation.save()
        except Exception as e:
            general_error = str(error)
            error = 'General error: ' + general_error + 'Calculation save error'
            calculation.error = error,
            calculation.total_cost = 0
            calculation.total_cost1000extra = 0
            calculation.save()

    else:
        status = 'Calculation failed'
        calculation.status = status
        calculation.offer_date = timezone.now().today().date()
        calculation.error = error
        calculation.total_cost = 0
        calculation.total_cost1000extra = 0
        calculation.save()
