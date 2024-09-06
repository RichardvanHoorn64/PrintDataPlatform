from django.db import models
from profileuseraccount.models import Members


# Create your models here.
class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    client = models.CharField(max_length=100, unique=True)
    tel_general = models.CharField(max_length=15, blank=True)
    e_mail_general = models.EmailField(blank=True)
    street_number = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=100, blank=True)

    manager_first_name = models.CharField(max_length=200, blank=True)
    manager_last_name = models.CharField(max_length=200, blank=True)
    manager_jobtitle = models.CharField(max_length=200, blank=True)
    manager_mobile_number = models.CharField(max_length=100, blank=True)
    manager_e_mail = models.CharField(max_length=100, blank=True)

    count_printprojects = models.PositiveIntegerField(default=0)
    count_orders = models.PositiveIntegerField(default=0)

    # social media
    linkedin_url = models.URLField(null=True, blank=True, max_length=200)
    facebook_url = models.URLField(null=True, blank=True, max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.client

    class Meta:
        verbose_name = 'clients'
        verbose_name_plural = 'client'


class ClientContacts(models.Model):
    clientcontact_id = models.AutoField(primary_key=True)
    clientcontact = models.CharField(max_length=200, blank=True, null=True)
    member = models.ForeignKey(Members, null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    jobtitle = models.CharField(max_length=25, blank=True)
    e_mail_personal = models.EmailField(blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    manager = models.BooleanField(default=False)

    # social media
    linkedin_url = models.URLField(null=True, blank=True, max_length=200)
    facebook_url = models.URLField(null=True, blank=True, max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.clientcontact

    class Meta:
        verbose_name = 'clientcontacts'
        verbose_name_plural = 'clientcontact'

class MemberProducerStatus(models.Model):
    memberproducerstatus_id = models.AutoField(primary_key=True)
    memberproducerstatus = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.memberproducerstatus

    class Meta:
        verbose_name = 'memberproducerstatus'
        verbose_name_plural = 'memberproducerstatus'