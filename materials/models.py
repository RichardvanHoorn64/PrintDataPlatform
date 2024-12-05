from django.db import models
from profileuseraccount.models import Producers, Languages


class PaperBrandReference(models.Model):
    paperbrandreference_id = models.AutoField(primary_key=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    papercategory = models.CharField(max_length=250, blank=True)
    paperbrand = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    FSC = models.BooleanField(default=True)

    def __str__(self):
        return self.papercategory

    class Meta:
        verbose_name = 'paperbrand'
        verbose_name_plural = 'paperbrands'


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
    singe_sided = models.BooleanField(default=False)
    sheets_per_pack = models.PositiveIntegerField(null=True, blank=True)
    price_1000sheets = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    upload_date = models.DateField(null=True)
    uploaded_by = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.paperbrand

    class Meta:
        verbose_name = 'paper'
        verbose_name_plural = 'papers'


class EnvelopeCategory(models.Model):
    env_category_id = models.AutoField(primary_key=True)
    env_category_name = models.CharField(max_length=250, blank=True)
    producer = models.ForeignKey(Producers, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.env_category_name

    class Meta:
        verbose_name = 'envelope_category'
        verbose_name_plural = 'envelope_categories'


class EnvelopeCatalog(models.Model):
    envelope_catalog_id = models.AutoField(primary_key=True)
    supplier = models.CharField(max_length=250)
    supplier_number = models.CharField(max_length=250)
    env_category_name = models.CharField(max_length=250)
    env_paper = models.CharField(max_length=250, blank=True)
    env_color = models.CharField(max_length=250, blank=True, null=True)
    env_interior = models.CharField(max_length=250, blank=True, null=True)
    env_height_mm = models.PositiveIntegerField(null=True, blank=True)
    env_width_mm = models.PositiveIntegerField(null=True, blank=True)
    env_size = models.CharField(max_length=250, blank=True)
    env_weight_m2 = models.PositiveIntegerField(null=True, blank=True)
    env_die_cut = models.CharField(max_length=250, blank=True)
    env_closure = models.CharField(max_length=250, blank=True)
    env_window_orientation = models.CharField(max_length=250, blank=True)
    env_window_size = models.CharField(max_length=250, blank=True)
    env_window_position = models.CharField(max_length=250, blank=True)
    FSC = models.BooleanField(default=True)

    # for dropdowns
    env_category = models.ForeignKey(EnvelopeCategory, null=True, on_delete=models.CASCADE)
    env_size_close_cut = models.CharField(max_length=500, blank=True, null=True)
    env_material_color = models.CharField(max_length=500, blank=True, null=True)
    env_window = models.CharField(max_length=500, blank=True, null=True)

    # for auto calculations
    producer = models.ForeignKey(Producers, default=1, null=True, on_delete=models.CASCADE)
    envelopes_per_pack = models.PositiveIntegerField(null=True, blank=True)
    price_1000_envelopes = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    upload_date = models.DateField(null=True)
    uploaded_by = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.envelope_catalog_id

    class Meta:
        verbose_name = 'paper'
        verbose_name_plural = 'papers'
