from django.shortcuts import redirect, render
from products.models import Product
from .forms import AddTableForm, DeleteTableForm
from django.contrib import messages
from delivery.forms import AddProductForm, RemoveProductForm, CloseSaleForm
from django.utils.text import slugify
from sales.models import Sale

def tables_dashboard(request):

    user = request.user
    
    products = Product.objects.filter(user=user)

    user = str(user)

    if user not in request.session:
        request.session[user] = {}
    else:
        pass

    if 'mesas' not in request.session[user] or 'numbers' not in request.session[user]['mesas']:
        request.session[user]['mesas'] = {}
        request.session[user]['mesas']['numbers'] = {}

    def add_table(table_number):

        if table_number in request.session[user]['mesas']['numbers']:
            messages.error(request, 'Esa mesa ya está abierta.')
        else:
            request.session[user]['mesas']['numbers'][table_number] = {'products':{}}
            request.session.modified = True

    def add_product(table_number,codigo,cantidad):
        
        if int(codigo) in list(products.values_list('codigo', flat=True)):
            product = products.get(codigo=codigo)
            product_name = slugify(str(product))
        else: 
            messages.error(request, 'No hay un producto con ese código.')
            return redirect('tables:tables_dashboard')    
        
        table = request.session[user]['mesas']['numbers'][table_number]

        if product_name not in request.session[user]['mesas']['numbers'][table_number]['products']:
            product_price = product.precio    
            product_subtotal = product_price * float(cantidad)
            table['products'][product_name] = {'cantidad':{},'subtotal':{}}
            table['products'][product_name]['cantidad'] = cantidad
            table['products'][product_name]['subtotal'] = str(product_subtotal)
            request.session.modified = True

        else:
            product_price = product.precio    
            product_current_quantity = int(table['products'][product_name]['cantidad'])
            new_quantity = int(cantidad) + product_current_quantity
            product_subtotal = new_quantity * product_price
            table['products'][product_name]['cantidad'] = new_quantity
            table['products'][product_name]['subtotal'] = product_subtotal
            request.session.modified = True

    def remove_product(table_number, product_name):
        product_name = slugify(str(product_name))    
        del request.session[user]['mesas']['numbers'][table_number]['products'][product_name]
        request.session.modified = True

    def calculate_totals():
        for number in request.session[user]['mesas']['numbers']:
            table = request.session[user]['mesas']['numbers'][number]
            total = 0
            for product in table['products']:
                total += float(table['products'][product]['subtotal'])
                
            table['total'] = total

        request.session.modified = True

    def close_sale(table_number, payed_with):

        origin = 'mesa'

        sale_total = request.session[user]['mesas']['numbers'][table_number]['total']

        args= {'user':request.user, 'origen':origin,
                'pagado_con':payed_with,'total': sale_total}
        
        new_sale = Sale(**args)
        new_sale.save()

        del request.session[user]['mesas']['numbers'][table_number]
        request.session.modified = True

    add_table_form = AddTableForm(request.POST or None)
    if add_table_form.is_valid():
        table_number = request.POST['numero']
        add_table(table_number)
        return redirect('tables:tables_dashboard')    

    add_product_form = AddProductForm(request.POST or None)
    if add_product_form.is_valid():
        table_number = request.POST.get('table_number')
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        add_product(table_number,codigo,cantidad)
        return redirect('tables:tables_dashboard')    

    remove_product_form = RemoveProductForm(request.POST or None)
    if remove_product_form.is_valid():  
        table_number = request.POST.get('table_number')
        product_name = request.POST.get('product_name')
        remove_product(table_number,product_name)
        return redirect('tables:tables_dashboard')

    close_sale_form = CloseSaleForm(request.POST or None)
    if close_sale_form.is_valid():
        payed_with = close_sale_form.cleaned_data.get('payment')
        table_number = request.POST.get('table_number')
        close_sale(table_number,payed_with)

        return redirect('sales:sales_list')

    delete_table_form = DeleteTableForm(request.POST or None)
    if delete_table_form.is_valid():
        print('ok')
        table_number = request.POST.get('table_number')
        del request.session[user]['mesas']['numbers'][table_number]
        request.session.modified = True

        return redirect('tables:tables_dashboard')

    tables_dict = request.session[user]['mesas']['numbers']
    
    calculate_totals()

    return render(request,'tables/tables_dashboard.html',{
                                                        'add_table_form':add_table_form,
                                                        'add_product_form':add_product_form,
                                                        'remove_product_form':remove_product_form,
                                                        'delete_table_form':delete_table_form,
                                                        'close_sale_form':close_sale_form,
                                                        'tables_dict':tables_dict,})