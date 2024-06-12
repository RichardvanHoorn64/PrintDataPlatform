from printprojects.models import PrintProjects
from assets.models import *
from methods.models import ProductCategory


class Calculations(models.Model):
    calculation_id = models.AutoField(primary_key=True)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    printproject = models.ForeignKey(PrintProjects, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=5000, blank=True, null=True)

    # status
    assortiment_item = models.BooleanField(default=False)
    catalog_code = models.CharField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=2000, blank=True, null=True)
    error = models.CharField(max_length=2000, blank=True, null=True)
    volume = models.PositiveIntegerField(null=True, blank=True)

    # asset selection
    printer = models.CharField(max_length=200, blank=True, null=True)
    printer_booklet = models.CharField(max_length=200, blank=True, null=True)
    printer_cover = models.CharField(max_length=200, blank=True, null=True)
    cuttingmachine = models.CharField(max_length=200, blank=True, null=True)
    cuttingmachine_booklet = models.CharField(max_length=200, blank=True, null=True)
    foldingmachine = models.CharField(max_length=200, blank=True, null=True)
    foldingmachines_booklet = models.CharField(max_length=2000, blank=True, null=True)
    bindingmachine = models.CharField(max_length=200, blank=True, null=True)

    # paper selection
    paperspec_id = models.CharField(max_length=35, null=True, blank=True)
    paperspec_id_booklet = models.CharField(max_length=35, null=True, blank=True)
    paperspec_id_cover = models.CharField(max_length=35, null=True, blank=True)
    purchase_paper_perc_added = models.PositiveIntegerField(null=True, blank=True, default=0)

    # brochure booklet
    pages_per_sheet_booklet = models.PositiveIntegerField(blank=True, default=0)
    pages_per_katern_booklet = models.PositiveIntegerField(blank=True, default=0)
    number_of_printruns_booklet = models.PositiveIntegerField(blank=True, default=0)
    book_thickness = models.PositiveIntegerField(blank=True, default=0)

    # paper waste
    waste_printing = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_printing1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_folding = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_folding1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_binding = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_binding1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)

    # paper waste cover
    waste_printing_cover = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_printing_cover1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_binding_cover = models.PositiveIntegerField(null=True, blank=True, default=0)
    waste_binding_cover1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)

    #  production
    order_startcost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )

    # printing costs
    printingcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printingcost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printingcost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printingcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printingcost_booklet1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printingcost_cover1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # inkcosts
    inkcost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    inkcost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    inkcost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    inkcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    inkcost_booklet1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    inkcost_cover1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )

    # folding costs
    foldingcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    foldingcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    foldingcost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    foldingcost_booklet1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # cutting costs 
    cuttingcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuttingcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuttingcost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuttingcost_booklet1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuttingcost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuttingcost_cover1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # finisching costs 
    bindingcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bindingcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # enhance costs (cover)
    enhancecost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    enhancecost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    enhancecost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    enhancecost_cover1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # plate costs 
    purchase_plates = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    margin_plates = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    platecost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    purchase_plates_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    margin_plates_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    platecost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    purchase_plates_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    margin_plates_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    platecost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )

    # paper costs 
    papercost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    papercost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    papercost_booklet = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    papercost_booklet1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    papercost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    papercost_cover1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    #  calculation cover
    number_of_printruns_cover = models.PositiveIntegerField(blank=True, default=0)
    cover_starttime = models.PositiveIntegerField(blank=True, default=0)
    printing_runtime_cover = models.PositiveIntegerField(blank=True, default=0)

    add_value_purchase_paper_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paper1000extra_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paper1000extra_cost_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    add_value_purchase_paper1000extra_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    printing_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    net_paper_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    net_paper_quantity1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    net_paper_quantity_booklet = models.PositiveIntegerField(null=True, blank=True, default=0)
    net_paper_quantity_booklet1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    net_paper_quantity_cover = models.PositiveIntegerField(null=True, blank=True, default=0)
    net_paper_quantity_cover1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)

    paper_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    paper_quantity1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    paper_quantity_booklet = models.PositiveIntegerField(null=True, blank=True, default=0)
    paper_quantity_booklet1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)
    paper_quantity_cover = models.PositiveIntegerField(null=True, blank=True, default=0)
    paper_quantity_cover1000extra = models.PositiveIntegerField(null=True, blank=True, default=0)

    # papercost
    papercost_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    papercost_booklet_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    papercost_cover_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    papercost_total1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    papercost_booklet_total1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    papercost_cover_total1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )

    # packaging costs
    packagingcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    packagingcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # logistics
    orderweight_kg = models.PositiveIntegerField(null=True, blank=True, )
    orderweight_kg1000extra = models.PositiveIntegerField(null=True, blank=True, )

    # transportation cost
    transportcost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    transportcost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    #   total en added value
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    total_cost1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # added_value calculation
    added_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    perc_added_value = models.PositiveIntegerField(null=True, blank=True, )
    added_value1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    perc_added_value1000extra = models.PositiveIntegerField(null=True, blank=True, )

    # member discount
    memberdiscount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    memberdiscount1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # offer
    offer_date = models.DateField(null=True, blank=True)
    offer_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    offer_value1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Calculations'
        verbose_name_plural = 'Calculation'
