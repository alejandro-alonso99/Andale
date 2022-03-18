from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.products_list, name='products_list'),
    path('create/',views.product_create, name="product_create"),
    path('<slug:product>/', views.product_detail, name='product_detail'),

]
