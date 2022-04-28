from unicodedata import name
from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('',views.sales_list, name='sales_list'),
    path('<int:id>/',views.sale_detail, name='sale_detail'),
]