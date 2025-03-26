from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from app1.models import InvoiceBill  # Assuming your model is named InvoiceBill

def generate_bill_pdf(request, bill_id):
    # Try fetching invoice bill details, otherwise use default values
    try:
        invoice_bill = InvoiceBill.objects.get(id=bill_id)
    except InvoiceBill.DoesNotExist:
           class DefaultInvoice:
            def __init__(self):
                self.Bill_number = "123456"
                self.Invoice_number = "INV-2025-001"
                self.Bill_date = "2025-03-25"
                self.Bill_time = "10:00 AM"
                self.Bill_validity = "2025-04-25"
                self.ValueOfGood = "5000.00"
                self.ReasonForTransport = "Business Transfer"
                self.ModeOfTransport = "Road"
                self.CEWBno = "N/A"
                self.MultiVehInfo = "None"

                self.Warehouse = self.WarehouseClass()
                self.Receiver = self.ReceiverClass()
                self.Transporter = self.TransporterClass()
                self.Driver = self.DriverClass()

            class WarehouseClass:
                def __init__(self):
                    self.WarehouseCompany = "ABC Warehouses"
                    self.WarehouseGSTIN = "29ABCDE1234F1Z5"
                    self.WarehouseAddress = "123 Warehouse Street, City"
                    self.WarehouseCity = "Metropolis"

            class ReceiverClass:
                def __init__(self):
                    self.ReceiverCompany_GSTIN = "29XYZDE5678F1Z6"
                    self.ReceiverCompany_Address = "456 Receiver Lane, City"

            class TransporterClass:
                def __init__(self):
                    self.TransporterName = "XYZ Transporters"

            class DriverClass:
                def __init__(self):
                    self.VehicleNumber = "KA01AB1234"

           invoice_bill = DefaultInvoice() 
    
    # Create a response object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{invoice_bill.Bill_number}.pdf"'
    
    # Create a PDF document
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Bill Number {invoice_bill.Bill_number}")
    
    # Invoice Upper Section
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"E-WayBill Number: {invoice_bill.Invoice_number}")
    p.drawString(50, height - 120, f"E-WayBill Date: {invoice_bill.Bill_date}")
    p.drawString(50, height - 140, f"Generated By: {invoice_bill.Warehouse.WarehouseCompany}")
    p.drawString(50, height - 160, f"Valid From: {invoice_bill.Bill_time}")
    p.drawString(50, height - 180, f"Valid Until: {invoice_bill.Bill_validity}")
    
    # PART-A Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 220, "PART-A")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 240, f"GSTIN OF Supplier: {invoice_bill.Warehouse.WarehouseGSTIN}")
    p.drawString(50, height - 260, f"Place of Dispatch: {invoice_bill.Warehouse.WarehouseAddress}")
    p.drawString(50, height - 280, f"GSTIN OF Recipient: {invoice_bill.Receiver.ReceiverCompany_GSTIN}")
    p.drawString(50, height - 300, f"Place of Delivery: {invoice_bill.Receiver.ReceiverCompany_Address}")
    p.drawString(50, height - 320, f"Document No.: {invoice_bill.Bill_number}")
    p.drawString(50, height - 340, f"Document Date: {invoice_bill.Bill_date}")
    p.drawString(50, height - 360, f"Value of Goods: {invoice_bill.ValueOfGood}")
    p.drawString(50, height - 380, f"Reason for Transport: {invoice_bill.ReasonForTransport}")
    p.drawString(50, height - 400, f"Transporter Name: {invoice_bill.Transporter.TransporterName}")
    
    # PART-B Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 440, "PART-B")
    
    # Table Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 460, "Mode")
    p.drawString(150, height - 460, "Vehicle Number")
    p.drawString(250, height - 460, "From")
    p.drawString(350, height - 460, "Entered Date")
    p.drawString(450, height - 460, "Entered By")
    p.drawString(550, height - 460, "CEWB No.")
    p.drawString(650, height - 460, "Multi Veh. Info")
    
    # Table Data
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 480, str(invoice_bill.ModeOfTransport))
    p.drawString(150, height - 480, str(invoice_bill.Driver.VehicleNumber))
    p.drawString(250, height - 480, str(invoice_bill.Warehouse.WarehouseCity))
    p.drawString(350, height - 480, str(invoice_bill.Bill_time))
    p.drawString(450, height - 480, str(invoice_bill.Warehouse.WarehouseGSTIN))
    p.drawString(550, height - 480, str(invoice_bill.CEWBno))
    p.drawString(650, height - 480, str(invoice_bill.MultiVehInfo))
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response
