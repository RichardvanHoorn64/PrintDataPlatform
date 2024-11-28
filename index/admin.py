# Register your models here.
from django.contrib import admin
from index.models import *
from profileuseraccount.models import Languages, MemberPlans
from producers.models import ProducerProductOfferings

admin.site.register(MemberToProducerList)
admin.site.register(WhitelistEmail)
admin.site.register(BlacklistEmail)
admin.site.register(BlacklistDomains)
admin.site.register(Conditions)
admin.site.register(DropdownChoices)
admin.site.register(ProductCategory)
admin.site.register(Texts)
admin.site.register(Languages)
admin.site.register(MemberPlans)
admin.site.register(ProducerProductOfferings)