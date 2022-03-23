from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
]