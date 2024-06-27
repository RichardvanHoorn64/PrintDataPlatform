from assets.models import *
from producers.models import *
from index.forms.form_fieldtypes import *


class CreateUpdatePrinterForm(forms.ModelForm):
    # General
    asset_name = char_field_200_true
    tariff_eur_hour = decimal_field
    productionspeed_sheets_hour = integer_field
    max_number_colors = integer_field_notreq
    starttime_per_order = integer_field_notreq

    buy_tariff_plate_eur = decimal_field_notreq
    margin_plate_eur = decimal_field_notreq

    # Perfecter press
    max_number_colors_front_sw = integer_field_notreq
    max_number_colors_back_sw = integer_field_notreq

    # Options
    perfecting = boolean_field
    varnish_unit = boolean_field
    pms_offered = boolean_field
    varnish_at_printunit = boolean_field

    # Sheet size
    printsize_height = integer_field
    printsize_width = integer_field
    sheetsize_height_min = integer_field
    sheetsize_width_min = integer_field

    # Margins
    extra_mm_sheet_sidemargin = integer_field_notreq
    strips_extra_margin_mm = integer_field_notreq
    central_extra_margin_mm = integer_field_notreq
    extra_strip_option = integer_field_notreq

    # Inkcosts
    ink_1000_prints_zw = decimal_field_notreq
    ink_1000_prints_fc = decimal_field_notreq
    ink_1000_prints_varnish = decimal_field_notreq
    ink_1000_prints_pms = decimal_field_notreq
    ink_start_costs_pms = decimal_field_notreq

    # times
    start_time_sheet_frontside = integer_field_notreq
    start_time_sheet_backside = integer_field_notreq
    start_time_pms_color = integer_field_notreq
    start_time_varnish = integer_field_notreq

    perc_speedreduction_heavy_paper = integer_field_notreq
    weight_heavy_paper = integer_field_notreq
    perc_speedreduction_light_paper = integer_field_notreq
    weight_light_paper = integer_field_notreq
    perc_speedreduction_perfecting = integer_field_notreq
    changetime_perfector = integer_field_notreq

    # paperwaste
    paperwaste_per_order = integer_field_notreq
    paperwaste_per_side_black = integer_field_notreq
    paperwaste_per_side_fc = integer_field_notreq
    paperwaste_per_side_pms = integer_field_notreq
    paperwaste_per_side_varnish = integer_field_notreq
    perc_paperwaste_printing_1000_sheets = integer_field_notreq
    perc_extra_paperwaste_printing_pms = integer_field_notreq
    perc_paperwaste_printing_1000_sheet_perfector = integer_field_notreq

    class Meta:
        model = Printers
        fields = (
            'asset_name', 'productionspeed_sheets_hour', 'max_number_colors', 'starttime_per_order', 'tariff_eur_hour',
            'buy_tariff_plate_eur', 'margin_plate_eur', 'max_number_colors_front_sw', 'max_number_colors_back_sw',
            'perfecting', 'varnish_unit', 'varnish_at_printunit', 'pms_offered', 'printsize_height', 'printsize_width',
            'sheetsize_height_min',
            'sheetsize_width_min', 'extra_mm_sheet_sidemargin', 'strips_extra_margin_mm', 'central_extra_margin_mm',
            'extra_strip_option', 'ink_1000_prints_zw', 'ink_1000_prints_fc', 'ink_1000_prints_varnish',
            'ink_1000_prints_pms', 'ink_start_costs_pms', 'start_time_sheet_frontside', 'start_time_sheet_backside',
            'start_time_pms_color', 'start_time_varnish', 'perc_speedreduction_heavy_paper', 'weight_heavy_paper',
            'perc_speedreduction_light_paper', 'weight_light_paper', 'perc_speedreduction_perfecting',
            'changetime_perfector',
            'paperwaste_per_order', 'paperwaste_per_side_black', 'paperwaste_per_side_fc', 'paperwaste_per_side_pms',
            'paperwaste_per_side_varnish', 'perc_paperwaste_printing_1000_sheets', 'perc_extra_paperwaste_printing_pms',
            'perc_paperwaste_printing_1000_sheet_perfector')


class CreateUpdateCuttingmachinesForm(forms.ModelForm):
    # General
    asset_name = char_field_200_true
    tariff_eur_hour = decimal_field
    max_width_mm = integer_field
    max_depth_mm = integer_field
    max_stackheight_mm = integer_field
    setup_order_min = integer_field
    time_cutting_sec = integer_field
    time_per_extra_sec = integer_field

    class Meta:
        model = Cuttingmachines
        fields = (
            'asset_name', 'tariff_eur_hour', 'max_width_mm', 'max_depth_mm', 'max_stackheight_mm', 'setup_order_min',
            'time_cutting_sec', 'time_per_extra_sec')


class CreateUpdateFoldingMachinesForm(forms.ModelForm):
    asset_name = char_field_200_false
    tariff_eur_hour = decimal_field_notreq
    added_value = boolean_field
    vertical_offered = boolean_field
    landscape_offered = boolean_field
    square_offered = boolean_field
    max_paperheight_mm = integer_field_notreq
    max_paperwidth_mm = integer_field_notreq
    max_number_stations = integer_field_notreq

    # folders
    sheet_per_hour = integer_field_notreq
    setup_time_min = integer_field_notreq
    setup_time_per_station_min = integer_field_notreq
    speedreduction_heavy_paper_perc = decimal_field_notreq
    weight_heavy_paper = integer_field_notreq
    speedreduction_light_paper_perc = decimal_field_notreq
    weight_light_paper = integer_field_notreq
    paperwaste_1000sheet_perc = decimal_field_notreq
    paperwaste_start = integer_field_notreq

    # katerns
    margin_katern_mm = integer_field_notreq
    meter_per_hour = integer_field_notreq
    pages_per_katern = integer_field_notreq
    sheet_input = char_field_200_false
    setup_time_1e_katern_min = integer_field_notreq
    setup_time_next_katern_min = integer_field_notreq
    min_weight_paper_katern = integer_field_notreq
    max_weight_paper_katern = integer_field_notreq

    class Meta:
        model = Foldingmachines
        fields = ('asset_name', 'tariff_eur_hour', 'added_value',
                  'vertical_offered', 'landscape_offered', 'square_offered', 'max_paperheight_mm', 'max_paperwidth_mm',
                  'max_number_stations', 'sheet_per_hour', 'setup_time_min', 'setup_time_per_station_min',
                  'speedreduction_heavy_paper_perc', 'weight_heavy_paper', 'speedreduction_light_paper_perc',
                  'weight_light_paper', 'paperwaste_1000sheet_perc', 'paperwaste_start', 'margin_katern_mm',
                  'meter_per_hour', 'pages_per_katern', 'sheet_input', 'setup_time_1e_katern_min',
                  'setup_time_next_katern_min', 'min_weight_paper_katern', 'max_weight_paper_katern')


class CreateUpdateBindingMachineForm(forms.ModelForm):
    asset_name = char_field_200_true
    tariff_eur_hour = decimal_field
    added_value = boolean_field
    finishingmethod_id = integer_field_notreq
    cover_feeder = boolean_field
    max_number_stations_default = integer_field
    max_number_stations_max = integer_field
    max_speed_hour = integer_field
    speedreduction_extra_station = integer_field
    max_width_untrimmed_mm = integer_field
    max_height_untrimmed_mm = integer_field
    min_width_untrimmed_mm = integer_field
    min_height_untrimmed_mm = integer_field
    setup_order_min = integer_field
    setup_time_cover_min = integer_field
    setup_time_station_min = integer_field
    paperwaste_perc = integer_field
    speedreduction_landscape = integer_field
    speedreduction_square = integer_field
    setup_landscape = integer_field
    setup_square = integer_field

    class Meta:
        model = Bindingmachines
        fields = (
            'asset_name', 'tariff_eur_hour', 'added_value', 'finishingmethod_id', 'tariff_eur_hour', 'added_value',
            'cover_feeder',
            'max_number_stations_default', 'max_number_stations_max', 'max_speed_hour', 'speedreduction_extra_station',
            'max_width_untrimmed_mm', 'max_height_untrimmed_mm', 'min_width_untrimmed_mm',
            'min_height_untrimmed_mm', 'setup_order_min', 'setup_time_cover_min', 'setup_time_station_min',
            'paperwaste_perc', 'speedreduction_landscape', 'speedreduction_square', 'setup_landscape', 'setup_square'
        )


class ProducerUpdateGeneralTariffForm(forms.ModelForm):
    order_startcost = decimal_field_notreq
    purchase_paper_perc_added = decimal_field_notreq
    overflow_offset_mm = decimal_field_notreq
    katernmargin = decimal_field_notreq
    headmargin = decimal_field_notreq

    class Meta:
        model = GeneralCalculationSettings
        fields = ('order_startcost', 'purchase_paper_perc_added', 'overflow_offset_mm', 'katernmargin', 'headmargin')


class ProducerCreateUpdateEnhancementForm(forms.ModelForm):
    enhancement_id = char_field_200_false
    setup_cost = decimal_field_notreq
    minimum_cost = decimal_field_notreq
    production_cost_1000sheets = decimal_field_notreq
    max_sheet_width = decimal_field_notreq
    max_sheet_height = decimal_field_notreq

    class Meta:
        model = EnhancementTariffs
        fields = ('enhancement_id', 'setup_cost', 'minimum_cost', 'production_cost_1000sheets', 'max_sheet_width',
                  'max_sheet_height')


class ProducerUpdatePackagingForm(forms.ModelForm):
    setup_cost = decimal_field_notreq
    cost_per_100kg = decimal_field_notreq
    cost_per_unit = decimal_field_notreq
    max_weight_packaging_unit_kg = integer_field_notreq

    class Meta:
        model = PackagingTariffs
        fields = ('setup_cost', 'cost_per_100kg', 'cost_per_unit', 'max_weight_packaging_unit_kg')
