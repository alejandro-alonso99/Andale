from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale
from django.contrib.auth.decorators import login_required
from products.forms import DateForm, DestroyObjectForm
from django.contrib.postgres.search import SearchVector
from .forms import SearchSaleForm

@login_required
def sales_list(request):

    user = request.user

    sales = Sale.objects.filter(user=user)

    search_form = SearchSaleForm()

    date_form = DateForm()

    tipo = None

    date_query_start = None
    date_query_end = None

    if 'tipo' in request.GET:
        form = SearchSaleForm(request.GET)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            sales = sales.annotate(search=SearchVector('origen'),).filter(search=tipo)

    if 'date_query_start' and 'date_query_end' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query_start = form.cleaned_data['date_query_start'].strftime("%Y-%m-%d")
            date_query_end = form.cleaned_data['date_query_end'].strftime("%Y-%m-%d")
            sales = sales.filter(fecha__range=[date_query_start, date_query_end])

    return render(request, 'sales/sales_list.html',{
                                                    'sales':sales,
                                                    'search_form':search_form,
                                                    'date_form':date_form,
                                                    'tipo':tipo,
                                                    'date_query_start':date_query_start,
                                                    'date_query_end':date_query_end,
                                                    })

@login_required
def sale_detail(request, sale):

    user = request.user

    sale = get_object_or_404(Sale, user= user, 
                                        slug = sale,)

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        sale.delete()
        
        return redirect('sales:sales_list')
    else:
        destroy_object_form = DestroyObjectForm()

    return render(request,'sales/sale_detail.html',{
                                                    'sale':sale,
                                                    'destroy_object_form':destroy_object_form,                                                    
                                                    })