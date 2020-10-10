from django.contrib import admin
from .models import *
# Register your models here.

class AdminDeliveryboylctn(admin.ModelAdmin):
    list_display = ['ename']

class AdminOrders(admin.ModelAdmin):
    list_display = ['order_name']

admin.site.register(Deliveryboylctn,AdminDeliveryboylctn)
admin.site.register(Orders,AdminOrders)
