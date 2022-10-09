from django.db import models
from django.contrib.auth import get_user_model
from .mixins import DateTruncMixin
from datetime import timedelta, date

User = get_user_model()

class MonthField(DateTruncMixin, models.DateField):
    def truncate_date(self, dt):
        return dt - timedelta(days=dt.day-1)

class BaseModel(models.Model):
   created_on = models.DateTimeField(auto_now_add=True)
   modified_on = models.DateTimeField(auto_now=True)
   class Meta:
       abstract = True

class Khata(BaseModel):
    amount = models.IntegerField()
    description = models.TextField(blank=True)
    paid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="khata")
    date = models.DateField(null=True, blank=True, help_text="keep the current billing month")
    
    def __str__(self) -> str:
        return str(self.description)

class MonthlyRent(models.Model):
    amount = models.IntegerField(default=25000)
    
    def __str__(self) -> str:
        return str(self.amount)
    
class ElectricityBill(BaseModel):
    amount = models.IntegerField()
    month = MonthField("Month Value", help_text="electricity bill")
    due_date = models.DateField(blank=True, null=True, help_text="due date")
   
    def __str__(self) -> str:
        return str(self.amount)

class WaterBill(BaseModel):
    amount = models.IntegerField()
    month = MonthField("Month Value", help_text="water bill")
   
    def __str__(self) -> str:
        return str(self.amount)