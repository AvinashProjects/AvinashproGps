from django.db import models


# Create your models here.

class Deliveryboylctn(models.Model):
    ename = models.CharField(max_length=30)
    l_lat = models.DecimalField(max_digits=9, decimal_places=7)
    l_lon = models.DecimalField(max_digits=9, decimal_places=7)
    start_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.ename


# class Datereceived(models.Model):
#     daterecived = models.DateField(max_length=64)


class Orders(models.Model):
    order_name = models.CharField(max_length=64)
    order_lat = models.DecimalField(max_digits=9, decimal_places=7)
    order_lon = models.DecimalField(max_digits=9, decimal_places=7)
    deliverd_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.order_name
