from django.db import models
from registration.models import Warehouse
from transport.models import Transporter,Driver
from outbound.models import ReceiverSide
from inbound.models import SendersSide
import uuid
from django.db.models import URLField
from cloudinary.models import CloudinaryField
from django.utils.timezone import now
# Create your models here.
class InvoiceBill(models.Model):
    
    Invoice_number = models.CharField(max_length=100,null=False,blank=False,unique=True)
    Bill_date = models.DateField(auto_now_add=True)
    Bill_number = models.CharField(max_length=20,null=True,blank=True,unique=True)
    Bill_time = models.DateTimeField(auto_now=True)
    Bill_validity = models.DateTimeField()
    ValueOfGoods = models.IntegerField(default=0)
    ReasonForTransport = models.TextField()
    CEWBno = models.IntegerField()
    MultiVehInfo = models.IntegerField()
    Bill_pdf = URLField(null=True,blank=True)

    # Relationships
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,blank=True)

    receiver = models.ForeignKey(ReceiverSide, on_delete=models.CASCADE, null=True, blank=True)
    Sender = models.ForeignKey(SendersSide, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"Invoice {self.Invoice_number} - {self.Bill_number}"



    def save(self, *args, **kwargs):
        if not self.Bill_number:  
            self.Bill_number = self.generate_bill_number()
        super().save(*args, **kwargs)
    def generate_bill_number(self):
     return f"BILL-{now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

