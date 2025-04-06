from django.shortcuts import render
from invoice.models import InvoiceBill
from .models import ReceiverSide
from transport.models import Transporter,Driver
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .utils.email_service import send_mail,EmailMessage
from invoice.views import generate_invoice_pdf
import json
# Create your views here.
@csrf_exempt
def submit_form_receiver(request):

    if request.method =='POST':

        
        try:
            print(request.body)
            data = json.loads(request.body)

            # if not request.user.is_authenticated:
            #  return JsonResponse({"message":"User not authenticated"},status=401)

            

            Receiver_obj = ReceiverSide.objects.create(
                ReceiverCompany_Name = data.get("receiverCompanyName",""),
                Receiver_Address =data.get("receiverCompanyAddress",""),
                Receiver_City = data.get("receiverCompanyCity",""),
                Receiver_GSTIN = data.get("receiverCompanyGSTIN",""),
                Receiver_State = data.get("receiverCompanyState",""),
                Receiver_Contact=data.get("receiverCompanyContact",""),
                Receiver_Email =data.get("receiverCompanyEmail","")
                 )
           
            message = """Dear {receiver_name},

We have successfully received your outbound shipment request. Our team is now reviewing the details, and we will begin processing your order shortly.

You will receive further updates as we proceed. If you have any questions, feel free to reach out to us.

Thank you for choosing WarehouseMini!

Best Regards,  
WarehouseMini Team  
📞 Contact: 98997975743  
📧 Email: supportTotal@gmail.com 
"""

            send_mail(
                "Order Received /Confirmation Mail",
                message.format(
                    receiver_name=Receiver_obj.ReceiverCompany_Name,  
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data.get("receiverCompanyEmail","")]

            )

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
           
            pdf_file = generate_invoice_pdf(data.get("invoiceNumber","")) 
            print(pdf_file)
            return JsonResponse({"message":"Data fetched Successully","pdf-file":pdf_file},status =200)
        
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
    

def automate_pdf_email(invoice_number):
    try:
        invoice_obj = InvoiceBill.objects.filter(Invoice_number=invoice_number).first()
        receiver_obj = ReceiverSide.objects.filter(ReceiverCompany_Email=invoice_obj.ReceiverCompany_Email).first()
        # pdf_file = generate_invoice_pdf(invoice_number)
        # file_path = f'media/invoices/{invoice_obj.Invoice_number}.pdf'
        email = EmailMessage(
            "Invoice PDF",
            "Please find the attached invoice PDF file.",
            from_email=settings.EMAIL_HOST_USER,
            to=[receiver_obj.ReceiverCompany_Email],
        )

        # email.attach_file(pdf_file)
        email.send()
        return JsonResponse({"message":"Email sent successfully"},status=200)   

    except Exception as e:
        return JsonResponse({"message":"Invalid request"},status=400)

