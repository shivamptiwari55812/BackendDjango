from django.conf import settings
from django.core.mail import send_mail
from registration.models import Warehouse
from outbound.models import ReceiverSide
from inbound.models import SendersSide

def send_mail_warehouse():
    subject = ""
    message =""
    from_email = settings.HOST_USER_NAME
    recipients = []

    send_mail(subject,message,from_email,recipients)