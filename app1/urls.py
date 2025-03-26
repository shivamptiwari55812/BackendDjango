from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    
    # path('eway',views.EWayBill,name='EWayBill'),
    # path('pdf',views.generate_bill_pdf,name='generate_bill_pdf'),
    path('submit_Form',views.submit_form_receiver,name="submit_Form"),
    path('t',views.recordOutbound,name='recordOutbound'),
    path('get-inventory-data',views.get_inventory_data,name='get_inventory_data'),
    path('submit_Warehouseform',views.warehouseSet,name="warehouseSet"),
    path('setTransporter',views.TransporterSet,name="TransporterSet"),
  
]