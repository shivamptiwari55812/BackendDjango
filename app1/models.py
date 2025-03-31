from django.db import models
import uuid
from django.utils.timezone import now
from registration.models import Warehouse


class Inventory(models.Model):
    INBOUND = 'Inbound'
    OUTBOUND = 'Outbound'
    TRANSACTION_CHOICES = [(INBOUND, 'Inbound'), (OUTBOUND, 'Outbound')]
    STATUS_CHOICES = [
        ('InStock', 'In Stock'),
        ('LowStock', 'Low Stock'),
        ('OutofStock', 'Out of Stock'),
    ]   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True,default='InStock')
    ProductName = models.CharField(max_length=100)
    ProductCategory = models.CharField(max_length=100, null=False, blank=False)
    ProductQuantity = models.IntegerField(null=False, blank=False)
    ProductPrice = models.FloatField()
    Product_Rejected = models.IntegerField(null=False, blank=False)
    Transaction_type =  models.CharField(max_length=30 ,choices=TRANSACTION_CHOICES,default="Inbound")
    ProductRestock = models.IntegerField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs): 
        if self.ProductQuantity > 70:
            self.status = "InStock"
        elif self.ProductQuantity > 30:
            self.status = "LowStock"
        else:
            self.status = "OutofStock"
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.ProductName




