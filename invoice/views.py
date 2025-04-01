from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import JsonResponse,FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from .models import InvoiceBill
from registration.models import Warehouse
from app1.models import Inventory
from transport.models import Transporter,Driver
from outbound.models import ReceiverSide
from django.conf import settings
from .utils.email_services import send_mail_warehouse
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
# Create your views here.
# @csrf_exempt
def generate_invoice_pdf(request, Invoice_number):
    try:
        invoice = InvoiceBill.objects.get(Invoice_number=Invoice_number)
        warehouse = Warehouse.objects.first()
        receiver = ReceiverSide.objects.first()
        transporter = Transporter.objects.first()
        driver = Driver.objects.first()
    except InvoiceBill.DoesNotExist:
        return JsonResponse({"message": "Invoice not found"}, status=404)

    file_path = f'media/invoices/{invoice.Bill_number}.pdf'
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
        ["GSTIN Of Supplier:", warehouse.WarehouseGSTIN],
        ["Place of Dispatch:", warehouse.WarehouseAddress],
        ["GSTIN of Recipient:", receiver.Receiver_GSTIN],
        ["Place of Receipt:", receiver.Receiver_Address],
        ["Document Number:", invoice.Bill_number],
        ["Value of Goods:", str(invoice.ValueOfGoods)],
        ["Reason for Transport:", invoice.ReasonForTransport],
        ["CEWB No:", str(invoice.CEWBno)]
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

    formatted_entered_date = invoice.Bill_time.strftime('%d-%m-%Y %H:%M:%S')  # Improved Date Format

    transport_data = [
        ["Mode", "Vehicle No", "From", "Entered Date", "Entered By", "CEWB No", "Multi Vehicle Info"],
        [
            str(receiver.ModeOfTransport or ''),
            str(driver.Vehicle_Number or ''),
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
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

# @csrf_exempt
# def get_invoice_pdf(request,invoice_id):
     
#      file_path = generate_invoice_pdf(invoice_id)

#      if file_path:
#          return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#      else:
#          return JsonResponse({'error': 'Invoice not found'}, status=404)
     

@csrf_exempt
def automate_email(request):
    inventory_obj = Inventory.objects.all()
    try:
        if( inventory_obj.status== 'OutofStock'):
            Subject= "Automated mail to place order for the ${inventory_obj.ProductName}"
            Warehouse = "${inventory_obj.Warehouse.WarehouseCompany_Name} System this side ," \
            " We need to place the order for the ${inventory_obj.ProductName} to you , The Product Quantity will be ${inventory_obj.ProductRestock}" \
            " We Hope you will reach us on this as soon as possible "
            Recipient_list =["${inventory_obj.SendersSide.Sender_Email}"]
            send_mail_warehouse(Subject,Warehouse,Recipient_list,settings.EMAIL_HOST_USER)

    except Exception as e:
        return JsonResponse({"message":"Invalid request"},status=400)