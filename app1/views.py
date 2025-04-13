from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import uuid
import json
from django.db.models import Sum
from invoice.models import InvoiceBill
from transport.models import Transporter,Driver
from registration.models import Warehouse
from inbound.models import SendersSide
from outbound.models import ReceiverSide
from .models import Inventory
from django.contrib.auth.models import User
from .decorators import jwt_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .utils.email_service import send_warehouse_email


@csrf_exempt
@jwt_required
def add_item_inventory(request):
   if request.method =='POST':
     try:
       user=request.user

       if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)

       data = json.loads(request.body)
       print(data)
      #  if not request.user.is_authenticated:
      #     return JsonResponse({"message":"User not authenticated"},status=401)
      
      #  Warehouse = Warehouse.objects.get(user=request.user)
       product_obj = Inventory.objects.create(
         ProductName = data.get("productName",""),
         ProductCategory =data.get("productCategory",""),
         ProductQuantity = int(data.get("productQuantity",0)),
         ProductPrice =float(data.get("productPrice",0)),
         Product_Rejected = int(data.get("ProductRejected",0)),
         Transaction_type = data.get("transactionType",""),
         ProductRestock = data.get("productRestock",0),
         user=user
       )

       return JsonResponse({"message":"Saved Successfully"},status=200)
     except Exception as e:
      print("Error:", e)  
      return JsonResponse({"error": str(e)}, status=400)  

   return JsonResponse({"message":"Invalid Request"},status =401)

@csrf_exempt
@jwt_required
def del_product_inventory(request):
    if request.method == 'DELETE':
        try:
           
           user = request.user
           if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)

           data = json.loads(request.body)
           print(data)
        
           product_id= data.get("id")
           product_obj = Inventory.objects.filter(id = product_id,user=user).first()

           if not product_obj:
            return JsonResponse({"message":"Product not found"},status=404)   

           product_obj.delete()
           return JsonResponse({"message":"Product deleted successfully"},status=200)
        except Exception as e:
            return JsonResponse({"message":"Invalid request"},status=400)
                 
           
    return JsonResponse({"message":"Invalid request"},status=405)

@csrf_exempt
@jwt_required
def edit_product_inventory(request):
    if request.method == 'PUT':
       try:
          
          user= request.user
          if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
          data = json.loads(request.body)
          print(data)

          product_id = request.GET.get('product_id')

          product_obj = Inventory.objects.filter(id=product_id,user=user).first()

          if not product_obj:
             return JsonResponse ({"message":"Product not found"},status =404)
          
          product_obj.ProductName = data.get("ProductName",product_obj.ProductName)
          product_obj.ProductCategory = data.get("ProductCategory",product_obj.ProductCategory) 
          product_obj.ProductQuantity = int(data.get("ProductQuantity",product_obj.ProductQuantity)) 
          product_obj.ProductPrice = float(data.get("ProductPrice",product_obj.ProductPrice))
          product_obj.Product_Rejected = int(data.get("ProductRejected",product_obj.Product_Rejected))
          product_obj.ProductRestock = int(data.get("ProductRestock",product_obj.ProductRestock))
          product_obj.Transaction_type = data.get("TransactionType",product_obj.Transaction_type)
          product_obj.save()
          return JsonResponse({"message":"Product updated successfully"},status=200)
       except Exception as e:
          return JsonResponse({"message":"Invalid request"},status=400)
    return JsonResponse({"message":"Invalid request"},status=405)


@csrf_exempt
@jwt_required
def get_product_details(request):

   if request.method == "GET":
      try:

         user = request.user
         if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
         products_obj = Inventory.objects.filter(user=user)
         product_list = list(products_obj.values())
         return JsonResponse({"message":"Data sent successfully","data":product_list},status=200)
      except Exception as e:
         return JsonResponse({"message":"Invalid request"},status=400)
   else:
      return JsonResponse({"message":"Invalid request"},status=405)

@csrf_exempt
@jwt_required  
def get_product_foredit(request): 
    user=request.user
    if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
    product_id = request.GET.get("product_id")
    if not product_id:
       return JsonResponse({"error": "Product ID is required"}, status=400)
    product = get_object_or_404(Inventory, id=product_id,user=user)  

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



@csrf_exempt
@jwt_required
def totalItems(request):
 try:
   if request.method == "GET":
      user=request.user
      if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
      total_items = Inventory.objects.aggregate(total_items=Sum('ProductQuantity'))
      print(total_items)
      if total_items is None:
         return JsonResponse({"total_items": 0}, status=200)
      else:
         return JsonResponse({"total_items": total_items}, status=200)   
   else:
      return JsonResponse({"error": "Invalid request"}, status=400)
 except Exception as e:
    return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)