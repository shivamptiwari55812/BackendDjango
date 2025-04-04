from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('add_item',views.add_item_inventory,name='add_item_inventory'),
    path('del_product',views.del_product_inventory,name='del_product_inventory'),
    path('edit_product',views.edit_product_inventory,name='edit_product_inventory'),
    path('get_product',views.get_product_details,name='get_product_details'),
    path('get_productDetails/<int:product_id>/', views.get_product_foredit, name='get_product_foredit'),
    # path('get_product_status',views.get_product_Status,name='get_product_Status'),
    path('sendEmail',views.sent_notification,name='sent_notification'),
]