from django.db import models
import uuid
from django.utils.timezone import now
from registration.models import Warehouse
class ReceiverSide(models.Model):
    ReceiverCompany_Name = models.CharField(max_length=100,null=True,blank=True)
    Receiver_Address = models.CharField(max_length=100)
    Receiver_City = models.CharField(max_length=30)
    Receiver_GSTIN = models.CharField(max_length=100)
    Receiver_State = models.CharField(max_length=100)
    Receiver_Contact = models.CharField(max_length=30)
    Receiver_Email = models.EmailField(max_length=100)
    ModeOfTransport = models.CharField(max_length=100,blank=True,null=True,default = 'By Road')  

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.ReceiverCompany_Name
    

