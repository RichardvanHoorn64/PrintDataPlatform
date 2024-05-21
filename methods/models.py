from printprojects.models import PrintProjects, Clients, ProductCategory
from profileuseraccount.models import *


class Notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, null=True, on_delete=models.CASCADE)
    printproject = models.ForeignKey(PrintProjects, null=True, on_delete=models.CASCADE)
    offer = models.PositiveIntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    note = models.CharField(max_length=2500, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural = 'note'


class StandardSize(models.Model):
    standardsize_id = models.AutoField(primary_key=True)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    standard = models.CharField(max_length=50, blank=True, null=True)
    size_description = models.TextField(max_length=200, blank=True)
    height_mm_product = models.PositiveIntegerField(blank=True, null=True)
    width_mm_product = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.size_description

    class Meta:
        verbose_name = 'standardsizes'
        verbose_name_plural = 'standardsize'


class FoldingMethods(models.Model):
    foldingmethod_id = models.AutoField(primary_key=True)
    foldingmethod = models.TextField(max_length=200, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    number_of_pages = models.PositiveIntegerField(blank=True, null=True)
    width_factor = models.PositiveIntegerField(blank=True, null=True)
    height_factor = models.PositiveIntegerField(blank=True, null=True)
    foldingmachine_number_of_stations = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.foldingmethod

    class Meta:
        verbose_name = 'foldingmethod'
        verbose_name_plural = 'foldingmethods'


class BrochureFinishingMethods(models.Model):
    finishingmethod_id = models.AutoField(primary_key=True)
    finishingmethod = models.TextField(max_length=200, blank=True)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.finishingmethod

    class Meta:
        verbose_name = 'finishingmethod'
        verbose_name_plural = 'finishingmethods'


class EnhancementOptions(models.Model):
    enhancement_id = models.AutoField(primary_key=True)
    enhancement = models.CharField(max_length=200)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.enhancement

    class Meta:
        verbose_name = 'Enhancement option'
        verbose_name_plural = 'Enhancement options'


class PackagingOptions(models.Model):
    packagingoption_id = models.AutoField(primary_key=True)
    packaging = models.CharField(max_length=50)
    packaging_unit = models.CharField(max_length=150)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'packagingoption'
        verbose_name_plural = 'packaging options'


class TransportOptions(models.Model):
    transportoption_id = models.AutoField(primary_key=True)
    transport = models.CharField(max_length=50)
    measure = models.CharField(max_length=150)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'transportoption'
        verbose_name_plural = 'transport options'
