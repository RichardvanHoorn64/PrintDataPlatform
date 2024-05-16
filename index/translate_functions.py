from methods.models import *


def find_enhancement_id(rfq_input):
    try:
        enhancement_id = EnhancementOptions.objects.get(enhancement=rfq_input).enhancement_id
    except EnhancementOptions.DoesNotExist:
        enhancement_id = 0
    return enhancement_id


def find_finishingmethod_id(rfq_input):
    try:
        finishingmethod_id = BrochureFinishingMethods.objects.get(finishingmethod=rfq_input).finishingmethod_id
    except BrochureFinishingMethods.DoesNotExist:
        finishingmethod_id = 0
    return finishingmethod_id


def find_foldingmethod_id(rfq_input):
    try:
        foldingmethod = FoldingMethods.objects.get(foldingmethod=rfq_input).foldingmethod_id
    except FoldingMethods.DoesNotExist:
        foldingmethod = 0
    return foldingmethod


def find_orientation(rfq_input):
    orientation = 0
    if rfq_input in ['Staand', 'staand', 'Portrait', 'portrait']:
        orientation = 1
    if rfq_input in ['Liggend' 'liggend', 'Landscape', 'landscape']:
        orientation = 2
    if rfq_input in ['Vierkant' 'vierkoant', 'Square', 'square']:
        orientation = 3
    return orientation


def modify_printsided(rfq_input):
    printsided = 0
    if rfq_input in [1, 'Eenzijdig']:
        printsided = 1
    if rfq_input in [2, 'Tweezijdig gelijk']:
        printsided = 2
    if rfq_input in [3, 'Tweezijdig verschillend']:
        printsided = 3
    if rfq_input in [4, 'Alleen voorzijde']:
        printsided = 4
    if rfq_input in [5, 'Alleen achterzijde']:
        printsided = 5

    return printsided


def modify_printcolors(rfq_input):
    printcolors = 0
    if rfq_input in [1, 'Zwart', 'Black']:
        printcolors = 1
    if rfq_input in [4, 'Full Colour']:
        printcolors = 4
    return printcolors


def modify_boleaninput(rfq_input):
    bolean = rfq_input
    if rfq_input in [1, 'Ja', 'Yes']:
        bolean = 1
    if rfq_input in [0, 'Nee', 'No']:
        bolean = 0
    return bolean


def translate_dataframe(dataframe):
    dataframe = dataframe.fillna(0)

    if dataframe.productcategory_id[0] == 3:  # Selfcovers
        dataframe['printsided'] = 2

    empty_cols = []

    if dataframe.productcategory_id[0] == 2:  # Folders
        empty_cols = ['print_booklet', 'pressvarnish_booklet', 'finishing_brochures', 'number_of_pages',
                      'number_pms_colors_booklet',
                      'paperbrand_cover', 'paperweight_cover', 'papercolor_cover']

    if dataframe.productcategory_id[0] in [4, 5]:  # Brochures
        empty_cols = ['folding', 'print_front', 'print_rear', 'pressvarnish_front', 'pressvarnish_rear',
                      'enhance_front', 'enhance_rear', 'number_pms_colors_front', 'number_pms_colors_rear',
                      'paperbrand_cover', 'paperweight_cover', 'papercolor_cover']
        dataframe['printsided'] = 2
        dataframe['enhance_sided'] = 1

    for col in empty_cols:
        try:
            dataframe.insert(2, col, 0.0)
        finally:
            pass

    for col in dataframe.columns:
        if col == 'oplage':
            dataframe['volume'] = dataframe['oplage']

        if col == 'omschrijving':
            dataframe['project_title'] = dataframe['omschrijving']

        if col == 'artikelnummer':
            dataframe['catalog_code'] = dataframe['artikelnummer']

        if col == 'breedte_mm_product':
            dataframe['width_mm_product'] = dataframe['breedte_mm_product']

        if col == 'hoogte_mm_product':
            dataframe['height_mm_product'] = dataframe['hoogte_mm_product']

        if col == 'aantal_paginas':
            dataframe['number_of_pages'] = dataframe['aantal_paginas']

        if col == 'staand_liggend':
            dataframe['portrait_landscape'] = dataframe['staand_liggend']

        if col == 'nabewerking_brochures':
            dataframe['finishing_brochures'] = dataframe['nabewerking_brochures']

        if col == 'bedrukking':
            dataframe['print_booklet'] = dataframe['bedrukking']

        if col == 'bedrukking_bw':
            dataframe['print_booklet'] = dataframe['bedrukking_bw']

        if col == 'persvernis':
            dataframe['pressvarnish_booklet'] = dataframe['persvernis']

        if col == 'papiersoort':
            dataframe['paperbrand'] = dataframe['papiersoort']

        if col == 'papiersoort_bw':
            dataframe['paperbrand'] = dataframe['papiersoort_bw']

        if col == 'papiergewicht_m2':
            dataframe['paperweight'] = (dataframe['papiergewicht_m2'])

        if col == 'papiergewicht_m2_bw':
            dataframe['paperweight'] = (dataframe['papiergewicht_m2_bw'])

        if col == 'papierkleur':
            dataframe['papercolor'] = dataframe['papierkleur']

        if col == 'papierkleur_bw':
            dataframe['papercolor'] = dataframe['papierkleur_bw']

        if col == 'aantal_pms_kleuren':
            dataframe['number_pms_colors_booklet'] = dataframe['aantal_pms_kleuren']

        if col == 'aantal_pms_kleuren_bw':
            dataframe['number_pms_colors_booklet'] = dataframe['aantal_pms_kleuren_bw']

        if col == 'aantal_pms_kleuren_voorzijde':
            dataframe['number_pms_colors_front'] = dataframe['aantal_pms_kleuren_voorzijde']

        if col == 'aantal_pms_kleuren_achterzijde':
            dataframe['number_pms_colors_rear'] = dataframe['aantal_pms_kleuren_achterzijde']

        if col == 'aantal_pms_kleuren':
            dataframe['number_pms_colors_booklet'] = dataframe['aantal_pms_kleuren']

        if col == 'persvernis':
            dataframe['pressvarnish_booklet'] = dataframe['persvernis']

        if col == 'persvernis_bw':
            dataframe['pressvarnish_booklet'] = dataframe['persvernis_bw']

        if col == 'papiersoort_omslag':
            dataframe['paperbrand_cover'] = dataframe['papiersoort_omslag']

        if col == 'papiergewicht_m2_omslag':
            dataframe['paperweight_cover'] = (dataframe['papiergewicht_m2_omslag'])

        if col == 'papierkleur_omslag':
            dataframe['papercolor_cover'] = dataframe['papierkleur_omslag']

        if col == 'uitvoering':
            dataframe['printsided'] = dataframe['uitvoering']

        if col == 'bedrukking':
            dataframe['print_booklet'] = dataframe['bedrukking']

        if col == 'bedrukking_voorzijde':
            dataframe['print_front'] = dataframe['bedrukking_voorzijde']

        if col == 'bedrukking_achterzijde':
            dataframe['print_rear'] = dataframe['bedrukking_achterzijde']

        if col == 'persvernis_omslag':
            dataframe['pressvarnish_front'] = dataframe['persvernis_omslag']

        if col == 'persvernis_voorzijde':
            dataframe['pressvarnish_front'] = dataframe['persvernis_voorzijde']

        if col == 'persvernis_achterzijde':
            dataframe['pressvarnish_rear'] = dataframe['persvernis_achterzijde']

        if col == 'veredeling_voorzijde':
            dataframe['enhance_front'] = dataframe['veredeling_voorzijde']

        if col == 'veredeling_achterzijde':
            dataframe['enhance_rear'] = dataframe['veredeling_achterzijde']

        if col == 'veredeling_uitvoering':
            dataframe['enhance_sided'] = dataframe['veredeling_uitvoering']

        if col == 'verpakking':
            dataframe['packaging'] = dataframe['verpakking']

        if col == 'nabewerking_folders':
            dataframe['folding'] = dataframe['nabewerking_folders']

    return dataframe
