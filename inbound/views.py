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
            
            # Check for missing required fields BEFORE creating the object
            required_fields = ["SenderCompany_Name", "SenderCompany_Address", "SenderCompany_City", "SenderCompany_Email","productQuantity"]  # Include the fields you consider required
            if not all(field in data for field in required_fields):  # Check presence
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            warehouse_obj = Warehouse.objects.filter(user=user).first() 
            sender_obj = SendersSide.objects.create(
                SenderCompany_Name = data.get("SenderCompany_Name",""),
                Sender_Address = data.get("SenderCompany_Address",""),
                Sender_City = data.get("SenderCompany_City",""),
                Sender_Email = data.get("SenderCompany_Email",""),
                ProductName = data.get("productName",""),
                ProductQuantity = int(data.get("productQuantity","")),
                user=user
                # Expected_Date = data.get("Expected_Date"),
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
                    receiver_name=sender_obj.SenderCompany_Name, 
                    Warehouse_name =warehouse_obj.WarehouseCompany_Name, 
                    Warehouse_Email =warehouse_obj.WarehouseEmail,
                    ProductName =sender_obj.productName,
                    ProductQuantity =sender_obj.productQuantity
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data.get("SenderCompany_Email","")]

            )

            if not all(sender_obj):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            return JsonResponse({"message":"Data saved Successfully"},status=200)
        except json.JSONDecodeError as e:
            # Log the error
            logger.error(f"JSONDecodeError: {e}")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"message":"Invalid request"},status=400)   
    else:
     return JsonResponse({"message":"Invalid request"},status=405)