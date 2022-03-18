from django.shortcuts import render

def create_delivery(request):

    return render(request,'delivery/create_delivery.html',{})