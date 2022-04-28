from django import forms

TYPE_CHOICES = (
        ('mesa','Mesa'),
        ('delivery','Delivery'),
    )

class SearchSaleForm(forms.Form):

    tipo = forms.ChoiceField(choices=TYPE_CHOICES)