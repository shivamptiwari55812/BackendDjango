from django.db import models
from registration.models import Warehouse
from transport.models import Transporter,Driver
from outbound.models import ReceiverSide
import uuid
from django.utils.timezone import now
# Create your models here.
class InvoiceBill(models.Model):
    
    Invoice_number = models.CharField(max_length=100,null=False,blank=False)
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

