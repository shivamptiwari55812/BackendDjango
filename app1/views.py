from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import uuid
import json
from app1.models import ReceiverSide, InvoiceBill ,Transporter,Driver,Warehouse


# //for the outbound record

def recordOutbound(request):
    Invoicebill =InvoiceBill.objects.all()

    context ={
        'Invoicebill':Invoicebill,
    }
    return render(request , 'recordout.html',context)

        

#for the receiving of the data



def generate_bill_number():
    return f"BILL-{now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


@csrf_exempt
def submit_form_receiver(request):

    if request.method =='POST':
        try:
            print(request.body)
            data = json.loads(request.body)
            data = data.get('formData')
            

            Receiver_obj = ReceiverSide.objects.create(
                ReceiverCompany_Name = data.get("receiverCompanyName",""),
                Receiver_Address =data.get("receiverCompanyAddress",""),
                Receiver_City = data.get("receiverCompanyCity",""),
                Receiver_GSTIN = data.get("receiverCompanyGSTIN",""),
                Receiver_State = data.get("receiverCompanyState",""),
                Receiver_Contact=data.get("receiverCompanyContact",""),
                Receiver_Email =data.get("receiverCompanyEmail","")
                 )
            
            
            print(Receiver_obj)

            InvoiceBill_obj = InvoiceBill.objects.create(
                Invoice_number= data.get("invoiceNumber"),
                ReasonForTransport= data.get("reasonForTransport",""),
                MultiVehInfo = data.get("multiVehInfo",0),
                CEWBno =data.get("cewbNo",0),
                ValueOfGoods = data.get("valueOfGoods",0),
                Bill_validity = data.get("ValidityBill","")
                 )

            Transporter_obj = Transporter.objects.create(
                TransporterName = data.get("TransporterName","")
                )

            Driver_obj = Driver.objects.create(
                Vehicle_Number = data.get("vehicleNumber","MH7804")
                )
            return JsonResponse({"message":"Data fetched Successully"},status =200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error":"Invalid request"},status=400)


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

@csrf_exempt
def TransporterSet(request):
    if request.method =="POST":
        try:
            print(request.body)
            data =json.loads(request.body)
            Transporter_obj = Transporter.objects.create(
                TransporterName = data.get("TransporterName "),
                TransporterAddress = data.get("TransporterAddress"),
                Transporter_Contact = data.get("TransporterContact"),
                Transporter_Email = data.get("TransporterEmail")
            )

            return JsonResponse({"message":"Saved Successfully"},status=200)
        except Exception as e :
            return JsonResponse({"message":"Not a valid Request"},status=400)
    
    return JsonResponse({"Invalid Error"},status=400)



# //For tableOut



def get_inventory_data(request):
    
     invoice_data = list(InvoiceBill.objects.values())  
     receiver_data = list(ReceiverSide.objects.values())  

     combined_data = {
        'invoice_data': invoice_data,
        'receiver_data': receiver_data
    }
    #  print(combined_data)
     return JsonResponse({'combined_data':combined_data})










