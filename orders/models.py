from offers.models import *
from printprojects.models import *
from profileuseraccount.models import *


class OrderStatus(models.Model):
    orderstatus_id = models.AutoField(primary_key=True)
    orderstatus = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.orderstatus

    class Meta:
        verbose_name = 'orderstatus'
        verbose_name_plural = 'orderstatus'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    ordernumber = models.CharField(max_length=200, blank=True, null=True)
    printproject = models.ForeignKey(PrintProjects, null=True, blank=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, null=True, blank=True, on_delete=models.SET_NULL)
    offer = models.ForeignKey(Offers, null=True, blank=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    productcategory = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    order_status = models.ForeignKey(OrderStatus, null=True, blank=True, on_delete=models.SET_NULL)
    order_description = models.TextField(max_length=1000, blank=True)
    supplier_remarks = models.TextField(max_length=500, blank=True)
    orderdate = models.DateField(blank=True, null=True)
    orderer = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    order_volume = models.PositiveIntegerField(blank=True, null=True)
    order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_morecost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_remarks = models.TextField(max_length=300, blank=True)
    delivery_date_request = models.DateField(blank=True, null=True)
    delivery_date_deliverd = models.DateField(blank=True, null=True)
    printfiles_available = models.CharField(max_length=300, blank=True, null=True)
    deliver_street_number = models.CharField(max_length=300, blank=True, null=True)
    deliver_postcode = models.CharField(max_length=300, blank=True, null=True)
    deliver_city = models.CharField(max_length=300, blank=True, null=True)
    deliver_company = models.CharField(max_length=300, blank=True, null=True)
    deliver_contactperson = models.CharField(max_length=300, blank=True, null=True)
    deliver_tel = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_description

    class Meta:
        verbose_name = 'orders'
        verbose_name_plural = 'order'
