from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
from django.contrib.auth.models import User
import cloudinary
from app1.decorators import jwt_required
from .models import Warehouse,OTP
# Create your views here.


@csrf_exempt
@jwt_required
def warehouseSet(request):
    
    if request.method == 'POST':
        print("request received")
        try:

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            print(request.body)
            
            warehouse_name = request.POST.get("warehouseName")
            warehouse_address = request.POST.get("warehouseAddress")
            warehouse_city = request.POST.get("warehouseCity")
            warehouse_gstin = request.POST.get("warehouseGSTIN")
            warehouse_state = request.POST.get("warehouseState")
            warehouse_pincode = request.POST.get("warehousePincode")
            warehouse_contact = request.POST.get("warehouseContact")
            warehouse_type = request.POST.get("TypeOfWarehouse")
            warehouse_email = request.POST.get("warehouseEmail")
            document = request.FILES.get("document")

            result = cloudinary.uploader.upload(document)
            document_url = result['secure_url']

            Warehouse.objects.create(
                WarehouseCompany_Name=warehouse_name,
                WarehouseAddress=warehouse_address,
                WarehouseCity=warehouse_city,
                WarehouseGSTIN=warehouse_gstin,
                WarehouseState=warehouse_state,
                WarehousePincode=int(warehouse_pincode),
                WarehouseContact=warehouse_contact,
                WarehouseEmail=warehouse_email,
                WarehouseType=warehouse_type,
                document=document_url,
                user=user
            )

            return JsonResponse({"message":"Data saved Successfully"},status=200)
    
        except Exception as e:
          import traceback
          traceback.print_exc()  
          return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"Message":"Invalid request"},status=404)



def generate_and_store_otp(user):
    otp_code = random.randint(100000,999999)

    otp_instance =OTP.objects.create(user=user,code=str(otp_code))

    return otp_code

from django.forms.models import model_to_dict

@csrf_exempt
@jwt_required
def getDetails(request):
    if request.method == "GET":
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            
            warehouse_obj = Warehouse.objects.filter(user=user).first()
            if not warehouse_obj:
                return JsonResponse({"message": "Warehouse not found"}, status=404)
            
            # Convert the model instance to a dictionary
            warehouse_data = model_to_dict(warehouse_obj)
            
            return JsonResponse({"message": "Data sent successfully", "data": warehouse_data}, status=200)
        except Exception as e:
            return JsonResponse({"message": "Error occurred", "error": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid request"}, status=405)
