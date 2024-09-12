# Register your models here.
from django.contrib import admin
from index.models import Blacklist, Conditions, DropdownChoices, ProductCategory, Texts, Whitelist
from profileuseraccount.models import Languages, MemberPlans
from producers.models import ProducerProductOfferings

admin.site.register(Blacklist)
admin.site.register(Conditions)
admin.site.register(DropdownChoices)
admin.site.register(ProductCategory)
admin.site.register(Texts)
admin.site.register(Whitelist)

admin.site.register(Languages)
admin.site.register(MemberPlans)

admin.site.register(ProducerProductOfferings)