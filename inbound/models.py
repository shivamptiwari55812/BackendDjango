from django.db import models
import uuid
from django.utils.timezone import now
from invoice.models import InvoiceBill


# Create your models here.
class SendersSide(models.Model):
    SenderCompany_Name = models.CharField(max_length=100)
    Sender_Address = models.CharField(max_length=100)
    Sender_City = models.CharField(max_length=30)
    Sender_Email = models.EmailField(max_length=100)

    # Relationship
    Invoice = models.ForeignKey(InvoiceBill, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.SenderCompany_Name
    
