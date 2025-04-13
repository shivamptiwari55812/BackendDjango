from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('saveDetails',views.getDetails,name='getDetails'),
    path('save_location',views.saveLocation,name='saveLocation'),
]