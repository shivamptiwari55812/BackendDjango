from django.shortcuts import render
from invoice.models import InvoiceBill
from .models import ReceiverSide
from transport.models import Transporter,Driver
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .utils.email_service import send_mail,EmailMessage
from invoice.models import InvoiceBill
from transport.models import Transporter,Driver
from invoice.views import generate_invoice_pdf
import json
from app1.decorators import jwt_required
import logging
logger = logging.getLogger(__name__)
# Create your views here.
@csrf_exempt
@jwt_required
def submit_form_receiver(request):

    if request.method =='POST':

        
        try:

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            print(request.body)
            data = json.loads(request.body)

            Receiver_obj = ReceiverSide.objects.create(
                ReceiverCompany_Name = data.get("ReceiverCompany_Name",""),
                Receiver_Address =data.get("ReceiverCompany_Address",""),
                Receiver_City = data.get("ReceiverCompany_City",""),
                Receiver_GSTIN = data.get("ReceiverCompany_GSTIN",""),
                Receiver_State = data.get("ReceiverCompany_State",""),
                Receiver_Contact=data.get("ReceiverCompany_Contact",""),
                Receiver_Email =data.get("ReceiverCompany_Email",""),
                ModeOfTransport = data.get("ModeOfTransport",""),
                user=user
            )
            message = """Dear {receiver_name},

We have successfully received your outbound shipment request. Our team is now reviewing the details, and we will begin processing your order shortly.

You will receive further updates as we proceed. If you have any questions, feel free to reach out to us.

Thank you for choosing WarehouseMini!

Best Regards,  
WarehouseMini Team  
📞 Contact: 98997975743  
📧 Email: supportTotal@gmail.com 
"""

            send_mail(
                "Order Received /Confirmation Mail",
                message.format(
                    receiver_name=Receiver_obj.ReceiverCompany_Name,  
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data.get("ReceiverCompany_Email","")]

            )

            return JsonResponse({"message":"Data fetched Successully"},status =200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error":"Invalid request"},status=400)




@csrf_exempt
def getOrdersDetails(request):
    if request.method == "GET":
        try:
            invoice_obj = InvoiceBill.objects.all()
            receiver_obj = ReceiverSide.objects.all()
            receiver_list = list(receiver_obj.values())
            invoice_list = list(invoice_obj.values())
            
            return JsonResponse({"message":"Data sent successfully","invoices":invoice_list,"receiver":receiver_list},status=200)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({"message": "An error occurred while processing the request"}, status=500)
    else:
        return JsonResponse({"message":"Invalid request"},status=405)