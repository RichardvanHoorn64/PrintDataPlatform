from calculations.models import Calculations
from profileuseraccount.models import *
from printprojects.models import *
from profileuseraccount.models import *

class Offerstatus(models.Model):
    offerstatus_id = models.AutoField(primary_key=True)
    offerstatus = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return self.offerstatus

    class Meta:
        verbose_name = 'offerstatus'
        verbose_name_plural = 'offerstatus'


# Create your models here.
class Offers(models.Model):
    offer_id = models.AutoField(primary_key=True)
    printproject = models.ForeignKey(PrintProjects, null=True, blank=True, on_delete=models.SET_NULL)
    calculation = models.ForeignKey(Calculations, null=True, blank=True, on_delete=models.SET_NULL)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    offerstatus = models.ForeignKey(Offerstatus, null=True, blank=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    offer_date = models.DateTimeField(blank=True, null=True)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=1000, blank=True)
    requester = models.CharField(max_length=200, blank=True, null=True)

    offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer1000extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    producer_contact = models.CharField(max_length=200, blank=True, null=True)
    producer_quote = models.CharField(max_length=200, blank=True, null=True)
    producer_notes = models.TextField(max_length=2500, blank=True)
    offer_key = models.PositiveIntegerField(null=True, blank=True)
    offer_key_test = models.PositiveIntegerField(null=True, blank=True)
    reference_key = models.PositiveIntegerField(null=True, blank=True)

    # uploaded offers tot blobstorage
    doc_name = models.TextField(max_length=250, blank=True)
    doc_uploaded = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    # offer submit data
    submit_date = models.DateTimeField(null=True, blank=True)
    submit_by = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'offers'
        verbose_name_plural = 'offer'
