from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('pdf/<str:Invoice_number>/',views.generate_invoice_pdf,name='generate_invoice_pdf'),
]