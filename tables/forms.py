from django import forms

class AddTableForm(forms.Form):

    numero = forms.IntegerField(label='numero', widget=forms.NumberInput(attrs={'placeholder':'Nro. Mesa'}))

class DeleteTableForm(forms.Form):
    delete_field = forms.BooleanField(required=True, initial=True)

    class Meta:
        widgets = {
            'delete_field': forms.HiddenInput
        }