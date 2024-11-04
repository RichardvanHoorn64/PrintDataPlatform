# Functies voor het uitvoeren van offset calculaties
import pandas as pd
from materials.models import *
from methods.models import FoldingMethods
from assets.models import *


def define_folderspecs(rfq):
    foldingmethod = FoldingMethods.objects.get(foldingmethod_id=rfq.folding)
    number_of_stations = foldingmethod.foldingmachine_number_of_stations
    number_of_pages = foldingmethod.number_of_pages

    gross_height = 0
    gross_width = 0

    if rfq.portrait_landscape in [1, 3]:  # 'staand vierkant':
        gross_width = rfq.width_mm_product * foldingmethod.width_factor
        gross_height = rfq.height_mm_product * foldingmethod.height_factor

    if rfq.portrait_landscape == 2:  # 'liggend':
        gross_width = rfq.width_mm_product * foldingmethod.height_factor
        gross_height = rfq.height_mm_product * foldingmethod.width_factor

    return gross_height, gross_width, number_of_stations, number_of_pages


def define_foldingmachine(number_of_stations, producer_id, planoproduct_width_mm, planoproduct_height_mm):
    foldingmachines_fit = pd.DataFrame(Foldingmachines.objects.filter(
        producer_id=producer_id,
        foldingtype_id=2,
        max_number_stations__gte=number_of_stations,
        max_paperheight_mm__gte=planoproduct_height_mm,
        max_paperwidth_mm__gte=planoproduct_width_mm
    ).values())

    foldingmachines_fit['cost_per_folder'] = foldingmachines_fit.tariff_eur_hour / foldingmachines_fit.sheet_per_hour
    foldingmachine_id = \
        foldingmachines_fit[foldingmachines_fit.cost_per_folder == min(foldingmachines_fit.cost_per_folder)][
            'foldingmachine_id'].iloc[0]
    return foldingmachine_id


def foldingcost_calculation(set_up, rfq, foldingmachine_number_of_stations, paperspec_id, foldingmachine_id):
    foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id)
    paper = PaperCatalog.objects.get(paperspec_id=paperspec_id)
    volume = 1000
    set_up_time = float(0.0)
    speedfactor_heavy_paper = float(1 + (foldingmachine.speedreduction_heavy_paper_perc / 100))
    speedfactor_light_paper = float(1 + (foldingmachine.speedreduction_light_paper_perc / 100))

    if set_up:
        volume = rfq.volume
        set_up_time = float(foldingmachine.setup_time_min) + (
                float(foldingmachine_number_of_stations) * float(foldingmachine.setup_time_per_station_min))

    run_time = float(volume / foldingmachine.sheet_per_hour)

    if paper.paperweight_m2 <= foldingmachine.weight_light_paper:
        run_time = run_time * speedfactor_light_paper
    if paper.paperweight_m2 >= foldingmachine.weight_heavy_paper:
        run_time = run_time * speedfactor_heavy_paper
    if rfq.enhance_front > 0 or rfq.enhance_back > 0:
        run_time = run_time * speedfactor_heavy_paper
    foldingcost = (set_up_time + run_time) * float(foldingmachine.tariff_eur_hour / 60)
    return foldingcost


def foldingwaste_calculation(set_up, rfq, foldingmachine_id):
    foldingmachine = Foldingmachines.objects.get(foldingmachine_id=foldingmachine_id)

    paperwaste_start = 0.0
    volume = 1000

    if set_up:
        paperwaste_start = foldingmachine.paperwaste_start
        volume = rfq.volume

    run_waste = float(volume) * float(foldingmachine.paperwaste_1000sheet_perc) * .01

    foldingwaste = paperwaste_start + run_waste
    return foldingwaste
