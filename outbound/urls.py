from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('saveDetails',views.submit_form_receiver,name='submit_form_receiver'),
    path('getOrderDetails',views.getOrdersDetails,name='getOrdersDetails'),
    path('chart',views.chart_data_view,name='chart_data_view'),
    path('piechart_view',views.piechart_view,name='piechart_view'),
]