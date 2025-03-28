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

