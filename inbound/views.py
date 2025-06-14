from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SendersSide
from outbound.utils.email_service import send_mail,EmailMessage
from django.views.decorators.csrf import csrf_exempt
import logging
from registration.models import Warehouse
from django.conf import settings
from warehouseminiBack.jwt_utils import decode_jwt
from app1.decorators import jwt_required
logger = logging.getLogger(__name__)
from django.utils import timezone
from datetime import datetime

# Create your views here.
def recordInbound(request):
   
    return request("Hello")


@csrf_exempt
@jwt_required
def orderForm(request):
    if request.method == "POST":
        try:
            user=request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            data = json.loads(request.body)
            print(data)
            
            expected_date_str = data.get("Expected_date")
            expected_date_obj = timezone.make_aware(datetime.strptime(expected_date_str, "%Y-%m-%d")) if expected_date_str else None
           
            warehouse_obj = Warehouse.objects.filter(user=user).first() 
            sender_obj = SendersSide.objects.create(
                SenderCompany_Name = data.get("SenderCompany_Name",""),
                Sender_Address = data.get("SenderCompany_Address",""),
                Sender_City = data.get("SenderCompany_City",""),
                Sender_Email = data.get("SenderCompany_Email",""),
                ProductName = data.get("productName",""),
                ProductQuantity = int(data.get("productQuantity","")),
                Expected_Date = expected_date_obj,
                user=user
                
            )

            message = """Dear {SenderCompany_Name},

Greetings from {Warehouse_name}!
This is a system generated related email from our side for booking the order of "{ProductName}" with quantity of "{ProductQuantity}".
We Hope you will soon reach us with your quoatation on our official Email address {Warehouse_Email}.

Best Regards,  
{Warehouse_name} Team  
📞 Contact: 98997975743  
📧 Email: supportTotal@gmail.com 
"""

            send_mail(
                "Order Received /Confirmation Mail",
                message.format(
                    SenderCompany_Name=sender_obj.SenderCompany_Name, 
                    Warehouse_name =warehouse_obj.WarehouseCompany_Name, 
                    Warehouse_Email =warehouse_obj.WarehouseEmail,
                    ProductName =sender_obj.ProductName,
                    ProductQuantity =sender_obj.ProductQuantity
                ),
                from_email=Warehouse.objects.first().WarehouseEmail,
                recipient_list=[data.get("SenderCompany_Email","")]

            )

            return JsonResponse({"message":"Data saved Successfully"},status=200)
        except json.JSONDecodeError as e:
            # Log the error
            logger.error(f"JSONDecodeError: {e}")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}") 
            return JsonResponse({"message":"Invalid request"},status=400)   
    else:
     return JsonResponse({"message":"Invalid request"},status=405)
    
