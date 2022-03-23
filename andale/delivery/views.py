from django.shortcuts import redirect, render
from .forms import AddProductForm, RemoveProductForm, CloseSaleForm
from products.models import Product
from django.utils.text import slugify
from sales.models import Sale
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create_delivery(request):

    user = request.user

    products = Product.objects.filter(user=user)

    user = str(user)

    if user not in request.session:
        request.session[user] = {}
    else:
        pass

    if 'delivery' not in request.session[user] or 'products' not in request.session[user]['delivery']:
        request.session[user]['delivery'] = {}
        request.session[user]['delivery']['products'] = {}
    else:
        pass

    def add_product(codigo,cantidad):

        if int(codigo) in list(products.values_list('codigo', flat=True)):
            product = products.get(codigo=codigo)
            product_name = slugify(str(product))
        else: 
            messages.error(request, 'No hay un producto con ese código.')
            return redirect('delivery:create_delivery')

        if product_name not in request.session[user]['delivery']['products']:
            product_price = product.precio    
            product_subtotal = product_price * float(cantidad)
            request.session[user]['delivery']['products'][product_name] = {'cantidad':{},'subtotal':{}}
            request.session[user]['delivery']['products'][product_name]['cantidad'] = cantidad
            request.session[user]['delivery']['products'][product_name]['subtotal'] = str(product_subtotal)
            request.session.modified = True
        else:
            product_price = product.precio    
            product_current_quantity = int(request.session[user]['delivery']['products'][product_name]['cantidad'])
            new_quantity = int(cantidad) + product_current_quantity
            product_subtotal = new_quantity * product_price
            request.session[user]['delivery']['products'][product_name]['cantidad'] = str(new_quantity)
            request.session[user]['delivery']['products'][product_name]['subtotal'] = str(product_subtotal)
            request.session.modified = True

    def remove_product(product):
        product_name = slugify(str(product))    
        del request.session[user]['delivery']['products'][product_name]
        request.session.modified = True

    def calculate_total():
        total = 0
        for product in request.session[user]['delivery']['products']:
            product_name = slugify(str(product))
            product_subtotal = float(request.session[user]['delivery']['products'][product_name]['subtotal'])
            total += product_subtotal
        
        return total

    def close_sale(payed_with):

        origin = 'delivery'

        args= {'user':request.user, 'origen':origin,
                'pagado_con':payed_with,'total': delivery_total}

        new_sale = Sale(**args)
        new_sale.save()

        del request.session[user]['delivery']['products']
        request.session.modified = True


    add_product_form = AddProductForm(request.POST or None)
    if add_product_form.is_valid():  
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        add_product(codigo,cantidad)
        return redirect('delivery:create_delivery')


    remove_product_form = RemoveProductForm(request.POST or None)
    if remove_product_form.is_valid():  
        product_name = request.POST.get('product_name')
        remove_product(product_name)
        return redirect('delivery:create_delivery')

    if 'delivery' not in request.session[user]:
        delivery_dict = {}

        delivery_total =  0
    else:
        delivery_dict = request.session[user]['delivery']['products']

        delivery_total =  calculate_total()
    

    close_sale_form = CloseSaleForm(request.POST or None)
    if close_sale_form.is_valid():
        payed_with = close_sale_form.cleaned_data.get('payment')

        close_sale(payed_with)

        return redirect('sales:sales_list')


    return render(request,'delivery/create_delivery.html',{
                                                        'add_product_form':add_product_form,
                                                        'delivery_dict' :delivery_dict,
                                                        'delivery_total':delivery_total,
                                                        'remove_product_form':remove_product_form,
                                                        'close_sale_form':close_sale_form,
                                                            })