from django.shortcuts import redirect,render
import datetime
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from products.forms import DestroyObjectForm
from sales.models import Sale

@login_required
def ticket(request,number):

    user = str(request.user)

    tables_dict = request.session[user]['mesas']['numbers'][number]

    date = datetime.datetime.now

    return render(request,'account/ticket.html',{
                                                'tables_dict':tables_dict,
                                                'date':date,
                                                'number':number,
                                                })
                                                
@login_required
def delivery_ticket(request):

    user = str(request.user)

    delivery_dict = request.session[user]['delivery']['products']

    date = datetime.datetime.now

    def calculate_total():
        total = 0
        for product in request.session[user]['delivery']['products']:
            product_name = slugify(str(product))
            product_subtotal = float(request.session[user]['delivery']['products'][product_name]['subtotal'])
            total += product_subtotal
        return total

    delivery_total = calculate_total()

    return render(request, 'account/delivery_ticket.html',{
                                                            'delivery_dict':delivery_dict,
                                                            'date':date,
                                                            'delivery_total':delivery_total,
                                                        })

def delete_sales_and_expenses(request):

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        user_sales = Sale.objects.filter(user=request.user)
        user_expenses = Expense.objects.filter(user=request.user)

        user_sales.delete()
        user_expenses.delete()
        
        return redirect('products:products_list')
        
    else:
        destroy_object_form = DestroyObjectForm()

    return render(request,'account/delete_all.html',{'destroy_object_form':destroy_object_form})