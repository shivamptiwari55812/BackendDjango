from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import uuid
import json
# from app1.models import ReceiverSide, InvoiceBill ,Transporter,Driver,Warehouse
from invoice.models import InvoiceBill
from transport.models import Transporter,Driver
from registration.models import Warehouse
from inbound.models import SendersSide
from outbound.models import ReceiverSide
from .models import Inventory
from django.shortcuts import get_object_or_404
from .utils.email_service import send_warehouse_email


@csrf_exempt
def add_item_inventory(request):
   if request.method =='POST':
     try:
       data = json.loads(request.body)
       print(data)

       product_obj = Inventory.objects.create(
         ProductName = data.get("productName",""),
         ProductCategory =data.get("productCategory",""),
         ProductQuantity = int(data.get("productQuantity",0)),
         ProductPrice =float(data.get("productPrice",0)),
         Product_Rejected = int(data.get("productRejected",0)),
         Transaction_type = data.get("TransactionType",""),
         ProductRestock = data.get("productRestock",0),
       )

       return JsonResponse({"message":"Saved Successfully"},status=200)
     except Exception as e:
      print("Error:", e)  
      return JsonResponse({"error": str(e)}, status=400)  

   return JsonResponse({"message":"Invalid Response"},status =400)

@csrf_exempt
def del_product_inventory(request):
    if request.method == 'DELETE':
        try:
           data = json.loads(request.body)
           print(data)
           Product_Name = data.get("")
           product_obj = Inventory.objects.filter(ProductName=Product_Name).first()

           if not Product_Name:
            return JsonResponse({"message":"Product not found"},status=404)   

           product_obj.delete()
           return JsonResponse({"message":"Product deleted successfully"},status=200)
        except Exception as e:
            return JsonResponse({"message":"Invalid request"},status=400)
                 
           
    return JsonResponse({"message":"Invalid request"},status=400)

@csrf_exempt
def edit_product_inventory(request):
    if request.method == 'PUT':
       try:
          data = json.loads(request.body)
          print(data)

          product_Name = data.get("productName")

          product_obj = Inventory.objects.filter(ProductName=product_Name).first()

          if not product_obj:
             return JsonResponse ({"message":"Product not found"},status =404)
          
          product_obj.ProductName = data.get("productName",product_obj.ProductName)
          product_obj.ProductCategory = data.get("productCategory",product_obj.ProductCategory) 
          product_obj.ProductQuantity = data.get("productQuantity",product_obj.ProductQuantity) 
          product_obj.ProductPrice = data.get("productPrice",product_obj.ProductPrice)
          product_obj.Product_Rejected = data.get("productRejected",product_obj.Product_Rejected)
          product_obj.Transaction_type = data.get("transactionType",product_obj.Transaction_type)
          product_obj.save()
          return JsonResponse({"message":"Product updated successfully"},status=200)
       except Exception as e:
          return JsonResponse({"message":"Invalid request"},status=400)
    return JsonResponse({"message":"Invalid request"},status=400)


@csrf_exempt
def get_product_details(request):

   if request.method == "GET":
      try:
         products_obj = Inventory.objects.all()
         product_list = list(products_obj.values())
         return JsonResponse({"message":"Data sent successfully","data":product_list},status=200)
      except Exception as e:
         return JsonResponse({"message":"Invalid request"},status=400)
   else:
      return JsonResponse({"message":"Invalid request"},status=400)

@csrf_exempt   
def get_product_foredit(request, product_id):  # ✅ Accept product_id here
    product = get_object_or_404(Inventory, id=product_id)  # ✅ Lookup by ID

    return JsonResponse({
        "ProductName": product.ProductName,
        "ProductPrice": float(product.ProductPrice),
        "ProductQuantity": product.ProductQuantity,
        "Product_Rejected": product.Product_Rejected,
        "ProductRestock": product.ProductRestock,
        "ProductCategory": product.ProductCategory,
        "Transaction_type": product.Transaction_type,
    })

def sent_notification(request):
   send_warehouse_email()
   return JsonResponse({"message":"Email sent successfully"},status=200)

