from django.core.mail import send_mail
from django.conf import settings
def send_warehouse_email():
    subject ="This email is from django server and yk"
    message ="test message from django server email"
    from_email = settings.EMAIL_HOST_USER
    recipients = ["hanumanptiwari55812@gmail.com"]

    send_mail(subject, message, from_email, recipients)