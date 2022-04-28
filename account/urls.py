from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('ticket/<str:number>/', views.ticket, name='ticket'),
    path('delivery/ticket/', views.delivery_ticket, name='delivery_ticket'),
]