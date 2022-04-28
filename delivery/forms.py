from django import forms

class AddProductForm(forms.Form):

    codigo = forms.IntegerField(label='código', widget=forms.NumberInput(attrs={'placeholder':'Código'}))
    cantidad = forms.IntegerField(label='cantidad', widget=forms.NumberInput(attrs={'placeholder':'Cantidad'}))

class RemoveProductForm(forms.Form):
    field = forms.BooleanField(required=True, initial=True)

    class Meta:
        widgets = {
            'field': forms.HiddenInput
        }

PAYMENT_CHOICES = (
        ('efectivo','Efectivo'),
        ('tarjeta','Tarjeta'),
    )

class CloseSaleForm(forms.Form):

    payment = forms.ChoiceField(choices=PAYMENT_CHOICES)
    