from cProfile import label
from django import forms
from .models import Product
from django.db import models

class ProductForm(forms.ModelForm):

    codigo = forms.IntegerField(label='código', widget=forms.TextInput(attrs={'placeholder':'Código'}))
    nombre = forms.CharField(label='nombre', widget=forms.TextInput(attrs={'placeholder':'nombre'}))
    precio = forms.IntegerField(label='precio', widget=forms.TextInput(attrs={'placeholder':'0000'}))


    class Meta:
        model = Product
        exclude = ('slug','user')

class DateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(forms.Form):
    query = forms.CharField()

class DateForm(forms.Form):
    date_query_start = forms.DateField(widget=DateInput)
    date_query_end = forms.DateField(widget=DateInput)

class DestroyObjectForm(forms.Form):
    field = forms.BooleanField(required=False)

    widgets = {
            'field': forms.HiddenInput
        }

class ChangeFoodPriceForm(forms.Form):
    food_amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'ej. 15 = 15%'}))

class ChangeDrinksPriceForm(forms.Form):
    drinks_amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'ej. 15 = 15%'}))