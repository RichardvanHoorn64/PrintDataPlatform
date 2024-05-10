from django.db import models
from profileuseraccount.models import UserProfile, Members


class APIs(models.Model):
    api_id = models.AutoField(primary_key=True)
    api = models.CharField(max_length=200, default=0)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    member_id = models.ForeignKey(Members, null=True, blank=True, on_delete=models.SET_NULL)
    api_producer_id = models.PositiveIntegerField(null=True, blank=True)
    api_client_id = models.PositiveIntegerField(null=True, blank=True)
    producer = models.CharField(max_length=200)
    producer_api_key = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.producer

    class Meta:
        verbose_name = 'connections'
        verbose_name_plural = 'connection'
