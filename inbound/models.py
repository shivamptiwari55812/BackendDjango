from django.db import models
import uuid
from django.utils.timezone import now
# from invoice.models import InvoiceBill
from registration.models import Warehouse
from django.utils import timezone

# Create your models here.
class SendersSide(models.Model):
    SenderCompany_Name = models.CharField(max_length=100)
    Sender_Address = models.CharField(max_length=200)
    Sender_City = models.CharField(max_length=30)
    Sender_Email = models.EmailField(max_length=100)
    ProductName = models.CharField(max_length=100,null=True,blank=True)
    ProductQuantity = models.IntegerField(null=True,blank=True)
    Expected_Date = models.DateTimeField(blank=True,null=True) 

    # Relationship
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.SenderCompany_Name
    
