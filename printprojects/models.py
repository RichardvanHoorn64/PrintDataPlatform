from django.core.validators import MinValueValidator, MaxValueValidator

from index.models import ProductCategory
from members.models import Clients, ClientContacts
from profileuseraccount.models import *


class PrintprojectStatus(models.Model):
    printprojectstatus_id = models.AutoField(primary_key=True)
    printprojectstatus = models.CharField(max_length=200)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.printprojectstatus

    class Meta:
        verbose_name = 'printprojectstatus'
        verbose_name_plural = 'printprojectstatus'


class PrintProjects(models.Model):
    printproject_id = models.AutoField(primary_key=True)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Clients, blank=True, null=True, on_delete=models.SET_NULL)
    clientcontact = models.ForeignKey(ClientContacts, blank=True, null=True, on_delete=models.SET_NULL)
    printprojectstatus = models.ForeignKey(PrintprojectStatus, null=True, blank=True, on_delete=models.SET_NULL)
    project_title = models.CharField(max_length=500, blank=True, null=True)
    catalog_code = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=2500, blank=True)
    error = models.TextField(max_length=500, blank=True)
    message_extra_work = models.TextField(max_length=1000, blank=True)
    own_quotenumber = models.CharField(max_length=200, null=True, blank=True, )
    client_quotenumber: str = models.CharField(max_length=200, null=True, blank=True, )

    rfq_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(null=True, blank=True)
    volume = models.PositiveIntegerField(blank=True, null=True, default=0)
    number_of_offers = models.PositiveIntegerField(default=0)

    # planning
    supply_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)

    # Products
    format_selection = models.CharField(max_length=200, blank=True, null=True)
    standard_size = models.CharField(max_length=200, blank=True, null=True)
    height_mm_product = models.PositiveIntegerField(blank=True, null=True)
    width_mm_product = models.PositiveIntegerField(blank=True, null=True)

    # paper
    papercategory = models.CharField(max_length=200, blank=True, null=True)
    paperbrand = models.CharField(max_length=200, blank=True, null=True)
    paperweight = models.PositiveIntegerField(blank=True, null=True, default=0)
    papercolor = models.CharField(max_length=200, blank=True, null=True)

    # pressvarnish
    pressvarnish_front = models.PositiveIntegerField(blank=True, null=True, default=0)
    pressvarnish_back = models.PositiveIntegerField(blank=True, null=True, default=0)
    pressvarnish_booklet = models.PositiveIntegerField(blank=True, null=True, default=0)

    # enhance
    enhance_sided = models.PositiveIntegerField(blank=True, null=True, default=0)
    enhance_front = models.PositiveIntegerField(blank=True, null=True, default=0)
    enhance_back = models.PositiveIntegerField(blank=True, null=True, default=0)

    # packaging choices
    packaging = models.CharField(max_length=200, blank=True, null=True)

    # for folders
    folding = models.PositiveIntegerField(blank=True, null=True, default=0)

    # for folders, selfcovers and brochures:
    number_of_pages = models.PositiveIntegerField(blank=True, null=True, default=0)
    portrait_landscape = models.PositiveIntegerField(blank=True, null=True, default=0)
    finishing_brochures = models.PositiveIntegerField(blank=True, null=True, default=0)

    # printing general
    printsided = models.PositiveIntegerField(blank=True, null=True, default=0)

    # print pms colors
    number_pms_colors_front = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True, null=True,
                                                          default=0)
    number_pms_colors_back = models.PositiveIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)], blank=True, null=True, default=0)
    number_pms_colors_booklet = models.PositiveIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)], blank=True, null=True, default=0)

    # basic print black, full color or only specials
    print_front = models.PositiveIntegerField(blank=True, null=True, default=0)
    print_back = models.PositiveIntegerField(blank=True, null=True, default=0)
    print_booklet = models.PositiveIntegerField(blank=True, null=True, default=0)

    # paper cover
    papercategory_cover = models.CharField(max_length=200, blank=True, null=True)
    paperbrand_cover = models.CharField(max_length=200, blank=True, null=True)
    paperweight_cover = models.PositiveIntegerField(null=True, blank=True)
    papercolor_cover = models.CharField(max_length=200, blank=True, null=True)

    # pricing
    salesprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salesprice_1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoiceturnover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # general
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)
    assortiment_item = models.BooleanField(default=False)

    def __str__(self):
        return self.project_title

    class Meta:
        verbose_name = 'printprojects'
        verbose_name_plural = 'printproject'


class MemberProducerStatus(models.Model):
    memberproducerstatus_id = models.AutoField(primary_key=True, default=None, editable=False)
    status_id = models.PositiveIntegerField(default=0)
    memberproducerstatus = models.CharField(max_length=100, blank=True, null=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.memberproducerstatus

    class Meta:
        verbose_name = 'memberproducerstatus'
        verbose_name_plural = 'memberproducerstatus'


class MemberProducerMatch(models.Model):
    memberproducermatch_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    memberproducerstatus = models.ForeignKey(MemberProducerStatus, null=True, default=2, on_delete=models.CASCADE)
    api = models.BooleanField(default=True)
    api_username = models.CharField(max_length=100, blank=True)
    api_password = models.CharField(max_length=15, blank=True)
    ranking = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    producer_accept = models.BooleanField(default=True)
    member_accept = models.BooleanField(default=True)
    auto_quote = models.BooleanField(default=False)

    # Member salesallowance per productcategory
    perc_salesallowance_1 = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    perc_salesallowance_2 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_3 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_4 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_5 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_6 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_7 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_8 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_9 = models.DecimalField(default=0, decimal_places=2,max_digits=5)
    perc_salesallowance_10 = models.DecimalField(default=0, decimal_places=2,max_digits=5)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.producer

    class Meta:
        verbose_name = 'producers'
        verbose_name_plural = 'producer'


class PrintProjectMatch(models.Model):
    printprojectmatch_id: int = models.AutoField(primary_key=True)
    printproject = models.ForeignKey(PrintProjects, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    memberproducermatch = models.ForeignKey(MemberProducerMatch, null=True, default=2, on_delete=models.CASCADE)
    ranking = models.IntegerField(default=1)
    matchprintproject = models.BooleanField(default=False)
    member_block = models.BooleanField(default=False)
    preferred_supplier = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)
