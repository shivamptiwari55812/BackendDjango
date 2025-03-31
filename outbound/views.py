from django.shortcuts import render
from invoice.models import InvoiceBill
from .models import ReceiverSide
from transport.models import Transporter,Driver
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.
@csrf_exempt
def submit_form_receiver(request):

    if request.method =='POST':
        try:
            print(request.body)
            data = json.loads(request.body)
            

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
def get_details_bill(request):

    if request.method == "GET":
        try:
            bill_obj = InvoiceBill.objects.all()
            receiver_obj = ReceiverSide.objects.all()
            receiver_list = list(receiver_obj.values())
            bill_list = list(bill_obj.values())
          
            return JsonResponse({"message":"Data sent successfully","data":{"receivers": receiver_list, "bills": bill_list}},status=200)
        except Exception as e:
            return JsonResponse({"message":"Invalid request"},status=400)
    else:
        return JsonResponse({"message":"Invalid request"},status=400)