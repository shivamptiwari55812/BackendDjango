from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from app1.decorators import jwt_required
from django.conf import settings
from outbound.utils.email_service import send_mail
from outbound.models import ReceiverSide
from .models import Transporter , Driver ,Driver_Location
# Create your views here.

@csrf_exempt
@jwt_required
def getDetails(request):
    if request.method =="POST":
        try:
              
            user=request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            print(request.body)
            data =json.loads(request.body)
            Receiver_Email=data.get("Receiver_Email")
            

            if not Receiver_Email:
                return JsonResponse({"error": "Receiver email not provided"}, status=400)

            # Try to get the receiver by email and user
            try:
                receiver = ReceiverSide.objects.get(Receiver_Email=Receiver_Email, user=user)
            except ReceiverSide.DoesNotExist:
                return JsonResponse({"error": "Receiver not found"}, status=404)

           
            Transporter_obj = Transporter.objects.create(
                TransporterName = data.get("TransporterName",'None'),
                TransporterAddress = data.get("TransporterAddress"),
                Transporter_Contact = data.get("TransporterContact"),
                Transporter_Email = data.get("TransporterEmail"),
                user=user,
                receiver=receiver

            )
            Drivers_obj = Driver.objects.create(
                Driver_Name = data.get("DriverName"),
                Vehicle_Number = data.get("Vehicle_Number"),
                Driver_Contact = data.get("DriverContact"),
                Driver_Email = data.get("DriverEmail"),
                Transporter=Transporter_obj
            )

            return JsonResponse({"message":"Saved Successfully"},status=200)
        except Exception as e :
          import traceback
          traceback.print_exc()  
          return JsonResponse({"error": str(e)}, status=400)
        except:
            return JsonResponse({"message":"Not a valid Request"},status=400)
    
    return JsonResponse({"Invalid Error"},status=400)


# @csrf_exempt
# def Driverget(request):
#     if request.method == "POST":
#         try:
#             print(request.body)
#             data = json.loads(request.body)
#             # if not request.user.is_authenticated:
#             #   return JsonResponse({"message":"User not authenticated"},status=401)
 
#             Drivers_obj = Driver.objects.create(
#                 Driver_Name = data.get("DriverName"),
#                 Vehicle_Number = data.get("Vehicle_Number"),
#                 Driver_Contact = data.get("DriverContact"),
#                 Driver_Email = data.get("DriverEmail")
#             )
#             return JsonResponse({"message":"Saved Successfully"},status=200)
#         except Exception as e:
#             return JsonResponse({"message":"Invalid request"},status=400)
#     return JsonResponse({"message":"Invalid request"},status=400)
            

@csrf_exempt
def saveLocation(request):

    if request.method == 'POST':
     try:
         data = json.loads(request.body)
         print(data)

         driver_obj = Driver_Location.objects.create(
             latitude = data.get("latitude"),
             longitude = data.get("longitude"),
         )

         return JsonResponse({'Successfull data fetched'})

     except Exception as e:
         return JsonResponse({"message":"Invalid "})
    else:
        return JsonResponse({"Invalid request"})
    

@csrf_exempt
def send_email_to_driver(Driver_Email, token):
    # Construct the email content
    warehouse_obj = Warehouse.objects.filter(user=user).first();
    subject = "Delivery Verification"
    from_email = WarehouseEmail or settings.EMAIL_HOST_USER
    recipient_list = [Driver_Email]
    link = f"{settings.FRONTEND_URL}/delivery-verification/{token}"

    message = f"""
    <html>
        <body>
            <h2>Delivery Verification</h2>
            <p>Click the link below to proceed with the OTP verification:</p>
            <a href="{link}">Verify Delivery</a>
        </body>
    </html>
    """
    send_mail(subject, message, from_email, recipient_list, html_message=message)