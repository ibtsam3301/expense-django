from django.contrib import admin
from .models import Khata, MonthlyRent, ElectricityBill, WaterBill
from .forms import *

@admin.register(Khata)
class KhataAdmin(admin.ModelAdmin):
    pass

@admin.register(MonthlyRent)
class MonthlyRentAdmin(admin.ModelAdmin):
    pass

@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    form = ElectricityForm

@admin.register(WaterBill)
class WaterBillAdmin(admin.ModelAdmin):
    form = WaterForm
