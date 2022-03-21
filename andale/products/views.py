from django.shortcuts import get_object_or_404, redirect, render
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, SearchForm, ChangeFoodPriceForm,ChangeDrinksPriceForm,DestroyObjectForm
from django.contrib.postgres.search import SearchVector


@login_required
def products_list(request):

    search_form = SearchForm()

    query = None

    products = Product.objects.filter(user= request.user)

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = products.annotate(search=SearchVector('nombre'),).filter(search=query)
        
    
    change_food_price_form = ChangeFoodPriceForm()

    if 'food_amount' in request.GET:
        change_food_price_form = ChangeFoodPriceForm(request.GET)
        if change_food_price_form.is_valid():
            food_amount = change_food_price_form.cleaned_data['food_amount']
            products = products.filter(categoria='comida')
            for product in products:
                product.precio += (product.precio * (food_amount/100))
                product.save()

            return redirect('products:products_list')

    change_drinks_price_form = ChangeDrinksPriceForm()

    if 'drinks_amount' in request.GET:
        change_drinks_price_form = ChangeDrinksPriceForm(request.GET)
        if change_drinks_price_form.is_valid():
            drinks_amount = change_drinks_price_form.cleaned_data['drinks_amount']
            products = products.filter(categoria='bebida')
            for product in products:
                product.precio += (product.precio * (drinks_amount/100))
                product.save()

            return redirect('products:products_list')

    return render(request,'products/products_list.html',{
                                                        'products':products,
                                                        'search_form':search_form,
                                                        'query':query,
                                                        'change_drinks_price_form':change_drinks_price_form,
                                                        'change_food_price_form':change_food_price_form,
                                                        })


@login_required
def product_create(request):

    product_form = ProductForm(request.POST or None)

    if product_form.is_valid():  
        codigo = product_form.cleaned_data.get('codigo')
        nombre = product_form.cleaned_data.get('nombre')
        precio = product_form.cleaned_data.get('precio')
        categoria = product_form.cleaned_data.get('categoria')

        attrs = {'codigo':codigo, 'nombre':nombre, 
            'precio':precio, 'categoria':categoria, 'user':request.user}

        new_product = Product(**attrs)
        new_product.save()


        return redirect('products:products_list')

    return render(request, 'products/product_create.html',{
                                                            'product_form':product_form,
                                                        })
@login_required
def product_detail(request, product):

    user = request.user

    product = get_object_or_404(Product, user= user, 
                                        slug = product,)                

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        product.delete()
        
        return redirect('products:products_list')
        
    else:
        destroy_object_form = DestroyObjectForm()

    change_price_form = ChangeFoodPriceForm()

    if 'food_amount' in request.GET:
        change_price_form = ChangeFoodPriceForm(request.GET)
        if change_price_form.is_valid():

            food_amount = change_price_form.cleaned_data['food_amount']

            product.precio += (product.precio * (food_amount/100))
            product.save()

            return redirect(product.get_absolute_url())

    return render(request, 'products/product_detail.html', {
                                                            'product':product,
                                                            'change_price_form':change_price_form,
                                                            'destroy_object_form':destroy_object_form,
                                                            })                                                    