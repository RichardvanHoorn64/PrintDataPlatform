from methods.models import *
from profileuseraccount.models import *


class ProducerProductOfferings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    min_product_size = models.PositiveIntegerField(null=True, default=1)
    max_product_size = models.PositiveIntegerField(null=True, default=1000)
    min_product_volume = models.PositiveIntegerField(null=True, default=1)
    max_product_volume = models.PositiveIntegerField(null=True, default=100000)
    availeble = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.productcategory


class ProducerContacts(models.Model):
    producercontact_id = models.AutoField(primary_key=True)
    producercontact = models.CharField(max_length=200, blank=True, null=True)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    jobtitle = models.CharField(max_length=25, blank=True)
    contact = models.CharField(max_length=200, blank=True, null=True)
    e_mail_personal = models.EmailField(blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    # social media
    linkedin_url = models.URLField(null=True, blank=True, max_length=200)
    facebook_url = models.URLField(null=True, blank=True, max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.producercontact

    class Meta:
        verbose_name = 'producercontacts'
        verbose_name_plural = 'producercontact'


class EnhancementTariffs(models.Model):
    enhancementtariff_id = models.AutoField(primary_key=True)
    enhancement = models.ForeignKey(EnhancementOptions, blank=True, null=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    added_value = models.BooleanField(default=True)
    availeble = models.BooleanField(default=False, null=True, blank=True)
    setup_cost = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    minimum_cost = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    production_cost_1000sheets = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    max_sheet_width = models.PositiveIntegerField(default=0)
    max_sheet_height = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'enhancementtariffs'
        verbose_name_plural = 'enhancementtariff'


class PackagingTariffs(models.Model):
    packagingtariff_id = models.AutoField(primary_key=True)
    packagingoption = models.ForeignKey(PackagingOptions, blank=True, null=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    availeble = models.BooleanField(default=False, null=True, blank=True)
    setup_cost = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    cost_per_100kg = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    cost_per_unit = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    max_weight_packaging_unit_kg = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'packagingtariffs'
        verbose_name_plural = 'packagingtariff'


class TransportTariffs(models.Model):
    transporttariff_id = models.AutoField(primary_key=True)
    transportoption = models.ForeignKey(TransportOptions, blank=True, null=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    added_value = models.BooleanField(default=True)
    availeble = models.BooleanField(default=False, null=True, blank=True)
    setup_cost = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    cost_per_100kg = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'transporttariffs'
        verbose_name_plural = 'transporttariff'
