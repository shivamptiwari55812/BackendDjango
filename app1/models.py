from django.db import models
import uuid
from django.utils.timezone import now
from registration.models import Warehouse


class Inventory(models.Model):
    INBOUND = 'Inbound'
    OUTBOUND = 'Outbound'
    TRANSACTION_CHOICES = [(INBOUND, 'Inbound'), (OUTBOUND, 'Outbound')]
    ProductName = models.CharField(max_length=100)
    ProductCategory = models.CharField(max_length=100, null=False, blank=False)
    ProductQuantity = models.IntegerField(null=False, blank=False)
    ProductPrice = models.FloatField()
    Product_Rejected = models.IntegerField(null=False, blank=False)
    Transaction_type =  models.CharField(max_length=30 ,choices=TRANSACTION_CHOICES,default="Inbound")

  
    def __str__(self):
        return self.ProductName






