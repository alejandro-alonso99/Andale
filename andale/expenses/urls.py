import imp
from unicodedata import name
from django import views
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expenses_list, name='expenses_list'),
    path('create/', views.expense_create, name='expense_create'),
    path('<slug:expense>/', views.expense_detail, name='expense_detail')
]