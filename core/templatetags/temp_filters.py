from django import template

register = template.Library()

@register.simple_tag
def check_khata(user, bill, year, month):
    amounts = []
    user_bill = bill
    user_khata = user.khata.filter(date__month=int(month), date__year=int(year)).values('amount')
    for khata in user_khata:
        amount = khata.get('amount')
        user_bill = round(user_bill-amount,2)
        amounts.append(str(amount))
    
    dt_st = f"- {''.join(amounts)} = {user_bill}"  if user_khata else ""
   
    return dt_st