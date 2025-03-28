from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Warehouse
# Create your views here.


@csrf_exempt
def warehouseSet(request):
    
    if request.method == 'POST':
        print("request received")
        try:
            print(request.body)
            data = json.loads(request.body)

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
