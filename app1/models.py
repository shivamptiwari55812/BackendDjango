from django.db import models
import uuid
from django.utils.timezone import now

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


    def __str__(self):
        return f"WarehouseCompany_Name: {self.WarehouseCompany_Name}"


class ReceiverSide(models.Model):
    ReceiverCompany_Name = models.CharField(max_length=100,null=True,blank=True)
    Receiver_Address = models.CharField(max_length=100)
    Receiver_City = models.CharField(max_length=30)
    Receiver_GSTIN = models.CharField(max_length=100)
    Receiver_State = models.CharField(max_length=100)
    Receiver_Contact = models.CharField(max_length=30)
    Receiver_Email = models.EmailField(max_length=100)

    def __str__(self):
        return self.ReceiverCompany_Name





class Inventory(models.Model):
    ProductName = models.CharField(max_length=100)
    ProductCategory = models.CharField(max_length=100, null=False, blank=False)
    ProductQuantity = models.IntegerField(null=False, blank=False)
    ProductPrice = models.FloatField()
    Product_Rejected = models.IntegerField()
    InBoundreadyProduct = models.IntegerField()
    OutBoundreadyProduct = models.IntegerField()
   


    # Relationship
    Warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.ProductName


class Transporter(models.Model):
    TransporterName = models.CharField(max_length=100,null=True,blank=True)
    TransporterAddress = models.CharField(max_length=100,null=True,blank=True)
    Transporter_Contact = models.CharField(max_length=30)
    Transporter_Email = models.EmailField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.TransporterName


class Driver(models.Model):
    Driver_Name = models.CharField(max_length=100,null=False,blank=False)
    # Driver_Id = models.CharField(auto_created=True)
    Driver_Contact = models.CharField(max_length=20)
    Driver_Email = models.EmailField(max_length=100,null=True,blank=True)
    Vehicle_Number = models.CharField(max_length=100, null=True, blank=True)
    Driver_Location = models.CharField(max_length=100,null=True,blank=True)

    # Relationship
    Transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.Driver_Name




class InvoiceBill(models.Model):
    
    Invoice_number = models.CharField(max_length=100)
    Bill_date = models.DateField(auto_now_add=True)
    Bill_number = models.IntegerField(null=True,blank=True)
    Bill_time = models.DateTimeField(auto_now=True)
    Bill_validity = models.DateField()
    ValueOfGoods = models.IntegerField(default=0)
    ReasonForTransport = models.TextField()
    CEWBno = models.IntegerField()
    MultiVehInfo = models.IntegerField()
    Bill_pdf = models.FileField(upload_to='bills/', default='default_bill.pdf')

    # Relationships
    Warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,null=True,blank=True)
    Receiver = models.ForeignKey(ReceiverSide, on_delete=models.CASCADE,null=True,blank=True)
    Transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE,null=True,blank=True)
    Driver = models.ForeignKey(Driver, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"Invoice {self.Invoice_number} - {self.Bill_number}"



def save(self, *args, **kwargs):
        if not self.Bill_number:  
            self.Bill_number = self.generate_bill_number()
        super().save(*args, **kwargs)
def generate_bill_number():
    return f"BILL-{now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"




class SendersSide(models.Model):
    SenderCompany_Name = models.CharField(max_length=100)
    Sender_Address = models.CharField(max_length=100)
    Sender_City = models.CharField(max_length=30)
    Sender_Email = models.EmailField(max_length=100)

    # Relationship
    Invoice = models.ForeignKey(InvoiceBill, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.SenderCompany_Name