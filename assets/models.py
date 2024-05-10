# Create your models here.
from methods.models import EnhancementOptions, PackagingOptions, BrochureFinishingMethods
from django.core.validators import MaxValueValidator, MinValueValidator
from profileuseraccount.models import *


class GeneralCalculationSettings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    order_startcost = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    purchase_paper_perc_added = models.DecimalField(default=0,
                                                    validators=[MaxValueValidator(100), MinValueValidator(0)],
                                                    max_digits=6, decimal_places=2)
    overflow_offset_mm = models.PositiveIntegerField(default=2)
    katernmargin = models.PositiveIntegerField(default=5)
    headmargin = models.PositiveIntegerField(default=5)
    pms_offering = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'general tariff'
        verbose_name_plural = 'general-tariffs'


class Printers(models.Model):
    printer_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=200)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    tariff_eur_hour = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    buy_tariff_plate_eur = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)
    margin_plate_eur = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)

    # Options
    perfecting = models.BooleanField(default=False)
    pms_offered = models.BooleanField(default=False)
    varnish_unit = models.BooleanField(default=False)
    varnish_at_printunit = models.BooleanField(default=False)

    # ink
    ink_1000_prints_zw = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)
    ink_1000_prints_fc = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)
    ink_1000_prints_varnish = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)
    ink_1000_prints_pms = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)
    ink_start_costs_pms = models.DecimalField(default=0, null=True, max_digits=6, decimal_places=2)

    # colors
    max_number_colors = models.PositiveIntegerField(null=True)
    max_number_colors_front_sw = models.PositiveIntegerField(default=0, null=True, blank=True)
    max_number_colors_back_sw = models.PositiveIntegerField(null=True, default=0)

    # size
    printsize_height = models.PositiveIntegerField(default=0)
    printsize_width = models.PositiveIntegerField(default=0)
    sheetsize_height_min = models.PositiveIntegerField(default=0)
    sheetsize_width_min = models.PositiveIntegerField(default=0)

    # margins
    extra_mm_sheet_sidemargin = models.PositiveIntegerField(null=True, default=0)
    strips_extra_margin_mm = models.PositiveIntegerField(null=True, default=0)
    central_extra_margin_mm = models.PositiveIntegerField(null=True, default=0)
    extra_strip_option = models.PositiveIntegerField(null=True, default=0)

    #  speed
    productionspeed_sheets_hour = models.PositiveIntegerField(default=0, null=True)
    perc_speedreduction_heavy_paper = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True)
    weight_heavy_paper = models.PositiveIntegerField(default=170, null=True)
    perc_speedreduction_light_paper = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True)
    weight_light_paper = models.PositiveIntegerField(default=80, null=True)

    # times
    starttime_per_order = models.PositiveIntegerField(default=0, null=True)
    start_time_sheet_frontside = models.PositiveIntegerField(default=0, null=True)
    start_time_sheet_backside = models.PositiveIntegerField(default=0, null=True)
    start_time_pms_color = models.PositiveIntegerField(default=0, null=True)
    start_time_varnish = models.PositiveIntegerField(default=0, null=True)
    perc_speedreduction_perfecting = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True)
    changetime_perfector = models.PositiveIntegerField(default=0, null=True)

    # paperwaste
    paperwaste_per_order = models.PositiveIntegerField(default=0, null=True)
    paperwaste_per_side_black = models.PositiveIntegerField(default=0, null=True)
    paperwaste_per_side_fc = models.PositiveIntegerField(default=0, null=True)
    paperwaste_per_side_pms = models.PositiveIntegerField(default=0, null=True)
    paperwaste_per_side_varnish = models.PositiveIntegerField(default=0, null=True)
    perc_paperwaste_printing_1000_sheets = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True)
    perc_extra_paperwaste_printing_pms = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True)
    perc_paperwaste_printing_1000_sheet_perfector = models.DecimalField(default=0, max_digits=6, decimal_places=2,
                                                                        null=True)

    def __str__(self):
        return self.asset_name

    class Meta:
        verbose_name = 'Printer'
        verbose_name_plural = 'Printers'


class Cuttingmachines(models.Model):
    cuttingmachine_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=200)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    tariff_eur_hour = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    max_width_mm = models.PositiveIntegerField(validators=[MaxValueValidator(2000)], default=0, )
    max_depth_mm = models.PositiveIntegerField(validators=[MaxValueValidator(2000)], default=0, )
    max_stackheight_mm = models.PositiveIntegerField(validators=[MaxValueValidator(500)], default=0, )
    setup_order_min = models.PositiveIntegerField(default=0, )
    time_cutting_sec = models.PositiveIntegerField(default=0, )
    time_per_extra_sec = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return self.asset_name

    def save(self, *args, **kwargs):
        self.speed = self.time_cutting_sec * 3600
        super(Cuttingmachines, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cuttingmachines'
        verbose_name_plural = 'Cuttingmachine'


class FoldingTypes(models.Model):
    foldingtype_id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Languages, null=True, default=1, on_delete=models.SET_NULL)
    foldingtype = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Foldingtypes'
        verbose_name_plural = 'Foldingtype'


class Foldingmachines(models.Model):
    foldingmachine_id = models.AutoField(primary_key=True)
    foldingtype = models.ForeignKey(FoldingTypes, null=True, on_delete=models.SET_NULL)
    asset_name = models.CharField(max_length=200)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    tariff_eur_hour = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    added_value = models.BooleanField(default=True)
    vertical_offered = models.BooleanField(default=True)
    landscape_offered = models.BooleanField(default=True)
    square_offered = models.BooleanField(default=True)
    max_paperheight_mm = models.PositiveIntegerField(default=0, null=True)
    max_paperwidth_mm = models.PositiveIntegerField(default=0, null=True)
    setup_time_min = models.PositiveIntegerField(default=0, null=True)

    speedreduction_heavy_paper_perc = models.DecimalField(default=0, null=True, decimal_places=2,
                                                          max_digits=5)
    weight_heavy_paper = models.PositiveIntegerField(default=170, null=True)
    speedreduction_light_paper_perc = models.DecimalField(default=0, null=True, decimal_places=2,
                                                          max_digits=5)
    weight_light_paper = models.PositiveIntegerField(default=80, null=True)
    paperwaste_1000sheet_perc = models.DecimalField(default=0, null=True, decimal_places=2, max_digits=5)
    paperwaste_start = models.PositiveIntegerField(default=0, null=True)

    # folders
    setup_time_per_station_min = models.PositiveIntegerField(default=0, null=True)
    max_number_stations = models.PositiveIntegerField(default=0, null=True)
    sheet_per_hour = models.PositiveIntegerField(default=0, null=True)

    # katerns
    margin_katern_mm = models.PositiveIntegerField(default=0, null=True)
    meter_per_hour = models.DecimalField(default=0, null=True, decimal_places=2, max_digits=5)
    pages_per_katern = models.PositiveIntegerField(null=True, default=4)
    sheet_input = models.CharField(max_length=50, default='sheet_height')
    setup_time_1e_katern_min = models.PositiveIntegerField(default=0, null=True)
    setup_time_next_katern_min = models.PositiveIntegerField(default=0, null=True)
    min_weight_paper_katern = models.PositiveIntegerField(default=80)
    max_weight_paper_katern = models.PositiveIntegerField(default=170)

    def __str__(self):
        return self.asset_name

    class Meta:
        verbose_name = 'foldingmachines'
        verbose_name_plural = 'foldingmachine'


class Bindingmachines(models.Model):
    bindingmachine_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=200)
    finishingmethod = models.ForeignKey(BrochureFinishingMethods, on_delete=models.CASCADE, default=1)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    tariff_eur_hour = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    added_value = models.BooleanField(default=True)
    cover_feeder = models.BooleanField(default=False)
    max_number_stations_default = models.PositiveIntegerField(null=True, default=0)
    max_number_stations_max = models.PositiveIntegerField(null=True, default=0)
    max_speed_hour = models.PositiveIntegerField(null=True, default=0)
    speedreduction_extra_station = models.PositiveIntegerField(null=True, default=0)
    max_width_untrimmed_mm = models.PositiveIntegerField(null=True, default=0)
    max_height_untrimmed_mm = models.PositiveIntegerField(null=True, default=0)
    min_width_untrimmed_mm = models.PositiveIntegerField(null=True, default=0)
    min_height_untrimmed_mm = models.PositiveIntegerField(null=True, default=0)
    setup_order_min = models.PositiveIntegerField(null=True, default=0)
    setup_time_cover_min = models.PositiveIntegerField(null=True, default=0)
    setup_time_station_min = models.PositiveIntegerField(null=True, default=0)
    paperwaste_perc = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    speedreduction_landscape = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    speedreduction_square = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    setup_landscape = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    setup_square = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.asset_name

    class Meta:
        verbose_name = 'Bindingmachine'
        verbose_name_plural = 'Bindingmachines'


