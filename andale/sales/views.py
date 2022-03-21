from django.shortcuts import render, get_object_or_404
from .models import Sale
from django.contrib.auth.decorators import login_required

@login_required
def sales_list(request):

    user = request.user

    sales = Sale.objects.filter(user=user)

    return render(request, 'sales/sales_list.html',{'sales':sales})

@login_required
def sale_detail(request, sale):

    user = request.user

    sale = get_object_or_404(Sale, user= user, 
                                        slug = sale,)

    return render(request,'sales/sale_detail.html',{})