from django.shortcuts import redirect, render
from .models import *
from datetime import date
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime, date
from reportlab.pdfgen import canvas
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse


User = get_user_model()
    
def get_and_save_electricity_bill(month):
    month_of_bill = month.strftime("%B")
    bill_url = 'http://www.lesco.gov.pk:36269/BillNew.aspx?BatchNo=08&SubDiv=11218&RefNo=1669101&RU=U&Exec=941N7'
    r = requests.get(bill_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    bill_month = soup.select_one('#page1-div > p:nth-child(53) > b').text
    bill_month = ''.join([i for i in bill_month if not i.isdigit()])
    if bill_month.lower() != month_of_bill[3].lower():
        bill = soup.select_one('#page1-div > p:nth-child(164) > b').text
        due_date = parse(soup.select_one('#page1-div > p:nth-child(201) > b').text)
        
        ElectricityBill.objects.create(
            amount=int(bill.replace("Rs. ", "").replace(",", "")),
            month = date(2022, int(datetime.strftime(month,'%m')), 1),
            due_date = due_date
        )
        return bill, due_date
    
    return None, None
    
def get_data_from_model(year, month):
    month_year = date(int(year), int(month), 1) 
    monthly_bill = MonthlyRent.objects.all().first().amount
    electricity_bill_data = ElectricityBill.objects.filter(month__month=month_year.month).first()
    if electricity_bill_data:
        electricity_bill = electricity_bill_data.amount
        due_date = electricity_bill_data.due_date
    else:
        electricity_bill, due_date = get_and_save_electricity_bill(month_year)
        try:
            electricity_bill = int(electricity_bill.replace("Rs. ", "").replace(",", ""))
        except:
            electricity_bill = 0
            
    water_bill = WaterBill.objects.all().filter(month__month=month_year.month).first().amount
    internet_bill = InternetBill.objects.all().filter(month__month=month_year.month).first().amount
    khatas = Khata.objects.filter(date__month=month_year.month).select_related('paid_by')
   
    khata_bill = Khata.objects.aggregate(Sum('amount'))['amount__sum']
    if not khata_bill:
        khata_bill = 0

        
    total_bill = monthly_bill + electricity_bill + water_bill + khata_bill + internet_bill
    
    total_users = User.objects.filter(is_superuser=False)
    
    bill_split = total_bill/total_users.count()

    return total_bill, bill_split, total_users, khatas, electricity_bill, water_bill, month_year, due_date, internet_bill
    
def homepage(request):
    context = {}
    if request.method == 'POST':
        year = request.POST["year"]
        month = request.POST["month"]
        try:
            total_bill, bill_split, \
            total_users, khatas, electricity_bill, water_bill, month_year, due_date, internet_bill = get_data_from_model(year, month)
        except:
            return redirect('generate-bill')    
        
        context = {"total_bill": total_bill, 
                   "bill_split": bill_split, 
                   "users":total_users, 
                   'khatas':khatas,
                   "electricity_bill":electricity_bill,
                   "internet_bill":internet_bill,
                   "due_date":due_date,
                   "water_bill":water_bill,
                   "year":year,
                   "month":month,}
        
    return render(request,'main/homepage.html', context=context)



def check_khata(user, bill):
    amounts = []
    user_bill = bill
    user_khata = user.khata.values('amount')
    for khata in user_khata:
        amount = khata.get('amount')
        user_bill = round(user_bill-amount,2)
        amounts.append(str(amount))
    
    dt_st = f"- {''.join(amounts)} = {user_bill}"  if user_khata else ""
    
    return dt_st

def generate_PDF(request, year, month):
 
    total_bill, bill_split, total_users, khatas, \
    electricity_bill, water_bill, month_year, due_date, internet_bill = get_data_from_model(year, month)
    current_month = month_year.strftime("%B")
    response = HttpResponse(content_type='application/pdf') 

        
    response['Content-Disposition'] = f'attachment; filename="{current_month}-{month_year.year}"' 

    p = canvas.Canvas(response)
    x = p._pagesize[0] / 2
    p.setFont('Helvetica-Bold', 18)

    
    p.drawCentredString(x,800,f"Bill For the Month of {current_month}") 
    
    p.setFont('Helvetica-Bold', 10)
    p.drawCentredString(x,760,f"Generated On {datetime.today().date()} at {datetime.today().time().strftime('%H:%M')}") 
    p.setFont('Helvetica-Bold', 13)
    
    p.drawCentredString(x,700,f"Total Bill = {total_bill}")
    khata_y = 650
    for khata in khatas:
        p.drawCentredString(x,khata_y,f"{khata.description} --- {khata.date} --- {khata.amount} = {khata.paid_by.first_name}")
        khata_y-=30
    
    p.drawCentredString(x,khata_y-30,f"Electricity Bill = {electricity_bill} (due date: {due_date})")
    khata_y-=30
    
    p.drawCentredString(x,khata_y-30,f"Internet Bill = {internet_bill}")
    khata_y-=30
    
    p.drawCentredString(x,khata_y-30,f"Water Bill = {water_bill}")
    khata_y-=80
    
    for user in total_users:
        calc = check_khata(user, bill_split)
        p.drawCentredString(x,khata_y-30,f"{user.first_name} {user.last_name} = {bill_split} {calc}")
        khata_y-=30
    
    
    
    p.showPage() 
    p.save() 

    
    return response