from django.contrib import admin
from .models import Driver,Transporter,Driver_Location
# Register your models here.
admin.site.register(Driver)
admin.site.register(Transporter)
admin.site.register(Driver_Location)