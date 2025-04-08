from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
from .models import Warehouse,OTP
# Create your views here.


@csrf_exempt
def warehouseSet(request):
    
    if request.method == 'POST':
        print("request received")
        try:
            print(request.body)
            data = json.loads(request.body)

            # if not request.user.is_authenticated:
            #  return JsonResponse({"message":"User not authenticated"},status=401)


            warehouse_obj =Warehouse.objects.create(
            WarehouseCompany_Name=data.get("warehouseName"),
            WarehouseAddress=data.get("warehouseAddress"),
            WarehouseCity =data.get("warehouseCity"),
            WarehouseGSTIN = data.get("warehouseGSTIN"),
            WarehouseState =data.get("warehouseState"),
            WarehouseContact = data.get("warehouseContact"),
            WarehouseEmail = data.get("warehouseEmail"),
            WarehousePincode =data.get("warehousePincode"),
            WarehouseType = data.get("TypeOfWarehouse"),
            WarehouseCapacity = data.get("warehouseCapacity"),
            WarehouseAvailable = data.get("warehouseAvailable")
         )

            return JsonResponse({"message":"Data saved Successfully"},status=200)
    
        except Exception as e:
            return JsonResponse({"error":"Invalid shit"},status=400)
        
    return JsonResponse({"Message":"Invalid request"},status=404)



def generate_and_store_otp(user):
    otp_code = random.randint(100000,999999)

    otp_instance =OTP.objects.create(user=user,code=str(otp_code))

    return otp_code