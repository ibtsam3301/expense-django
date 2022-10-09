from django.contrib import admin
from .models import Khata, MonthlyRent, ElectricityBill, WaterBill
from django_object_actions import DjangoObjectActions
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


class ImportAdmin(DjangoObjectActions, admin.ModelAdmin):
    def imports(modeladmin, request, queryset):
        print("Imports button pushed")

    changelist_actions = ('imports', )