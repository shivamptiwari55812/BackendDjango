from django.conf import settings
from django.core.mail import send_mail
from registration.models import Warehouse
from outbound.models import ReceiverSide
from inbound.models import SendersSide

from django.core.mail import EmailMessage

def send_email_with_pdf(subject, body, recipient_email, pdf_path):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=Warehouse.objects.first().WarehouseEmail,  
        to=recipient_email,            
    )
    email.attach_file(pdf_path)
    email.send()
