from django.shortcuts import render
from sales.models import Sale
from expenses.models import Expense
import datetime

def summary_dashboard(request):

    user = request.user

    sales = Sale.objects.filter(user=user)

    expenses = Expense.objects.filter(user=user)

    today = datetime.datetime.today()    

    today_sales = sales.filter(fecha__day=today.day, fecha__month=today.month, fecha__year=today.year)

    total_today = sum(list(map(int,today_sales.values_list('total',flat=True))))

    today_sales_count = today_sales.count()

    today_cash_sales = today_sales.filter(pagado_con = 'efectivo')

    total_cash_today = sum(list(map(int,today_cash_sales.values_list('total',flat=True))))

    today_card_sales = today_sales.filter(pagado_con = 'tarjeta')

    total_card_today = sum(list(map(int,today_card_sales.values_list('total',flat=True))))

    month_sales = sales.filter(fecha__month = today.month)

    month_sales_count = month_sales.count()

    month_sales_total = sum(list(map(int, month_sales.values_list('total',flat=True))))

    month_cash_sales = month_sales.filter(pagado_con = 'efectivo')

    month_cash_total = sum(list(map(int, month_cash_sales.values_list('total',flat=True))))

    month_card_sales = month_sales.filter(pagado_con = 'tarjeta')

    month_card_total = sum(list(map(int, month_card_sales.values_list('total',flat=True))))

    month_expenses = expenses.filter(fecha__month = today.month)

    month_expenses_total = sum(list(map(int, month_expenses.values_list('monto',flat=True))))

    month_services_expenses = month_expenses.filter(tipo = 'servicios')

    month_supplies_expenses = month_expenses.filter(tipo= 'insumos')

    month_services_total =sum(list(map(int, month_services_expenses.values_list('monto',flat=True))))

    month_supplies_total = sum(list(map(int, month_supplies_expenses.values_list('monto',flat=True))))

    month_earned = month_sales_total - month_expenses_total

    return render(request, 'summary/summary_dashboard.html',{
                                                            'total_today':total_today,
                                                            'total_cash_today':total_cash_today,
                                                            'total_card_today':total_card_today,
                                                            'today_sales_count':today_sales_count,
                                                            'month_sales_count':month_sales_count,
                                                            'month_sales_total':month_sales_total,
                                                            'month_cash_total':month_cash_total,
                                                            'month_card_total':month_card_total,
                                                            'month_expenses_total':month_expenses_total,
                                                            'month_services_total':month_services_total,
                                                            'month_supplies_total':month_supplies_total,
                                                            'month_earned':month_earned,
                                                            })