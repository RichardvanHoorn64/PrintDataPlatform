from django.db import models
from profileuseraccount.models import Producers, Languages


class PaperBrandReference(models.Model):
    paperbrandreference_id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    papercategory = models.CharField(max_length=250, blank=True)
    paperbrand = models.CharField(max_length=250, blank=True)
    folders = models.BooleanField(default=True)
    brochures_interior = models.BooleanField(default=True)
    brochures_cover = models.BooleanField(default=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    FSC = models.BooleanField(default=True)

    def __str__(self):
        return self.papercategory

    class Meta:
        verbose_name = 'paperbrand'
        verbose_name_plural = 'paperbrands'


class PaperCategories(models.Model):
    papercategory_id = models.AutoField(primary_key=True)
    papercategory = models.CharField(max_length=250, blank=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    folders_cover = models.BooleanField(default=True)
    brochures_booklet = models.BooleanField(default=True)
    brochures_cover = models.BooleanField(default=True)

    def __str__(self):
        return self.papercategory

    class Meta:
        verbose_name = 'papercategory'
        verbose_name_plural = 'papercategories'


class PaperBrands(models.Model):
    paperbrand_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    papercategory = models.CharField(max_length=250, blank=True)
    paperbrand = models.CharField(max_length=250, blank=True)
    upload_date = models.DateField(null=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.paperbrand

    class Meta:
        verbose_name = 'paperbrand'
        verbose_name_plural = 'paperbrands'


class PaperWeights(models.Model):
    paperweight_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    papercategory = models.CharField(max_length=250, blank=True)
    paperbrand = models.CharField(max_length=250, blank=True)
    paperweight_m2 = models.PositiveIntegerField(null=True, blank=True)
    upload_date = models.DateField(null=True)

    def __str__(self):
        return self.paperweight_m2

    class Meta:
        verbose_name = 'paperweight'
        verbose_name_plural = 'paperweights'


class PaperCatalog(models.Model):
    paperspec_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=250)
    supplier_number = models.CharField(max_length=250)
    papercategory = models.CharField(max_length=250)
    paperbrand = models.CharField(max_length=250, blank=True)
    papercolor = models.CharField(max_length=25, blank=True, null=True)
    paperweight_m2 = models.PositiveIntegerField(null=True, blank=True)
    paper_height_mm = models.PositiveIntegerField(null=True, blank=True)
    paper_width_mm = models.PositiveIntegerField(null=True, blank=True)
    paper_surface = models.PositiveIntegerField(null=True, blank=True)
    fiber_direction = models.CharField(max_length=250, blank=True)
    paper_thickening = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    sheets_per_pack = models.PositiveIntegerField(null=True, blank=True)
    price_1000sheets = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    upload_date = models.DateField(null=True)
    uploaded_by = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.paperbrand

    class Meta:
        verbose_name = 'paper'
        verbose_name_plural = 'papers'
