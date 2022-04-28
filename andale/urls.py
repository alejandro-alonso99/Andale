from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls', namespace='account')),
    path('products/',include('products.urls', namespace='products')),
    path('expenses/',include('expenses.urls', namespace='expenses')),
    path('delivery/',include('delivery.urls', namespace='delivery')),
    path('sales/',include('sales.urls', namespace='sales')),
    path('tables/',include('tables.urls', namespace='tables')),
    path('summary/',include('summary.urls', namespace='summary')),
]
