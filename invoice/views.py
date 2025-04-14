from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from cloudinary.uploader import upload
from django.http import JsonResponse,FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.contrib.auth.models import User
from .models import InvoiceBill
from registration.models import Warehouse
from app1.models import Inventory
from transport.models import Transporter,Driver
from outbound.models import ReceiverSide
from django.conf import settings
from .utils.email_services import send_email_with_pdf
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import logging
from app1.decorators import jwt_required
logger = logging.getLogger(__name__)
# Create your views here.

def generate_invoice_pdf(user,Invoice_number):
    try:
        
        invoice = InvoiceBill.objects.filter(Invoice_number=Invoice_number,user=user)

        if not invoice.exists():
            return JsonResponse({"message": "Invoice not found"}, status=404)
        invoice = invoice.first()
        try:
         warehouse = Warehouse.objects.filter(user=user).first()
        except Exception as e:  
            return JsonResponse({"message": "Warehouse not found"}, status=404)
        receiver = ReceiverSide.objects.filter(user=user).first()
        transporter = Transporter.objects.filter(user=user).first()
        driver = Driver.objects.filter(Transporter__user=user).first()
    except InvoiceBill.DoesNotExist:
        return JsonResponse({"message": "Invoice not found"}, status=404)

    file_path = f'media/invoices/{invoice.Invoice_number}.pdf'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # HEADER
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(width / 2, height - 50, "INVOICE DETAILS")
    c.line(50, height - 60, 550, height - 60)

    # 🛠️ ADDING BILL NUMBER, DATE, GENERATED BY
    header_y = height - 100
    c.setFont("Helvetica", 11)
    c.drawString(50, header_y, f"Bill Number: {invoice.Bill_number}")
    c.drawString(50, header_y - 25, f"Bill Date: {invoice.Bill_time.strftime('%d-%m-%Y')}")
    c.drawString(50, header_y - 50, f"Generated By: {warehouse.WarehouseCompany_Name}")

    # PART-A (Starts after header section)
    part_a_start_y = header_y - 100
    line_spacing = 25  # More spacing between PART-A rows

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, part_a_start_y, "PART-A")
    part_a_data = [
    ["GSTIN Of Supplier:", getattr(warehouse, 'WarehouseGSTIN', '')],
    ["Place of Dispatch:", getattr(warehouse, 'WarehouseAddress', '')],
    ["GSTIN of Recipient:", getattr(receiver, 'Receiver_GSTIN', '')],
    ["Place of Receipt:", getattr(receiver, 'Receiver_Address', '')],
    ["Document Number:", getattr(invoice, 'Bill_number', '')],
    ["Value of Goods:", str(getattr(invoice, 'ValueOfGoods', ''))],
    ["Reason for Transport:", getattr(invoice, 'ReasonForTransport', '')],
    ["CEWB No:", str(getattr(invoice, 'CEWBno', ''))]
    ]

    y = part_a_start_y - 30
    for label, value in part_a_data:
      c.setFont("Helvetica-Bold", 10)
      c.drawString(50, y, label)
      c.setFont("Helvetica", 10)
      c.drawString(200, y, str(value))
      y -= line_spacing  # Increased spacing

    # PART-B
    part_b_start_y = y - 20  # Less gap between A and B
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, part_b_start_y, "PART-B")

# 🚀 FIX: Add Right Margin to Table
    table_width = 512  # Keeping 50px margin on left & right
    col_widths = [60, 80, 70, 110, 90, 50, 100]  # Adjusted for proper alignment

    formatted_entered_date = invoice.Bill_time.strftime('%d-%m-%Y %H:%M:%S') if invoice.Bill_time else 'N/A'  # Handle None case

    transport_data = [
     ["Mode", "Vehicle No", "From", "Entered Date", "Entered By", "CEWB No", "Multi Vehicle Info"],
     [
        str(receiver.ModeOfTransport or ''),
        str(driver.Vehicle_Number if driver else ''),  # Safe check for driver
        str(warehouse.WarehouseCity or ''),
        formatted_entered_date,  # Improved date format
        str(warehouse.WarehouseGSTIN or ''),
        str(invoice.CEWBno or ''),
        str(invoice.MultiVehInfo or '')
     ]
    ]


    table = Table(transport_data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1))  # 🚀 FIX: Wrap long text
    ]))

    # Draw table with margin from right
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, part_b_start_y - 50)  # Keeps 50px margin from the left

    c.save()
    # return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return file_path



# @csrf_exempt
# def automate_email(request):
#     inventory_obj = Inventory.objects.all()
#     try:
#         if( inventory_obj.status== 'OutofStock'):
#             Subject= "Automated mail to place order for the ${inventory_obj.ProductName}"
#             Warehouse = "${inventory_obj.Warehouse.WarehouseCompany_Name} System this side ," \
#             " We need to place the order for the ${inventory_obj.ProductName} to you , The Product Quantity will be ${inventory_obj.ProductRestock}" \
#             " We Hope you will reach us on this as soon as possible "
#             Recipient_list =["${inventory_obj.SendersSide.Sender_Email}"]
#             send_mail_warehouse(Subject,Warehouse,Recipient_list,settings.EMAIL_HOST_USER)

#     except Exception as e:
#         return JsonResponse({"message":"Invalid request"},status=400)

@csrf_exempt
@jwt_required
def getBillDetails(request):
   if request.method == "POST":
      try:
         user=request.user

         if not user.is_authenticated:
            return JsonResponse({"message": "User not authenticated"}, status=401)
         print(request.body)
         data = json.loads(request.body)


         Warehouse_obj = Warehouse.objects.filter(user=user).first()
         Transporter_obj = Transporter.objects.filter(user=user).first()
         Driver_obj = Driver.objects.filter(Transporter__user=user).first()
         Receiver_obj = ReceiverSide.objects.filter(user=user).first()
         invoice_obj = InvoiceBill.objects.create(
            Invoice_number = data.get("Invoice_number",""),
            Bill_validity = data.get("Bill_validity",""),
            ValueOfGoods = int(data.get("ValueOfGoods","")),
            ReasonForTransport = data.get("ReasonForTransport",""),
            CEWBno = int(data.get("CEWBno","")),
            MultiVehInfo = int(data.get("MultiVehInfo","")),
            user=user
         )

         invoice_pdf = generate_invoice_pdf(request.user,invoice_obj.Invoice_number)
         if invoice_pdf:
            invoice_url = upload_to_cloudinary(invoice_pdf)
            print(invoice_url)
            if invoice_url:
               invoice_obj.Bill_pdf = invoice_url
               invoice_obj.save()
         if not invoice_obj:
            return JsonResponse({"message":"Fail Fail Fail"},status=404)
         message = """Dear {receiver_name},

We have generated the Invoice Bill of our transaction. We want you to review the details, and we will begin processing your order shortly.

You will receive further updates as we proceed. If you have any questions, feel free to reach out to us.

Thank you for choosing our services.

Best Regards,  
{Warehouse_Name} Team  
📞 Contact: 98997975743  
📧 Email: supportTotal@gmail.com 
"""
         send_email_with_pdf(
            "Invoice Bill",
            message.format(                 
                  receiver_name=Receiver_obj.ReceiverCompany_Name,  
                  Warehouse_Name=Warehouse_obj.WarehouseCompany_Name),
                   [
        Receiver_obj.Receiver_Email,
        Warehouse_obj.WarehouseEmail,
        Transporter_obj.Transporter_Email,
        Driver_obj.Driver_Email
    ],
              invoice_pdf
            )
         return JsonResponse({"message":"Data fetched Successfully"},status=200)
      
      except AssertionError as e:
        logger.error(f"AssertionError occurred: {e}")
   else:
      return JsonResponse({"message":"Method Incorrect"},status=500)
   


def upload_to_cloudinary(file_path):
    try:
        response = upload(file_path, resource_type="raw")
        return response.get("url")  # Get the URL of the uploaded file
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None


@csrf_exempt
@jwt_required
def get_Details(request):
   if request.method=="GET":
      try:
         user=request.user
         if not user.is_authenticated:
            return JsonResponse({"message":"User not authenticated"},status=401)
         invoice_obj = InvoiceBill.objects.filter(user=user).order_by("-id")
         invoice_list = list(invoice_obj.values())
         return JsonResponse({"message":"Data sent successfully","data":invoice_list},status=200)
      except Exception as e:
         return JsonResponse({"message":"Error occurred","error":str(e)},status=400)
   else:
       return JsonResponse({"message":"Invalid request"},status=405)