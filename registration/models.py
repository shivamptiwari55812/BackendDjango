from django.db import models
import uuid
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import timedelta
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.db.models import URLField
# Create your models here.
class Warehouse(models.Model):
    WarehouseCompany_Name = models.CharField(max_length=200,null=False,blank=False)
    WarehouseAddress = models.CharField(max_length=100)
    WarehouseCity = models.CharField(max_length=30)
    WarehouseGSTIN = models.CharField(max_length=15)
    WarehouseState = models.CharField(max_length=100)
    WarehousePincode = models.IntegerField()
    WarehouseContact = models.CharField(max_length=30)
    WarehouseEmail = models.EmailField(max_length=100)
    WarehouseType = models.CharField(max_length=100)
    document = URLField(null=True,blank=True)


    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"WarehouseCompany_Name: {self.WarehouseCompany_Name}"
    
class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add = True)

    def is_expired(self):
        """Check if the OTP has expired (e.g., after 10 minutes)."""
        expiration_time = self.created_at + timedelta(minutes = 10)
        return expiration_time < timezone.now()