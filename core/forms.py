# forms.py
from django import forms
from .models import *
from .widgets import MonthYearWidget

class ElectricityForm(forms.ModelForm):
    class Meta:
        model = ElectricityBill
        exclude = []

    month = forms.DateField(
    required=False,
    widget=MonthYearWidget()
)

class WaterForm(forms.ModelForm):
    class Meta:
        model = WaterBill
        exclude = []

    month = forms.DateField(
    required=False,
    widget=MonthYearWidget()
)
    
class InternetForm(forms.ModelForm):
    class Meta:
        model = InternetBill
        exclude = []

    month = forms.DateField(
    required=False,
    widget=MonthYearWidget()
)