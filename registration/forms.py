from django import forms
from .models import Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            'WarehouseCompany_Name', 'WarehouseAddress', 'WarehouseCity', 'WarehouseGSTIN',
            'WarehouseState', 'WarehousePincode', 'WarehouseContact', 'WarehouseEmail',
            'WarehouseType', 'WarehouseCapacity', 'WarehouseAvailable', 'document'
        ]
