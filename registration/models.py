from django.db import models
import uuid
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Warehouse(models.Model):
    WarehouseCompany_Name = models.CharField(max_length=200,null=False,blank=False)
    WarehouseAddress = models.CharField(max_length=100)
    WarehouseCity = models.CharField(max_length=30)
    WarehouseGSTIN = models.CharField(max_length=100)
    WarehouseState = models.CharField(max_length=100)
    WarehousePincode = models.IntegerField()
    WarehouseContact = models.CharField(max_length=30)
    WarehouseEmail = models.EmailField(max_length=100)
    WarehouseType = models.CharField(max_length=100)
    WarehouseCapacity = models.IntegerField()
    WarehouseAvailable = models.BooleanField(default=True)

    User = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"WarehouseCompany_Name: {self.WarehouseCompany_Name}"