from django.urls import path
from . import views

app_name = 'summary'

urlpatterns = [
    path('', views.summary_dashboard, name='summary_dashboard')
]