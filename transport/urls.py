from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('submit_Transporter',views.TransporterSet,name='TransporterSet'),
    path('submit_Driver',views.Driverget,name='Driverget'),
    path('save_location',views.saveLocation,name='saveLocation'),
]