from django.conf import settings
from django.core.mail import send_mail , EmailMessage

def send_Warehouse_mail(subject,message,to):
    from_email = settings.EMAIL_HOST_USER
    

    EmailMessage(subject,message,from_email,to)