from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import JsonResponse,FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from .models import InvoiceBill
# Create your views here.


def generate_invoice_pdf(invoice_id):
    try:
     invoice =InvoiceBill.objects.get(id = invoice_id)
    except InvoiceBill.DoesNotExist:
     return None
   
    file_path = f'media/invoices/{invoice.Bill_number}.pdf'
    
    c= canvas.Canvas(file_path, pagesize=letter)
    width,height = letter
    c.setFont('Helvetica-Bold',14)

    c.drawString(200, height-50, invoice.Bill_number)
    c.line(50 , height - 60 ,550 ,height -60)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50,height -90,"PART-A")

    c.setFont("Helvetica",10)
    c.drawString(50,height-110,f"GSTIN Of Supplier:{invoice.Warehouse.WarehouseGSTIN}")
    c.drawString(50,height-120,f"Place of Dispatch : {invoice.Warehouse.WarehouseAddress}")
    c.drawString(50,height-130,f"GSTIN of Recepient:{invoice.Receiver.ReceiverGSTIN}")
    c.drawString(50,height-140,f"Place of Receipt : {invoice.Receiver.ReceiverAddress}")
    c.drawString(50,height-150,f"Document Number : {invoice.Bill_number}")
    c.drawString(50,height-160,f"Value of Goods:{invoice.ValueOfGoods}")
    c.drawString(50,height-170,f"Reason for Transport:{invoice.ReasonForTransport}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50,height-260,"PART-B")

    c.setFont("Helvetica",10)
    transport_data =[
        ["Mode","Vehicle No","From","Entered Date","Entered By","CEWB No","Multi Vehicle Info"],
        [invoice.ModeOfTransport, invoice.Driver.VehicleNumber , invoice.Warehouse.WarehouseCity,invoice.Bill_time,invoice.Warehouse.WarehouseGSTIN ,invoice.CEWBno,invoice.MultiVehInfo]
    ]

    x, y = 50, height - 280
    for row in transport_data:
            for col, text in enumerate(row):
                c.drawString(x + col * 80, y, text)
            y -= 20

    c.save()
    return file_path

 
@csrf_exempt
def get_invoice_pdf(request,invoice_id):
     file_path = generate_invoice_pdf(invoice_id)

     if file_path:
         return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
     else:
         return JsonResponse({'error': 'Invoice not found'}, status=404)