from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('submit_Form',views.submit_form_receiver,name='submit_form_receiver'),
    path('get-inventory-data',views.get_details_bill,name='get_details_bill'),
]