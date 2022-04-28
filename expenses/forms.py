from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):

    nombre = forms.CharField(label='nombre', widget=forms.TextInput(attrs={'placeholder':'nombre'}))
    monto = forms.IntegerField(label='monto', widget=forms.TextInput(attrs={'placeholder':'0000'}))

    class Meta:
        model = Expense
        exclude = ('slug','user')