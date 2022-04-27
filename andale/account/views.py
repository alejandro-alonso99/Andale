from django.shortcuts import render
import datetime
from django.utils.text import slugify

def ticket(request,number):

    user = str(request.user)

    tables_dict = request.session[user]['mesas']['numbers'][number]

    date = datetime.datetime.now

    return render(request,'account/ticket.html',{
                                                'tables_dict':tables_dict,
                                                'date':date,
                                                'number':number,
                                                })

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