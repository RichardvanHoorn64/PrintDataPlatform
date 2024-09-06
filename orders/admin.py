from django.contrib import admin
from orders.models import Orders, OrderStatus

admin.site.register(OrderStatus)
admin.site.register(Orders)

